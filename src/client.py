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
import chess
import chess.engine
import pysocket

PARENT = os.path.dirname(os.path.realpath(__file__))
EXE_PATH = os.path.join(PARENT, "Megalodon")
IP = input("IP: ")


def main():
    conn = pysocket.Client(IP, 5555, b"KWiXbMpNX3DdWW1lHa7j4TLm0oYE2FlhK6jXn0cDTbU=")

    while True:
        with open(EXE_PATH, "wb") as file:
            file.write(conn.recv())
        weights = conn.recv()
        print(weights)
        break

    conn.send({"type": "quit"})


main()
