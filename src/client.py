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
import chess.engine
import pysocket

PARENT = os.path.dirname(os.path.realpath(__file__))
EXE_PATH = os.path.join(PARENT, "Megalodon-Sharktest")
IP = input("IP: ")
DEPTH = 4


def play_game(options, weights):
    option = random.choice(options)
    value = random.randint(0, 200)

    white = chess.engine.SimpleEngine.popen_uci(EXE_PATH)
    black = chess.engine.SimpleEngine.popen_uci(EXE_PATH)
    side = random.random() > 0.5
    if side:
        white.configure({option: value})
    else:
        black.configure({option: value})

    board = chess.Board()
    win = False
    while not board.is_game_over():
        try:
            board.push(white.play(board, chess.engine.Limit(depth=DEPTH)).move)
            board.push(black.play(board, chess.engine.Limit(depth=DEPTH)).move)
        except chess.engine.EngineError:
            break
    result = board.result()
    if result == "1-0" and side == True:
        win = True
    if result == "0-1" and side == False:
        win = True

    return (option, value, win)


def main():
    conn = pysocket.Client(IP, 5555, b"KWiXbMpNX3DdWW1lHa7j4TLm0oYE2FlhK6jXn0cDTbU=")

    try:
        while True:
            with open(EXE_PATH, "wb") as file:
                file.write(conn.recv())
            options = conn.recv()
            weights = conn.recv()
            os.system(f"chmod +x {EXE_PATH}")

            option, value, win = play_game(options, weights)
            data = {"option": option, "value": value, "win": win}
            conn.send(data)

    except KeyboardInterrupt:
        pass

    conn.send({"type": "quit"})


main()
