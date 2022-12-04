# Завдання 2
# Розробіть сокет-сервер на основі бібліотеки asyncio.

import asyncio

HOST = ""
PORT = 9999


async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    data = None
    while data != b"Disconnected":
        data = await reader.read(1024)  # analog of recv
        message = data.decode('utf-8')
        addr, _ = writer.get_extra_info("peername")  # something similar to parsing of server.accept

        print(f"{addr} writes: {message!r}")
        message_to_send = f"Delivery confirmation: {message!r}"

        writer.write(message_to_send.encode('utf-8'))  # analog of send
        await writer.drain()  # compulsory syntax of async write.

    print(f"{addr} disconnected.")
    asyncio.open_connection().close()


async def run_server():
    server = await asyncio.start_server(handle, HOST, PORT)  # analog of socket server.bing
    async with server:
        await server.serve_forever()  # analog of server.listen


if __name__ == '__main__':
    asyncio.run(run_server())
