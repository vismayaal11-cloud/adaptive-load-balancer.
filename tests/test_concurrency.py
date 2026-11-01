import concurrent.futures
import json
import socket
import time

HOST = "127.0.0.1"
PORT = 8000
CLIENTS = 10

def send_one(request_id):
    start = time.perf_counter()
    try:
        with socket.create_connection((HOST, PORT), timeout=5) as sock:
            sock.settimeout(20)
            request = {
                "request_id": request_id,
                "payload": "concurrency test"
            }
            sock.sendall((json.dumps(request) + "\n").encode())
            reader = sock.makefile("r", encoding="utf-8")
            response = json.loads(reader.readline())

        latency = (time.perf_counter() - start) * 1000
        return {
            "id": request_id,
            "status": response.get("status"),
            "server": response.get("server"),
            "latency_ms": round(latency, 2)
        }
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return {"id": request_id, "status": "failed", "error": str(error)}

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=CLIENTS) as pool:
        results = list(pool.map(send_one, range(1, CLIENTS + 1)))

    for result in results:
        print(result)

    success = sum(result["status"] == "ok" for result in results)
    print(f"\nSuccessful requests: {success}/{CLIENTS}")
