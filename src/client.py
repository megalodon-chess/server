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
import time
import random
import multiprocessing
import chess
import chess.engine
import pysocket

PARENT = os.path.dirname(os.path.realpath(__file__))
EXE_PATH = os.path.join(PARENT, "Megalodon-Sharktest")
IP = input("IP: ")
DEPTH = 4


def write(msg):
    sys.stdout.write("\r"+" "*60+"\r")
    sys.stdout.write(msg)
    sys.stdout.flush()


def play_game(path, num, options, weights):
    option = random.choice(options)
    value = random.randint(0, 200)

    white = chess.engine.SimpleEngine.popen_uci(path)
    black = chess.engine.SimpleEngine.popen_uci(path)
    white.configure(weights)
    black.configure(weights)
    side = random.random() > 0.5
    if side:
        white.configure({option: value})
    else:
        black.configure({option: value})

    board = chess.Board()
    win = False
    move_num = 0
    for i in range(2):
        board.push(random.choice(list(board.generate_legal_moves())))
    while not board.is_game_over():
        move_num += 1
        try:
            board.push(white.play(board, chess.engine.Limit(depth=DEPTH)).move)
            board.push(black.play(board, chess.engine.Limit(depth=DEPTH)).move)
        except chess.engine.EngineError:
            break
    white.close()
    black.close()

    result = board.result()
    if result == "1-0" and side == True:
        win = True
    if result == "0-1" and side == False:
        win = True

    return (option, value, win)


def start():
    conn = pysocket.Client(IP, 5555, b"KWiXbMpNX3DdWW1lHa7j4TLm0oYE2FlhK6jXn0cDTbU=")
    game_num = 0
    path = EXE_PATH + str(time.time())

    try:
        while True:
            if os.path.isfile(path):
                os.remove(path)
            with open(path, "wb") as file:
                file.write(conn.recv())
            options = conn.recv()
            weights = conn.recv()
            os.system(f"chmod +x {path}")

            game_num += 1
            option, value, win = play_game(path, game_num, options, weights)
            data = {"type": "result", "option": option, "value": value, "win": win}
            conn.send(data)

    except KeyboardInterrupt:
        os.remove(path)

    conn.send({"type": "quit"})


def main():
    cores = int(input("Number of threads: "))
    for i in range(cores):
        multiprocessing.Process(target=start).start()
        time.sleep(0.01)


main()
