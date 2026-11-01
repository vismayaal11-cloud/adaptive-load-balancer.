import json
import socket
import time

HOST = "127.0.0.1"
PORT = 8000
REQUESTS = 5

def test_backend_failure():
    results = []

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
            results.append(response)

        except (OSError, ValueError) as error:
            print(f"Request {request_id} failed: {error}")
            results.append({"status": "connection_error"})

        time.sleep(0.2)

    first_failed = results[0].get("status") != "ok"
    remaining_succeeded = all(
        result.get("status") == "ok"
        and result.get("server") == "server2"
        for result in results[1:]
    )

    if first_failed and remaining_succeeded:
        print("\nFAILOVER TEST: PASS")
    else:
        print("\nFAILOVER TEST: NOT PASSED")

if __name__ == "__main__":
    test_backend_failure()
