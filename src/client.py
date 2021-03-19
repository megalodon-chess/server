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
GAME_CNT = 10
DEPTH = 4


def play_games(option, value, side):
    print(f"    Tested option: {option}")
    print(f"    New value: {value}")
    print("    Tested side: {}".format("White" if side else "Black"))

    white = 0
    black = 0
    draw = 0

    for game in range(GAME_CNT):
        try:
            print(f"Playing game {game+1}: ", end="", flush=True)
            white = chess.engine.SimpleEngine.popen_uci(EXE_PATH)
            black = chess.engine.SimpleEngine.popen_uci(EXE_PATH)
            if side:
                white.configure({option: value})
            else:
                black.configure({option: value})

            board = chess.Board()
            for i in range(2):
                board.push(random.choice(list(board.generate_legal_moves())))

            move_num = 0
            while not board.is_game_over():
                move_num += 1
                sys.stdout.write("\r"+" "*60+"\r")
                sys.stdout.write(f"Playing game {game+1}: Move {move_num}")
                sys.stdout.flush()

                try:
                    board.push(white.play(board, chess.engine.Limit(depth=DEPTH)).move)
                    board.push(black.play(board, chess.engine.Limit(depth=DEPTH)).move)
                except chess.engine.EngineError:
                    sys.stdout.write("\r"+" "*60+"\r")
                    sys.stdout.write(f"Playing game {game+1}: Illegal move.")
                    sys.stdout.flush()
                    break

            sys.stdout.write("\r"+" "*60+"\r")
            sys.stdout.write(f"Playing game {game+1}: Finished")
            sys.stdout.flush()

            result = board.result()
            if result == "1-0":
                white += 1
            elif result == "0-1":
                black += 1
            elif result == "1/2-1/2":
                draw += 1

        except KeyboardInterrupt:
            white.close()
            black.close()
            raise KeyboardInterrupt

    print()
    return (white, black, draw)


def start(conn, options):
    match = 0

    while True:
        try:
            match += 1
            print(f"Playing games: Match {match}, {GAME_CNT} games")

            option = random.choice(options)
            value = random.randint(0, 1000)
            side = random.random() > 0.5
            white, black, draw = play_games(option, value, side)
            conn.send({"type": "results", "option": option, "value": value, "white": white, "black": black, "draw": draw})

        except KeyboardInterrupt:
            print("Terminated")
            return


def main():
    conn = pysocket.Client(IP, 5555, b"wemHc7uk4y8AKzFTzx2CvwrAfVBPtb2uQLhXLuKoDfY=")
    options = conn.recv()
    exe = conn.recv()
    with open(EXE_PATH, "wb") as file:
        file.write(exe)
    os.system(f"chmod +x {EXE_PATH}")

    start(conn, options)
    conn.send({"type": "quit"})


main()
