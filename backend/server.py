import asyncio
import websockets
import threading
from current_state import State


# global variables -- I know, don't do it.
state = State()


async def run(websocket, path):
    global state

    while True:
        await websocket.send(state.jsonify())
        await asyncio.sleep(1)


def main():
    global state

    state_update = threading.Thread(target=state.update_state)
    state_update.start()

    start_server = websockets.serve(run, "127.0.0.1", 5678)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_server)
        loop.run_forever()
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        # stop background thread
        state.do_run_thread = False


if __name__ == '__main__':
    main()
