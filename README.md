# CS 6027: TCP reverse echo

Requires Python 3; no third-party packages are needed.

For the lab demonstration, run the server and client on **different machines
on the same network**. Open a terminal in the folder containing the Python files.

1. On the server machine, run:

   ```sh
   python3 my_echo_server.py
   ```

   The server listens on all IPv4 interfaces on TCP port **5001** and accepts
   one client. Allow inbound TCP port 5001 through the server's firewall if needed.

2. On the client machine, use the server machine's LAN IP address or hostname:

   ```sh
   python3 my_echo_client.py 192.168.1.10 5001
   ```

   Replace `192.168.1.10` with the actual server address. On Windows, use
   `python` instead of `python3` if that is your Python command.

3. Enter messages:

   ```text
   Enter a message: GOOD
   Server response: DOOG
   Enter a message: hello
   Server response: olleh
   Enter a message: end
   Server response: nif
   ```

TCP provides the connection used to send and receive messages. Both programs
encode text as UTF-8 and append a newline to mark the end of each message,
because TCP does not preserve message boundaries. Socket file readers use a
1024-byte buffer and assemble full lines, including messages longer than the
buffer. The newline is framing and is not part of the reversed text.

Entering `end` sends `fin`; the server replies `nif` and both programs close.
Entering `fin` directly also ends the connection. Restart the server before
another demonstration. For a local check, run both programs in separate
terminals on one machine and use `127.0.0.1` as the server address.
