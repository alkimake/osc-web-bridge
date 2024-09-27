import asyncio
import socket
import struct
import websockets
from websockets.server import serve


# WebSocket server details
ws_ip = "0.0.0.0"
ws_port = 8765

# Multicast group details
multicast_group_ip = "224.0.0.1"  # Example multicast address
multicast_port = 5005


def listen_multicast():
    # Create the UDP socket for multicast
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Allow multiple sockets to use the same PORT number
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the server address
    sock.bind(("", multicast_port))

    # Tell the operating system to add the socket to the multicast group
    # on all interfaces
    mreq = struct.pack("4sl", socket.inet_aton(multicast_group_ip), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    return sock


async def handle_multicast(sock, websockets_clients):
    loop = asyncio.get_event_loop()
    while True:
        data, addr = await loop.sock_recvfrom(sock, 1024)
        print(f"Received multicast message: {data.decode()} from {addr}")

        # Forward the message to all connected WebSocket clients
        if websockets_clients:
            await asyncio.wait([ws.send(data.decode()) for ws in websockets_clients])


async def handle_websocket(websocket, path, websockets_clients):
    # Register the new client
    websockets_clients.add(websocket)
    try:
        async for message in websocket:
            # WebSocket clients can send messages, but we just log them
            print(f"Received WebSocket message: {message}")
    except websockets.exceptions.ConnectionClosedOK:
        print(f"WebSocket connection closed cleanly")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"WebSocket connection closed with error: {e}")
    finally:
        # Unregister the client when it disconnects
        websockets_clients.remove(websocket)


async def run_websocket_server(ws_ip, ws_port, websockets_clients):
    """
    Coroutine to run the WebSocket server.
    """
    print(f"Starting WebSocket server on ws://{ws_ip}:{ws_port}")
    async with serve(
        lambda ws, path: handle_websocket(ws, path, websockets_clients), ws_ip, ws_port
    ):
        await asyncio.Future()


async def main():
    # Set to store all connected WebSocket clients
    websockets_clients = set()

    websocket_server_task = run_websocket_server(ws_ip, ws_port, websockets_clients)

    sock = listen_multicast()
    print(f"Listening for multicast on {multicast_group_ip}:{multicast_port}")
    multicast_task = handle_multicast(sock, websockets_clients)

    await asyncio.gather(websocket_server_task, multicast_task)


asyncio.run(main())
