
import json
import socket
import time

HOST = "127.0.0.1"
PORT = 8000
REQUESTS = 5

def test_backend_failure():
    successful = 0

    for request_id in range(1, REQUESTS + 1):
        request = {
            "request_id": request_id,
            "payload": "backend failure test"
        }

        try:
            with socket.create_connection((HOST, PORT), timeout=5) as sock:
                sock.settimeout(10)
                sock.sendall((json.dumps(request) + "\n").encode())

                reader = sock.makefile("r", encoding="utf-8")
                response = json.loads(reader.readline())

            print(f"Request {request_id}: {response}")

            if response.get("status") == "ok":
                successful += 1

        except (OSError, ValueError) as error:
            print(f"Request {request_id} failed: {error}")

        time.sleep(0.2)

    print(f"\nSuccessful requests: {successful}/{REQUESTS}")

    if successful == REQUESTS:
        print("FAILURE TEST: PASS")
    else:
        print("FAILURE TEST: NOT PASSED")

if __name__ == "__main__":
    test_backend_failure()
