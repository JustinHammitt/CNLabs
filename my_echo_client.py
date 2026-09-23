"""Run with: python3 my_echo_client.py <server-IP-or-hostname> <port>"""

import socket
import sys


BUFFER_SIZE = 1024


def main():
    # Validate the required server address and TCP port.
    if len(sys.argv) != 3 or not sys.argv[1].strip():
        print(f"Usage: python3 {sys.argv[0]} <server-IP-or-hostname> <port>")
        return 1

    host = sys.argv[1]
    try:
        port = int(sys.argv[2])
        if not 1 <= port <= 65535:
            raise ValueError
    except ValueError:
        print("Error: port must be an integer between 1 and 65535.")
        return 1

    try:
        # Create an IPv4 TCP socket and connect to the server.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((host, port))

            # Newline-delimited messages handle TCP's byte-stream behavior.
            with client.makefile("rb", buffering=BUFFER_SIZE) as incoming:
                while True:
                    message = input("Enter a message: ")
                    if message == "end":
                        message = "fin"  # Never send the word end.

                    # Encode and send one message, then wait for its response.
                    client.sendall((message + "\n").encode("utf-8"))
                    data = incoming.readline()
                    if not data or not data.endswith(b"\n"):
                        print("Server closed the connection before a complete response.")
                        return 1

                    response = data[:-1].decode("utf-8")
                    print(f"Server response: {response}")
                    if message == "fin":
                        break  # The context managers close the connection.
    except (OSError, UnicodeError) as error:
        print(f"Connection error: {error}")
        return 1
    except (EOFError, KeyboardInterrupt):
        print("\nClient shutting down.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
