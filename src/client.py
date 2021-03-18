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

import chess
import pysocket

IP = input("IP: ")


def main():
    conn = pysocket.Client(IP, 5555, b"wemHc7uk4y8AKzFTzx2CvwrAfVBPtb2uQLhXLuKoDfY=")
    conn.send({"type": "results", "option": "asdf", "value": 2, "white": 12, "black": 12, "draw": 12})
    conn.send({"type": "quit"})


main()
