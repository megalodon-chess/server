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
import json
import pysocket

PARENT = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(PARENT, "data")
with open(os.path.join(PARENT, "settings.json"), "r") as file:
    data = json.load(file)
IP = data["ip"]
PORT = data["port"]
ENC_KEY = data["enc_key"].encode()


def start(self: pysocket.ServerClient, dataman: pysocket.DataMan):
    self.alert("Connected")


def main():
    os.makedirs(DATA_PATH, exist_ok=True)
    dataman = pysocket.DataMan(DATA_PATH)
    server = pysocket.Server(IP, PORT, start, ENC_KEY, args=(dataman,))
    server.start()


main()
