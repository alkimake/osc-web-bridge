import socket

multicast_group = '224.0.0.1'
multicast_port = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

message = "Hello, multicast world!"
sock.sendto(message.encode(), (multicast_group, multicast_port))
print(f"Sent multicast message: {message}")