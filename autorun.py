import asyncio
import websockets
import json

# Store connected clients
connected_clients = set()

async def handler(websocket, path):
    # Register the new client
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            
            # Create a response (can be customized based on the message)
            response = {
                "type": "broadcast",
                "message": f"Server says: {message}"
            }
            # Broadcast the message to all connected clients
            await broadcast(response)
    except websockets.ConnectionClosed:
        print("Client disconnected")
    finally:
        # Unregister the client when it disconnects
        connected_clients.remove(websocket)

async def broadcast(message):
    if connected_clients:  # Ensure there are clients to broadcast to
        message = json.dumps(message)
        await asyncio.wait([client.send(message) for client in connected_clients])

async def main():
    server = await websockets.serve(handler, "localhost", 8765)
    await server.wait_closed()

# Run the WebSocket server
asyncio.run(main())
