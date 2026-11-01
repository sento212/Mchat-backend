import asyncio
import json
import asyncpg
import functools

async def main():
    # Connect to your PostgreSQL database (using your local tunnel port 5555)
    print("Connecting to database listener...")
    conn = await asyncpg.connect(
        user="sento",
        password="cfu800212345",
        database="mchat",
        host="localhost",
        port=5555
    )

    # Define the callback function that triggers instantly when a notification arrives
    def handle_notification(connection, pid, channel, payload, lala):
        print('pepekkkkkk')
        # The payload arrives as a JSON string from pg_notify
        data = json.loads(payload)

        print(f"Extra variable lala says: {lala}")
        
        print(f"\n[REAL-TIME ALERT] New row inserted!")
        print(f"  -> ID      : {data['id']}")

    async def hear_notif(Conn):
    # Register the listener on the 'chat_channel' channel
        my_lala_value = "Hello from the controller!"
        
        # 2. Bind lala using functools.partial before passing it to add_listener
        bound_callback = functools.partial(handle_notification, lala=my_lala_value)
        
        await Conn.add_listener('chat_channel_comvid_2026-10-09 14:32:23.407834', bound_callback)
        print("Listening for real-time inserts on 'chat_channel'... (Press Ctrl+C to exit)")

    await hear_notif(conn)

    try:
        # Keep the script running indefinitely to listen for pushes
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        pass
    finally:
        await conn.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nListener closed safely.")