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

import sys
import os
import random
import chess
import chess.engine
import pysocket

PARENT = os.path.dirname(os.path.realpath(__file__))
IP = input("IP: ")
EXE_PATH = os.path.join(PARENT, "Megalodon-Sharktest")
GAME_CNT = 100


def play_games(option, value, side):
    print(f"    Tested option: {option}")
    print(f"    New value: {value}")
    print("    Tested side: {}".format("White" if side else "Black"))

    for game in range(GAME_CNT):
        try:
            print(f"Playing game {game+1}: ")
            white = chess.engine.SimpleEngine.popen_uci(EXE_PATH)
            black = chess.engine.SimpleEngine.popen_uci(EXE_PATH)
            if side:
                white.configure({option: value})
            else:
                black.configure({option: value})
        except KeyboardInterrupt:
            white.quit()
            black.quit()
            raise KeyboardInterrupt


def start(options):
    match = 0

    while True:
        try:
            match += 1
            print(f"Playing games: Match {match}, {GAME_CNT} games")

            option = random.choice(options)
            value = random.randint(0, 1000)
            side = random.random() > 0.5
            play_games(option, value, side)

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
