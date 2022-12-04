import asyncio

HOST = "127.0.0.1"
PORT = 9999


async def run_client():
    reader, writer = await asyncio.open_connection(HOST, PORT)  # analog of client.connect
    while True:
        message = input("Write your message:\n")

        if not message:
            print("End of connection.")
            writer.write("Disconnected".encode('utf-8'))
            await writer.drain()

            asyncio.open_connection().close()
            break

        writer.write(message.encode('utf-8'))
        await writer.drain()

        data = await reader.read(1024)
        rcvd_msg = data.decode('utf-8')

        print(f'Received: {rcvd_msg!r}')


if __name__ == '__main__':
    asyncio.run(run_client())
