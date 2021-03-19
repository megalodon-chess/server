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
import threading
import time
import json
import pysocket

PARENT = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(PARENT, "data")
RESULTS_PATH = os.path.join(PARENT, "results.json")
EXE_PATH = os.path.join(PARENT, "Megalodon")
IP = input("IP: ")


def result_compile():
    with open(RESULTS_PATH, "w") as file:
        file.write("{}")


def start(self: pysocket.server.Client):
    def send_exe():
        with open(EXE_PATH, "rb") as file:
            self.send(file.read())
    def send_weights():
        with open(RESULTS_PATH, "r") as file:
            results = json.load(file)
        self.send(results)

    self.alert("Connected")
    path = os.path.join(DATA_PATH, str(time.time())+".json")
    send_exe()
    send_weights()

    while True:
        msg = self.recv()

        if msg["type"] == "quit":
            self.alert("Disconnected")
            self.conn.close()
            break

        elif msg["type"] == "result":
            data = {"option": msg["option"], "value": msg["value"], "win": msg["win"]}
            if os.path.isfile(path):
                with open(path, "r") as file:
                    curr = json.load(file)
                curr.append(data)
            else:
                curr = [data]
            with open(path, "w") as file:
                json.dump(curr, file, indent=4)

            send_exe()
            send_weights()


def main():
    threading.Thread(target=result_compile).start()
    server = pysocket.Server(IP, 5555, start, b"KWiXbMpNX3DdWW1lHa7j4TLm0oYE2FlhK6jXn0cDTbU=")
    server.start()


main()
