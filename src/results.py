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
import json

PARENT = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(PARENT, "data")
OUT_PATH = os.path.join(PARENT, "results.json")
OPTIONS = (
    "EvalMaterial",
    "EvalCenter",
    "EvalKing",
    "EvalPawn",
    "EvalKnight",
    "EvalRook",
)


def main():
    values = {}
    for op in OPTIONS:
        values[op] = [0, 0]

    count = 0
    for file in os.listdir(DATA_PATH):
        with open(os.path.join(DATA_PATH, file), "r") as file:
            results = json.load(file)
        for data in results:
            if len(data) > 0:
                count += 1
                if data["option"] in OPTIONS:
                    num = data["white"] if data["side"] else data["black"]
                    values[data["option"]][0] += num * data["value"]
                    values[data["option"]][1] += num
    print(f"Loaded {count} matches.")

    final = {}
    for op in OPTIONS:
        points = values[op][0]
        cnt = values[op][1]
        value = points/cnt if cnt > 0 else 100
        final[op] = value
    with open(OUT_PATH, "w") as file:
        json.dump(final, file, indent=4)


main()
