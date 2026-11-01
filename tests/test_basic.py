
import json
import socket
import time

HOST = "127.0.0.1"
PORT = 8000

def test_basic_request():
    request = {
        "request_id": 1,
        "payload": "basic test"
    }

    start = time.perf_counter()

    try:
        with socket.create_connection((HOST, PORT), timeout=5) as sock:
            sock.settimeout(10)
            sock.sendall((json.dumps(request) + "\n").encode())

            reader = sock.makefile("r", encoding="utf-8")
            response = json.loads(reader.readline())

        latency = (time.perf_counter() - start) * 1000

        print("Response:", response)
        print(f"Latency: {latency:.2f} ms")

        assert response.get("status") == "ok"
        assert response.get("server") in ("server1", "server2")

        print("BASIC TEST: PASS")

    except Exception as error:
        print("BASIC TEST: FAIL")
        print("Reason:", error)

if __name__ == "__main__":
    test_basic_request()
