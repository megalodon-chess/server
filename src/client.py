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
import chess
import pysocket

PARENT = os.path.dirname(os.path.realpath(__file__))
IP = input("IP: ")
EXE_PATH = os.path.join(PARENT, "Megalodon-Sharktest")
GAME_CNT = 100


def play_games(option, value):
    pass


def start(options):
    while True:
        try:
            option = random.choice(options)
            value = random.randint(0, 1000)
            play_games(option, value)
        except KeyboardInterrupt:
            print("Terminated")
            return


def main():
    conn = pysocket.Client(IP, 5555, b"wemHc7uk4y8AKzFTzx2CvwrAfVBPtb2uQLhXLuKoDfY=")
    options = conn.recv()
    exe = conn.recv()
    with open(EXE_PATH, "wb") as file:
        file.write(exe)

    start(options)
    conn.send({"type": "quit"})


main()
