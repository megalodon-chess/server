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
import random
import json
import pysocket
from hashlib import sha256

PARENT = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(PARENT, "data")
IP = input("IP: ")
OPTIONS = (
    "EvalMaterial",
    "EvalCenter",
    "EvalKing",
    "EvalPawn",
    "EvalKnight",
    "EvalRook",
)


def start(self: pysocket.server.Client):
    fname = sha256(str(random.randint(0, 10000000000)+random.random()).encode()).hexdigest() + ".json"
    fname = os.path.join(DATA_PATH, fname)

    self.alert("Connected")
    self.send(OPTIONS)

    with open(fname, "w") as file:
        json.dump([], file, indent=4)

    while True:
        msg = self.recv()

        if msg["type"] == "quit":
            self.alert("Disconnected")
            self.conn.close()
            break

        elif msg["type"] == "results":
            with open(fname, "r") as file:
                curr_data = json.load(file)
            data = {"option": msg["option"], "value": msg["value"], "white": msg["white"], "black": msg["black"], "draw": msg["draw"]}
            curr_data.append(data)
            with open(fname, "w") as file:
                json.dump(curr_data, file, indent=4)


def main():
    os.makedirs(DATA_PATH, exist_ok=True)
    server = pysocket.Server(IP, 5555, start, b"wemHc7uk4y8AKzFTzx2CvwrAfVBPtb2uQLhXLuKoDfY=")
    server.start()


main()
