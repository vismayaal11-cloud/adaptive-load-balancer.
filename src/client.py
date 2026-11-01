import argparse
import json
import socket
import time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--count", type=int, default=4)
    args = parser.parse_args()

    for request_id in range(1, args.count + 1):
        request = {
            "request_id": request_id,
            "payload": "Hello from client"
        }
        start = time.perf_counter()
        try:
            with socket.create_connection(
                (args.host, args.port), timeout=5
            ) as sock:
                sock.settimeout(20)
                sock.sendall((json.dumps(request) + "\n").encode())
                reader = sock.makefile("r", encoding="utf-8")
                line = reader.readline()
                if not line:
                    raise ConnectionError("No response received")
                response = json.loads(line)

            latency = (time.perf_counter() - start) * 1000
            print(
                f"Request {request_id}: {response} "
                f"| latency={latency:.2f} ms"
            )
        except (OSError, ValueError, json.JSONDecodeError) as error:
            print(f"Request {request_id} failed: {error}")

if __name__ == "__main__":
    main()
