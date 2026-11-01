import argparse
import json
import socket
import threading
import time

def handle_client(conn, address, name, delay):
    print(f"[CONNECTED] {name}: {address}")
    try:
        with conn:
            reader = conn.makefile("r", encoding="utf-8")
            for line in reader:
                try:
                    request = json.loads(line)
                    if not isinstance(request, dict):
                        raise ValueError("Expected a JSON object")

                    time.sleep(delay)
                    response = {
                        "request_id": request.get("request_id"),
                        "server": name,
                        "status": "ok",
                        "message": "Request processed"
                    }
                except (json.JSONDecodeError, ValueError) as error:
                    response = {"status": "error", "message": str(error)}

                conn.sendall(
                    (json.dumps(response) + "\n").encode("utf-8")
                )
                print(f"[SERVED] {name}: {response.get('request_id')}")
    except (OSError, ConnectionError) as error:
        print(f"[ERROR] {name}: {error}")
    finally:
        print(f"[DISCONNECTED] {name}: {address}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--delay", type=float, default=0.0)
    args = parser.parse_args()

    if not 1 <= args.port <= 65535 or args.delay < 0:
        parser.error("Invalid port or delay")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", args.port))
    server.listen(50)

    print(f"[STARTED] {args.name} listening on port {args.port}")

    try:
        while True:
            conn, address = server.accept()
            threading.Thread(
                target=handle_client,
                args=(conn, address, args.name, args.delay),
                daemon=True
            ).start()
    except KeyboardInterrupt:
        print(f"\n[STOPPED] {args.name}")
    finally:
        server.close()

if __name__ == "__main__":
    main()
