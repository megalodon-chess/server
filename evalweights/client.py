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

import sys
import os
import random
import socket
import chess
import chess.engine

PARENT = os.path.dirname(os.path.realpath(__file__))
ENG_PATH = os.path.join(PARENT, "Megalodon")

PARAMS = (
    "EvalCenter",
)
BATCH_SIZE = 50
DEPTH = 3
ALG = "DFS"


def rand_configure(engine, weights):
    for i in range(len(PARAMS)):
        engine.configure({PARAMS[i]: weights[i]})
    return engine


def play_games():
    weights = [random.randint(0, 1000) for i in PARAMS]
    results = {"weights": {}, "results": []}
    for i in range(len(PARAMS)):
        results["weights"][PARAMS[i]] = weights[i]

    for i in range(BATCH_SIZE):
        white = chess.engine.SimpleEngine.popen_uci(ENG_PATH)
        black = chess.engine.SimpleEngine.popen_uci(ENG_PATH)
        white.configure({"SearchDepth": DEPTH})
        black.configure({"SearchDepth": DEPTH})
        white.configure({"SearchAlg": ALG})
        black.configure({"SearchAlg": ALG})
        if random.random() < 0.5:
            white = rand_configure(white, weights)
        else:
            black = rand_configure(black, weights)

        board = chess.Board()
        while not board.is_game_over():
            result = white.play(board, chess.engine.Limit(depth=DEPTH))
            board.push(result.move)
            result = black.play(board, chess.engine.Limit(depth=DEPTH))
            board.push(result.move)

        result = board.result()
        if result == "0-1":
            results["results"].append(-1)
        elif result == "1/2-1/2":
            results["results"].append(0)
        elif result == "1-0":
            results["results"].append(1)

    return results


def main():
    while True:
        results = play_games()


main()
