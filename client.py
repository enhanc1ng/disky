from diskyv2.objects import Event
from diskyv2.utility import Utility, Links, OP
from diskyv2.errors import *
from diskyv2.logger import *
from datetime import datetime
from colorama import Fore
from websockets.exceptions import ConnectionClosed

import diskyv2.objects
import os
import asyncio
import websockets
import json
import requests
import time
import urllib.parse
import emoji
import zlib

class Client:
    def __init__(self, token:str=None, email:str=None, password:str=None, browser:str="chrome", intents:int=16381, log_socket_to_file:bool=False, log_to_console:bool=False):
        self.token = token
        self.email = email
        self.password = password

        self.browser = browser
        self.intents = intents
        self.useragent = Utility.useragent(self.browser)
        self.websocket = None
        self.connection_data = {}
        self.client_ready = False
        self.send_ready = True

        self.log_socket_to_file = log_socket_to_file
        self.log_to_console = log_to_console

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.useragent["useragent"],
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0"
        })

        self.session.get("https://discord.com")

        self.heartbeat_interval = None
        self.user = None
        self.fingerprint = None
        self.build = None
        self.release_hash = None
        self.xproperties = None
        self.event_listener = diskyv2.objects.Listener()

        if not token:
            if not email or not password:
                raise MissingAuth()
            self.token = Utility.fetch_token(self.session, self.email, self.password)

    async def __websocket_session__(self):
        init_time = time.time()

        async with websockets.connect(Links.gateway, max_size=2 ** 24) as websocket:
            self.websocket = websocket

            await self.__connect__()

            try:
                async for message in websocket:
                    event = Event(message)

                    if event.RECONNECT:
                        info("Reconnecting..", self.log_to_console)
                        await websocket.close()

                        break

                    if event.INVALID_SESSION:
                        info("Retrying (Invalid Session)..", self.log_to_console)
                        await websocket.close()

                        break

                    if event.READY and not self.client_ready:
                        for key, value in event.data.items():
                            if key != "user":
                                continue
                            self.user = diskyv2.objects.User(**value)
                            self.client_ready = True

                        info(f"<{Fore.LIGHTBLACK_EX}{Utility.fetch_frame()}{Fore.WHITE}> Client Established within {Fore.MAGENTA}{str(time.time() - init_time)}{Fore.WHITE}ms", self.log_to_console)

                    if event.HEARTBEAT_DATA:
                        self.heartbeat_interval = event.data.get("heartbeat_interval")

                        asyncio.create_task(self.__keep_alive__())

                    if event.HEARTBEAT_ACK:
                        info("Acknowledged Heartbeat", self.log_to_console)
                        continue

                    if event.READY and self.send_ready:
                        self.send_ready = False
                        await self.event_listener.callback(event)
                    elif not event.READY:
                        await self.event_listener.callback(event)

                    if self.log_socket_to_file:
                        os.makedirs("./log", exist_ok=True)

                        filename = datetime.now().strftime("%Y%m%d%H%M%S%f") + ".json"
                        filepath = os.path.join("./log", filename)

                        with open(filepath, "w") as file:
                            json.dump(event.data, file, indent=4)
            except ConnectionClosed:
                await websocket.close()
            except Exception as error:
                raise error


    async def __connect__(self):
        self.client_ready = False
        self.send_ready = True

        if self.token:
            if not self.fingerprint:
                fingerprint = Utility.fetch_fingerprint(self.session, self.log_to_console)
                self.fingerprint = fingerprint

            if not self.xproperties:
                self.xproperties = Utility.fetch_xprop(self.useragent, self.build)
                self.session.headers.update({
                    "User-Agent": self.useragent["useragent"],
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br",
                    "DNT": "1",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                    "Cache-Control": "max-age=0",
                    "Authorization": self.token,
                    "X-Super-Properties": self.xproperties
                })

            if not self.build:
                build, release_hash = Utility.fetch_build(self.session, self.log_to_console)
                self.build = int(build)
                self.release_hash = release_hash

            info(f"<{Fore.LIGHTBLACK_EX}{Utility.fetch_frame()}{Fore.WHITE}> Fetched Browser, Device, Build, Release Hash, and X-Fingerprint")

            self.connection_data = {
                "op": OP.Identify,
                "d": {
                    "token": self.token,
                    "capabilities": self.intents,
                    "properties": {
                        "os": self.useragent["os"],
                        "browser": self.useragent["browser"],
                        "device": "",
                        "system_locale": "en-US",
                        "browser_user_agent": self.useragent["useragent"],
                        "browser_version": "124.0.0.0",
                        "os_version": "10.15.7",
                        "referrer": "",
                        "referring_domain": "",
                        "referrer_current": "",
                        "referring_domain_current": "",
                        "release_channel": "stable",
                        "client_build_number": self.build,
                        "client_event_source": None,
                        "design_id": 0
                    },
                    "presence": {
                        "status": "unknown",
                        "since": 0,
                        "activities": [],
                        "afk": False
                    },
                    "compress": False,
                    "client_state": {
                        "guild_versions": {}
                    }
                }
            }

            await self.websocket.send(json.dumps(self.connection_data))

            info(f"<{Fore.LIGHTBLACK_EX}{Utility.fetch_frame()}{Fore.WHITE}> {Fore.LIGHTYELLOW_EX}{self.connection_data}")

    async def __keep_alive__(self):
        heartbeat_data = {"op": OP.Heartbeat, "d": None}

        while True:
            await asyncio.sleep(self.heartbeat_interval / 1000)
            await self.websocket.send(json.dumps(heartbeat_data))
            info(f"<{Fore.LIGHTBLACK_EX}{Utility.fetch_frame()}{Fore.WHITE}> {Fore.LIGHTYELLOW_EX}{heartbeat_data}", self.log_to_console)

    def start(self):
        while True:
            self.client_ready = False

            try:
                loop = asyncio.get_event_loop()
                if loop.is_closed():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                loop.run_until_complete(self.__websocket_session__())
            except RuntimeError:
                asyncio.run(self.__websocket_session__())
            except:
                asyncio.run(self.__websocket_session__())

    # // @ MESSAGES
    def send_message(self, channel_id:int, content:str, flags:int=0, nonce:int=Utility.fetch_nonce(), tts:bool=False):
        return self.session.post(
            f"{Links.channels}/{str(channel_id)}/messages",
            json = {
                "content": content,
                "flags": flags,
                "nonce": nonce,
                "tts": tts
            }
        )

    def edit_message(self, channel_id:int, message_id:int, content:str):
        return self.session.patch(
            f"{Links.channels}/{str(channel_id)}/messages/{str(message_id)}",
            json = {
                "content": content
            }
        )

    def delete_message(self, channel_id:int, message_id:int):
        return self.session.delete(
            f"{Links.channels}/{str(channel_id)}/messages/{str(message_id)}"
        )

    def pin_message(self, channel_id:int, message_id:int):
        return self.session.put(
            f"{Links.channels}/{str(channel_id)}/pins/{str(message_id)}"
        )

    def unpin_message(self, channel_id:int, message_id:int):
        return self.session.delete(
            f"{Links.channels}/{str(channel_id)}/pins/{str(message_id)}"
        )

    def react_message(self, channel_id:int, message_id:int, emoji:str):
        if Utility.is_emoji(emoji):
            emoji = urllib.parse.quote(emoji)
        else:
            emoji = emoji.replace(":", urllib.parse.quote(":"))

        return self.session.put(
            f"{Links.channels}/{str(channel_id)}/messages/{str(message_id)}/reactions/{emoji}/%40me?location=Message&type=0"
        )

    def unreact_message(self, channel_id:int, message_id:int, emoji:str):
        if Utility.is_emoji(emoji):
            emoji = urllib.parse.quote(emoji)
        else:
            emoji = emoji.replace(":", urllib.parse.quote(":"))

        return self.session.delete(
            f"{Links.channels}/{str(channel_id)}/messages/{str(message_id)}/reactions/{emoji}/%40me?location=Message&burst=false"
        )

    def greet_message(self, guild_id:int, channel_id:int, message_id:int, sticker_ids:list=["749054660769218631"]):
        return self.session.post(
            f"{Links.channels}/{str(channel_id)}/greet",
            json = {
                "sticker_ids": sticker_ids,
                "message_reference": {
                    "guild_id": str(guild_id),
                    "channel_id": str(channel_id),
                    "message_id": str(message_id)
                }
            }
        )