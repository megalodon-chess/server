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
import threading
import time
import json
import pysocket

PARENT = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(PARENT, "data")
RESULTS_PATH = os.path.join(PARENT, "results.json")
EXE_PATH = os.path.join(PARENT, "Megalodon")
IP = input("IP: ")
OPTIONS = (
    "EvalCenter",
    "EvalKing",
    "EvalPawn",
    "EvalKnight",
    "EvalRook",
)
COMP_INC = 600


def total_loss(results, value):
    loss = 0
    for r in results:
        if r["win"]:
            loss += 1000 - abs(value - r["value"])
        else:
            loss += abs(value - r["value"])

    return loss


def best_val(results):
    if len(results) == 0:
        return 100

    best = 0
    min_loss = float("inf")
    for i in range(1000):
        loss = total_loss(results, i)
        if loss < min_loss:
            min_loss = loss
            best = i

    return best


def result_compile():
    if not os.path.isfile(RESULTS_PATH):
        with open(RESULTS_PATH, "w") as file:
            file.write("{}")

    while True:
        print("Compiling results.")

        results = []
        for file in os.listdir(DATA_PATH):
            with open(os.path.join(DATA_PATH, file), "r") as file:
                results.extend(json.load(file))

        final = {}
        for op in OPTIONS:
            final[op] = best_val([r for r in results if r["option"] == op])
        with open(RESULTS_PATH, "w") as file:
            json.dump(final, file)

        time.sleep(COMP_INC)


def start(self: pysocket.server.Client):
    def send_exe():
        with open(EXE_PATH, "rb") as file:
            self.send(file.read())

    def send_options():
        self.send(OPTIONS)

    def send_weights():
        with open(RESULTS_PATH, "r") as file:
            results = json.load(file)
        self.send(results)

    self.alert("Connected")
    path = os.path.join(DATA_PATH, str(time.time())+".json")
    send_exe()
    send_options()
    send_weights()

    while True:
        msg = self.recv()

        if msg["type"] == "quit":
            self.alert("Disconnected")
            self.conn.close()
            break

        elif msg["type"] == "result":
            data = {"option": msg["option"], "value": msg["value"], "win": msg["win"]}
            if os.path.isfile(path):
                with open(path, "r") as file:
                    curr = json.load(file)
                curr.append(data)
            else:
                curr = [data]
            with open(path, "w") as file:
                json.dump(curr, file, indent=4)

            send_exe()
            send_options()
            send_weights()


def main():
    os.makedirs(DATA_PATH, exist_ok=True)
    threading.Thread(target=result_compile).start()
    server = pysocket.Server(IP, 5555, start, b"KWiXbMpNX3DdWW1lHa7j4TLm0oYE2FlhK6jXn0cDTbU=")
    server.start()


main()
