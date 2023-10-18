import asyncio
import websockets


banned_words = ["Rum"]


connected_clients = {}

async def send_ban_message(websocket):
    await websocket.send("Byl jste zakázán za použití zakázaného slova.")
    await websocket.close()

async def websocket_handler(websocket, path):
    client_id = len(connected_clients) + 1
    connected_clients[client_id] = websocket

    try:
        async for message in websocket:

            if any(word in message for word in banned_words):

                await send_ban_message(websocket)
                del connected_clients[client_id]
            else:

                for recipient_id, recipient in connected_clients.items():
                    await recipient.send(f"{client_id}: {message}")

    except websockets.ConnectionClosed:
        print(f"WebSocket connection closed for client {client_id}")
        del connected_clients[client_id]

async def main():
    async with websockets.serve(websocket_handler, "127.0.0.1", 8080):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())