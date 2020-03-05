"""
This example shows how to use the WiFi connection to connect to
a websocket chat server and listen for messages and send messages
from the the local user.

This example makes use of cooperative multitasking via Python's
asyncio package. This is required so that both a message listener
and an input listener can run at the same time.
"""

import json
import sys
import uasyncio as asyncio
import uselect as select

from uwebsockets import client


loop = asyncio.get_event_loop()


async def ainput(prompt=""):
    """This method implements an asyncronous version of Python's
    builtin input() function. It watches the sys.stdin buffer to
    see if there is data available. If so, it reads it. If the
    character is a newline, the built string is returned.

    The sys.stdout.write() calls are required so that whatever
    application is attached to the REPL can see the characters
    that the user is typing.
    """

    sys.stdout.write(prompt)
    input_text = ""
    while True:
        while select.select([sys.stdin], [], [], 0.01)[0]:
            char = sys.stdin.read(1)
            if char == '\n':
                sys.stdout.write('\n')
                return input_text
            else:
                sys.stdout.write(char)
                input_text += char
        await asyncio.sleep(0.01)


async def connect_and_listen():
    """This method connects to the chat server. It asks the user
    to provide a name that their messages will be tagged with.
    Then it will start listening for both incoming and outgoing
    messages.
    """

    websocket = await client.connect("ws://192.168.1.9:5000")
    username = await ainput("What username do you want? ")
    await websocket.send(json.dumps({"join": username}))

    # wait for the server header message then start chatting
    loop.call_later(1, chat(username, websocket))

    # now print any incoming messages
    while True:
        print(await websocket.recv())


async def chat(username, websocket):
    """This function listens to the user typing a message on
    the REPL. After it gets one, it will send it to the server
    to be processed and then redisplay the prompt. If the user
    wants to quit the application, they can type "exit" or "quit".
    """

    while True:
        msg = await ainput("> ")
        if msg.lower() in ["exit", "quit"]:
            await websocket.send(json.dumps({"leave": username}))
            websocket.close()
            print("Bye for now")
            sys.exit(0)
        elif msg:        
            await websocket.send(json.dumps({"name": username, "message": msg}))
            print("%s: %s" % (username, msg))
        await asyncio.sleep(.01)


# start the event loop and schedule the main coroutine to run
loop.create_task(connect_and_listen())
loop.run_forever()
