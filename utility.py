from diskyv2.errors import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from diskyv2.logger import *

import platform
import requests
import random
import re
import inspect
import base64
import json
import emoji
import threading
import time

class Links:
    gateway = "wss://gateway.discord.gg/?v=9&encoding=json"
    discord = "https://discord.com"

Links.api = f"{Links.discord}/api/v9"
Links.login = f"{Links.discord}/login"
Links.auth_login = f"{Links.api}/auth/login"
Links.user_me = f"{Links.api}/users/@me"
Links.experiments = f"{Links.api}/experiments"
Links.channels = f"{Links.api}/channels"

class OP:
    Identify = 2
    Heartbeat = 1
    Heartbeat_DATA = 10
    Heartbeat_ACK = 11
    Reconnect = 7
    Invalid_Session = 9

class Utility:
    @staticmethod
    def is_emoji(s):
        return s in emoji.EMOJI_DATA

    @staticmethod
    def fetch_nonce():
        return random.randint(-9223372036854775808, 9223372036854775807)

    @staticmethod
    def fetch_frame():
        frame = inspect.currentframe().f_back
        function_name = frame.f_code.co_name

        class_name = None
        if "self" in frame.f_locals:
            class_name = frame.f_locals['self'].__class__.__name__

        if class_name:
            return f"{class_name}.{function_name}"

        return function_name

    @staticmethod
    def get_os():
        os = platform.system().lower()
        if os == "darwin": os = "macos"
        return os

    @staticmethod
    def useragent(browser:str="chrome"):
        from fake_useragent import UserAgent

        return UserAgent(os=Utility.get_os()).getBrowser(browser)

    @staticmethod
    def fetch_token(session, email:str, password:str):
        request = session.post(
            Links.auth_login,
            json = {"login": email, "password": password},
            headers = {"Content-Type": "application/json"}
        )

        if request.status_code == 200:
            data = request.json()
            return data.get("token")
        else:
            raise FailedAuth()

    @staticmethod
    def token_data(session, token:str):
        request = session.get(
            Links.user_me,
            headers = {"Authorization": token}
        )

        if request.status_code == 200:
            data = request.json()
            return data
        else:
            raise FailedAuth()

    @staticmethod
    def fetch_build(session, log):
        build_num = 287665
        release_hash = "c843e820d559e1442507cb1fc1f89517be35d345"
        found_build_num = None
        found_release_hash = None

        lock = threading.Lock()

        request = session.get(
            Links.login,
            headers = {"Accept-Encoding": "identity"}
        )

        if request.status_code != 200:
            error("Failed to fetch the page. Resorting to default values.", log)
            return build_num, release_hash

        soup = BeautifulSoup(request.text, "html.parser")
        urls = [urljoin(Links.login, script.get("src")) for script in soup.find_all("script") if script.get("src")]

        def check_url(url):
            nonlocal found_build_num, found_release_hash

            build_request = session.get(
                url,
                headers={"Accept-Encoding": "identity"}
            )

            if build_request.status_code != 200:
                return None, None

            build_nums = re.findall(r'buildNumber\D+(\d+)', build_request.text)
            release_hashes = re.findall(r'release:"discord_web-([a-f0-9]+)"', build_request.text)

            if build_nums and release_hashes:
                found_build_num = build_nums[0]
                found_release_hash = release_hashes[0]

        for url in urls:
            thread = threading.Thread(target=check_url, args=(url,))
            thread.start()

        start = time.time()

        while True:
            if time.time() - start > 10:
                error("Failed to fetch Build Number and Release Hash, resorting to default values.", log)
                return build_num, release_hash
            else:
                if found_release_hash and found_build_num:
                    return found_build_num, found_release_hash

    @staticmethod
    def fetch_fingerprint(session, log):
        fingerprint = "1233073419302600705.vwGqbjW46duXfyiZmBOLAn-lk6w"

        request = session.get(
            Links.experiments
        )

        if request.status_code != 200:
            error("Failed to fetch Fingerprint, resorting to default value.", log)
            return fingerprint

        return request.json().get("fingerprint")

    @staticmethod
    def fetch_xprop(useragent, build):
        data = {
          "os": useragent["browser"],
          "browser": "Discord Client",
          "release_channel": "stable",
          "client_version": "0.0.302",
          "os_version": "23.4.0",
          "os_arch": useragent["browser"],
          "app_arch": useragent["browser"],
          "system_locale": "en-US",
          "browser_user_agent": useragent["useragent"],
          "browser_version": "28.2.10",
          "client_build_number": build,
          "native_build_number": None,
          "client_event_source": None,
          "design_id": 0
        }

        return base64.b64encode(json.dumps(data).encode("utf-8")).decode("utf-8")