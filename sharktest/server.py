#
#  Sharktest
#  Programs for testing Megalodon.
#  Copyright Megalodon Chess 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import os
import time
import random
import string
import json
import pysocket
from captcha.image import ImageCaptcha

PARENT = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(PARENT, "data")
with open(os.path.join(PARENT, "settings.json"), "r") as file:
    data = json.load(file)
IP = data["ip"]
PORT = data["port"]
ENC_KEY = data["enc_key"].encode()


def start(self: pysocket.ServerClient, dataman: pysocket.DataMan):
    self.alert("Connected")

    while True:
        time.sleep(0.1)
        msg = self.recv()

        if msg["type"] == "quit":
            self.quit()
            self.alert("Disconnected")
            break

        elif msg["type"] == "isready":
            self.send({"ready": True})

        elif msg["type"] == "keyinfo":
            if dataman.isfile("keys/{}.json".format(msg["key"])):
                data = dataman.load("keys/{}.json".format(msg["key"]))
                self.send({"exists": True, "used": data["used"], "limit": data["limit"], "you_own": data["ip_create"] == self.addr[0]})
            else:
                self.send({"exists": False})

        elif msg["type"] == "newkey":
            font = os.path.join(DATA_PATH, "font.ttf")
            captcha = ImageCaptcha(fonts=[font], width=640, height=240)
            text = "".join(random.choices(string.ascii_lowercase, k=6))
            data = captcha.generate(text).read()
            self.send(data)
            reply = self.recv()
            if reply == text:
                key = "".join(random.choices("0123456789abcdef", k=16))
                while dataman.isfile(f"keys/{key}.json"):
                    key = "".join(random.choices("0123456789abcdef", k=16))
                dataman.dump({"key": key, "used": 0, "limit": 1000, "ip_create": self.addr[0]}, f"keys/{key}.json")
                self.send({"success": True, "key": key})
            else:
                self.send({"success": False})


def main():
    os.makedirs(DATA_PATH, exist_ok=True)
    dataman = pysocket.DataMan(DATA_PATH)
    dataman.makedirs("keys", True)
    server = pysocket.Server(IP, PORT, start, ENC_KEY, args=(dataman,))
    server.start()


main()
