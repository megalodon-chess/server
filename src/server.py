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
import time
import threading
import random
import string
import json
import pysocket
from datetime import datetime
from hashlib import sha256
from captcha.image import ImageCaptcha

PARENT = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(PARENT, "data")
with open(os.path.join(PARENT, "settings.json"), "r") as file:
    data = json.load(file)
IP = data["ip"]
PORT = data["port"]
ENC_KEY = data["enc_key"].encode()
RESULT_INC = 10
TEST_THRES = 10


def resultcomp(dataman: pysocket.DataMan):
    if not dataman.isfile("results.json"):
        dataman.dump({}, "results.json")

    options = dataman.load("datafiles/options.json")
    while True:
        time.sleep(60*RESULT_INC)
        if len(dataman.listdir("results")) > 0:
            results = {opt: [] for opt in options}
            for file in dataman.listdir("results"):
                for result in dataman.load(f"results/{file}"):
                    results[result["opt"]].append((result["value"], result["win"]))

            final = dataman.load("results.json")
            for key in results:
                curr_results = results[key]
                if len(curr_results) > TEST_THRES:
                    best = best_val(curr_results, options[key]["min"], options[key]["max"])
                    final[key] = best
            dataman.dump(final, "results.json")


def best_val(results, least, greatest):
    best_score = float("-inf")
    best = least
    for i in range(least, greatest+1):
        sc = score(i, results)
        if sc > best_score:
            best_score = sc
            best = i
    return best


def score(val, results):
    sc = 0
    for v, win in results:
        if win:
            sc -= abs(v-val)
        else:
            sc += abs(v-val)
    return sc


def queue(dataman: pysocket.DataMan):
    if not dataman.isfile("stats.json"):
        dataman.dump({"total_requests": 0, "clients": {}, "conns": {}}, "stats.json")

    while True:
        time.sleep(0.01)

        if len(dataman.queue) > 0:
            cmd = dataman.queue.pop(0)

            if cmd["type"] == "request":
                data = dataman.load("stats.json")
                data["total_requests"] += 1
                if cmd["ip"] in data["clients"]:
                    data["clients"][cmd["ip"]]["requests"] += 1
                else:
                    data["clients"][cmd["ip"]] = {"requests": 1, "games": 0, "keys": 0}
                dataman.dump(data, "stats.json")

            elif cmd["type"] == "newkey":
                data = dataman.load("stats.json")
                if cmd["ip"] in data["clients"]:
                    data["clients"][cmd["ip"]]["keys"] += 1
                dataman.dump(data, "stats.json")

            elif cmd["type"] == "gameresult":
                data = dataman.load("stats.json")
                if cmd["ip"] in data["clients"]:
                    data["clients"][cmd["ip"]]["games"] += 1
                dataman.dump(data, "stats.json")

                data = dataman.load("keys/{}.json".format(cmd["key"]))
                data["used"] += 1
                dataman.dump(data, "keys/{}.json".format(cmd["key"]))

                path = "results/{}.json".format(cmd["ip"])
                if not dataman.isfile(path):
                    dataman.dump([], path)
                data = dataman.load(path)
                data.append({"opt": cmd["opt"], "value": cmd["value"], "win": cmd["win"], "time": time.time()})
                dataman.dump(data, path)

            elif cmd["type"] == "newconn":
                data = dataman.load("stats.json")
                if cmd["ip"] in data["conns"]:
                    data["conns"].pop(cmd["ip"], None)
                data["conns"][cmd["ip"]] = {"time_start": time.time(), "date_start": datetime.now().strftime("%m-%d-%Y %H-%M-%S")}
                dataman.dump(data, "stats.json")

            elif cmd["type"] == "rmconn":
                data = dataman.load("stats.json")
                data["conns"].pop(cmd["ip"], None)
                dataman.dump(data, "stats.json")


def start(self: pysocket.ServerClient, dataman: pysocket.DataMan):
    self.alert("Connected")
    dataman.queue.append({"type": "newconn", "ip": self.addr[0]})

    while True:
        time.sleep(0.1)
        msg = self.recv()
        dataman.queue.append({"type": "request", "ip": self.addr[0]})

        if msg["type"] == "quit":
            dataman.queue.append({"type": "rmconn", "ip": self.addr[0]})
            self.quit()
            self.alert("Disconnected")
            break

        elif msg["type"] == "isready":
            self.send({"ready": True})

        elif msg["type"] == "keyinfo":
            if dataman.isfile("keys/{}.json".format(msg["key"])):
                data = dataman.load("keys/{}.json".format(msg["key"]))
                self.send({"exists": True, "used": data["used"], "limit": data["limit"], "you_own": data["ip_create"] == self.addr[0]})
            else:
                self.send({"exists": False})

        elif msg["type"] == "newkey":
            font = os.path.join(DATA_PATH, "datafiles", "font.ttf")
            captcha = ImageCaptcha(fonts=[font], width=640, height=240)
            text = "".join(random.choices(string.ascii_lowercase, k=6))
            data = captcha.generate(text).read()
            self.send(data)
            reply = self.recv()
            if reply == text:
                key = "".join(random.choices("0123456789abcdef", k=16))
                while dataman.isfile(f"keys/{key}.json"):
                    key = "".join(random.choices("0123456789abcdef", k=16))
                dataman.dump({"key": key, "used": 0, "limit": 1000, "ip_create": self.addr[0]}, f"keys/{key}.json")
                self.send({"success": True, "key": key})
                dataman.queue.append({"type": "newkey", "ip": self.addr[0]})
            else:
                self.send({"success": False})

        elif msg["type"] == "getexe":
            if dataman.isfile("datafiles/Megalodon") and dataman.isfile("datafiles/options.json"):
                data = dataman.read("datafiles/Megalodon", mode="rb")
                digest = sha256(data).hexdigest()
                options = dataman.load("datafiles/options.json")
                results = dataman.load("results.json")
                for key in results:
                    options[key]["default"] = results[key]
                self.send({"success": True, "exe": data, "digest": digest, "options": options})
            else:
                self.send({"success": False})

        elif msg["type"] == "result":
            data = dataman.load("keys/{}.json".format(msg["key"]))
            if data["used"] < data["limit"]:
                dataman.queue.append({"type": "gameresult", "key": msg["key"], "opt": msg["opt"],
                    "value": msg["value"], "win": msg["win"], "ip": self.addr[0]})
                self.send({"success": True})
            else:
                self.send({"success": False})


def main():
    os.makedirs(DATA_PATH, exist_ok=True)


    dataman = pysocket.DataMan(DATA_PATH)
    dataman.makedirs("keys", True)
    dataman.makedirs("results", True)
    threading.Thread(target=resultcomp, args=(dataman,)).start()
    threading.Thread(target=queue, args=(dataman,)).start()

    server = pysocket.Server(IP, PORT, start, ENC_KEY, args=(dataman,))
    server.start()


main()
