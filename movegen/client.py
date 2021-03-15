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
import random
import subprocess
import io
import socket
import chess

PARENT = os.path.dirname(os.path.realpath(__file__))
ENG_PATH = os.path.join(PARENT, "Megalodon")
TMP1 = os.path.join(PARENT, "tmp1")
TMP2 = os.path.join(PARENT, "tmp2")

BATCH_SIZE = 2
IP = input("IP: ")


def random_pos():
    moves = []
    board = chess.Board()
    movect = random.choices(range(60), weights=[1.05**x for x in range(60)])[0]

    for i in range(movect):
        legal_moves = list(board.generate_legal_moves())
        if len(legal_moves) == 0:
            break
        move = random.choice(legal_moves)
        board.push(move)
        moves.append(move)

    return (board, moves)


def send_result(moves):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((IP, 5555))

    data = " ".join([m.uci() for m in moves])
    len_msg = str(len(data))
    len_msg += " " * (64-len(len_msg))
    conn.send(len_msg.encode())
    conn.send(data.encode())

    conn.close()


def engine_output(positions):
    in_data = ""
    for board, moves in positions:
        in_data += "position startpos moves "
        for m in moves:
            in_data += m.uci() + " "
        in_data += "\nlegalmoves\n"

    with open(TMP1, "w") as file:
        file.write(in_data)
    with open(TMP1, "r") as stdin, open(TMP2, "w") as stdout:
        subprocess.Popen([ENG_PATH], stdin=stdin, stdout=stdout).wait()
    with open(TMP2, "r") as file:
        lines = file.read().split("\n")

    out_moves = []
    while len(lines) > 0:
        l = lines.pop(0)
        if l.isdigit():
            out_moves.append([lines.pop(0) for i in range(int(l))])
    return out_moves


def main():
    while True:
        positions = []
        for i in range(BATCH_SIZE):
            positions.append(random_pos())

        output = engine_output(positions)
        for board, moves in positions:
            real_moves = [m.uci() for m in board.generate_legal_moves()]
            eng_moves = output.pop(0)
            if set(real_moves) != set(eng_moves):
                send_result(moves)


main()
