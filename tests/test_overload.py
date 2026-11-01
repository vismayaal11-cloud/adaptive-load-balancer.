
import json
import socket
import time

HOST = "127.0.0.1"
PORT = 8000
REQUESTS = 6

def send_request(request_id):
    request = {
        "request_id": request_id,
        "payload": "overload test"
    }

    start = time.perf_counter()

    try:
        with socket.create_connection((HOST, PORT), timeout=5) as sock:
            sock.settimeout(15)
            sock.sendall((json.dumps(request) + "\n").encode())

            reader = sock.makefile("r", encoding="utf-8")
            response = json.loads(reader.readline())

        latency = (time.perf_counter() - start) * 1000
        print(
            f"Request {request_id}: "
            f"server={response.get('server')}, "
            f"status={response.get('status')}, "
            f"latency={latency:.2f} ms"
        )
        return response.get("status") == "ok"

    except (OSError, ValueError) as error:
        print(f"Request {request_id} failed: {error}")
        return False

if __name__ == "__main__":
    successful = 0

    for request_id in range(1, REQUESTS + 1):
        if send_request(request_id):
            successful += 1
        time.sleep(0.1)

    print(f"\nSuccessful requests: {successful}/{REQUESTS}")
