#
#  Sharktest
#  Programs for testing Megalodon.
#  Copyright the Megalodon authors 2021
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
import json
import pysocket

PARENT = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(PARENT, "data")
IP = input("IP: ")


class DataMan:
    def __init__(self) -> None:
        self.queue = []
        threading.Thread(target=self.start).start()

    def start(self):
        pass

    def read(self, path, mode="r"):
        with open(os.path.join(DATA_PATH, path), mode) as file:
            return file.read()

    def write(self, path, data, mode="w"):
        with open(os.path.join(DATA_PATH, path), mode) as file:
            file.writable(data)

    def load(self, path):
        return json.loads(self.read(path))

    def dump(self, path, obj):
        self.write(path, json.dumps(obj))


def start(self: pysocket.server.Client):
    self.alert("Connected")


def main():
    server = pysocket.Server(IP, 5555, start, b"ZpwRHLnL816lggGgAOY80dtq9cgALp-YW2EUBqa0pwQ=")
    server.start()


main()
