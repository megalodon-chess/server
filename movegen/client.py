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

import random
import subprocess
import io
import socket
import chess

BATCH_SIZE = 100
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


def send_result():
    conn = socket.socket
    conn.connect(IP, 5555)


def main():
    board, moves = random_pos()


main()
