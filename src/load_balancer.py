import argparse
import json
import socket
import threading
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor

LOCK = threading.Lock()
ROUND_ROBIN_INDEX = 0
OVERLOAD_MS = 500
MAX_SAMPLES = 20

BACKENDS = {
    "server1": {
        "host": "127.0.0.1", "port": 9001,
        "healthy": True, "overloaded": False,
        "active": 0, "latencies": []
    },
    "server2": {
        "host": "127.0.0.1", "port": 9002,
        "healthy": True, "overloaded": False,
        "active": 0, "latencies": []
    }
}

CONTROLLER_URL = None

def notify_controller(name, healthy, overloaded):
    if not CONTROLLER_URL:
        return

    event = {
        "server": name,
        "healthy": healthy,
        "overloaded": overloaded
    }
    request = urllib.request.Request(
        CONTROLLER_URL,
        data=json.dumps(event).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(request, timeout=2) as response:
            print(f"[CONTROLLER] {name}: HTTP {response.status}")
    except (OSError, urllib.error.URLError) as error:
        print(f"[CONTROLLER ERROR] {error}")

def choose_backend(mode):
    global ROUND_ROBIN_INDEX

    with LOCK:
        candidates = [
            (name, info) for name, info in BACKENDS.items()
            if info["healthy"] and not info["overloaded"]
        ]

        if not candidates:
            return None

        if mode == "round_robin":
            name, _ = candidates[ROUND_ROBIN_INDEX % len(candidates)]
            ROUND_ROBIN_INDEX += 1
            return name

        def score(item):
            name, info = item
            samples = info["latencies"]
            average = sum(samples) / len(samples) if samples else 0
            return (info["active"], average, name)

        return min(candidates, key=score)[0]

def update_backend(name, latency_ms=None, failed=False):
    event = None

    with LOCK:
        info = BACKENDS[name]
        old_state = (info["healthy"], info["overloaded"])

        if failed:
            info["healthy"] = False
            info["overloaded"] = False
        else:
            info["healthy"] = True
            if latency_ms is not None:
                info["latencies"].append(latency_ms)
                info["latencies"] = info["latencies"][-MAX_SAMPLES:]
                average = sum(info["latencies"]) / len(info["latencies"])
                info["overloaded"] = average > OVERLOAD_MS

        new_state = (info["healthy"], info["overloaded"])
        if new_state != old_state:
            event = (name, *new_state)

    if event:
        notify_controller(*event)

def forward_request(message, mode):
    name = choose_backend(mode)
    if name is None:
        return {"status": "error", "message": "No healthy backend available"}

    with LOCK:
        BACKENDS[name]["active"] += 1

    start = time.perf_counter()

    try:
        backend = BACKENDS[name]
        with socket.create_connection(
            (backend["host"], backend["port"]), timeout=3
        ) as upstream:
            upstream.settimeout(15)
            upstream.sendall((json.dumps(message) + "\n").encode())
            reader = upstream.makefile("r", encoding="utf-8")
            line = reader.readline()
            if not line:
                raise ConnectionError("Backend returned no response")
            response = json.loads(line)

        latency = (time.perf_counter() - start) * 1000
        update_backend(name, latency_ms=latency)
        print(
            f"[FORWARD] request={message.get('request_id')} "
            f"backend={name} latency_ms={latency:.2f}"
        )
        return response

    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"[BACKEND ERROR] {name}: {error}")
        update_backend(name, failed=True)
        return {
            "status": "error",
            "backend": name,
            "message": "Backend unavailable"
        }

    finally:
        with LOCK:
            BACKENDS[name]["active"] -= 1

def handle_client(conn, address, mode, executor):
    print(f"[CLIENT CONNECTED] {address}")
    try:
        with conn:
            conn.settimeout(30)
            reader = conn.makefile("r", encoding="utf-8")
            for line in reader:
                try:
                    message = json.loads(line)
                    if not isinstance(message, dict):
                        raise ValueError("Expected a JSON object")
                    future = executor.submit(forward_request, message, mode)
                    response = future.result()
                except (json.JSONDecodeError, ValueError) as error:
                    response = {"status": "error", "message": str(error)}

                conn.sendall((json.dumps(response) + "\n").encode())
    except (OSError, ConnectionError) as error:
        print(f"[CLIENT ERROR] {error}")
    finally:
        print(f"[CLIENT DISCONNECTED] {address}")

def main():
    global CONTROLLER_URL

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument(
        "--mode", choices=["round_robin", "adaptive"],
        default="adaptive"
    )
    parser.add_argument(
        "--controller-url", default=None,
        help="Optional controller HTTP event endpoint"
    )
    args = parser.parse_args()
    CONTROLLER_URL = args.controller_url

    executor = ThreadPoolExecutor(max_workers=50)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((args.host, args.port))
    server.listen(100)

    print(
        f"[LOAD BALANCER] listening on {args.host}:{args.port}, "
        f"mode={args.mode}"
    )

    try:
        while True:
            conn, address = server.accept()
            threading.Thread(
                target=handle_client,
                args=(conn, address, args.mode, executor),
                daemon=True
            ).start()
    except KeyboardInterrupt:
        print("\n[LOAD BALANCER] stopping")
    finally:
        server.close()
        executor.shutdown(wait=False, cancel_futures=True)

if __name__ == "__main__":
    main()
