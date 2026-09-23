"""A one-client TCP reverse-echo server for CS 6027."""

import socket


HOST = "0.0.0.0"  # Listen on all network interfaces for another machine.
PORT = 5001
BUFFER_SIZE = 1024


def main():
    try:
        # Create an IPv4 TCP socket. Context managers close the sockets.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((HOST, PORT))
            server.listen(1)
            print(f"Server listening on port {PORT}...")

            # Accept exactly one client connection.
            connection, address = server.accept()
            with connection:
                print(f"Client connected from {address}")

                # TCP is a byte stream. A newline marks each complete message.
                # Buffered reads handle messages split across TCP packets.
                with connection.makefile("rb", buffering=BUFFER_SIZE) as incoming:
                    while True:
                        data = incoming.readline()
                        if not data:
                            break  # The client closed its connection.
                        if not data.endswith(b"\n"):
                            break  # The client disconnected mid-message.

                        message = data[:-1].decode("utf-8")
                        print(f"Received: {message}")

                        # Reverse the string and send the complete response.
                        response = message[::-1]
                        connection.sendall((response + "\n").encode("utf-8"))
                        print(f"Sent: {response}")

                        if message == "fin":
                            break  # Send nif first, then close and terminate.
    except (OSError, UnicodeError) as error:
        print(f"Server error: {error}")
    except KeyboardInterrupt:
        print("\nServer interrupted.")
    finally:
        print("Server shutting down.")


if __name__ == "__main__":
    main()
