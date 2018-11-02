# UDP-Ping
A ping application that we construct using UDP sockets

# Process Description:
  - Server creates a UDP socket (bound to 50007), waits for messages from client
  - Client opens a socket, sends a short message to server -> echoed back to client
  - Client records time elapsed from the message being sent to being received back
  - Process occurs 10 times
