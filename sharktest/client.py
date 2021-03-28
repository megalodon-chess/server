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
import json
import pysocket
import chess
import chess.engine
from hashlib import sha256
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
Tk().withdraw()

PARENT = os.path.dirname(os.path.realpath(__file__))
TIME = 1
if os.path.isfile(os.path.join(PARENT, "settings.json")):
    with open(os.path.join(PARENT, "settings.json"), "r") as file:
        data = json.load(file)
    IP = data["ip"]
    PORT = data["port"]
    ENC_KEY = data["enc_key"].encode()
else:
    print("Sharktest setup:")
    print("Edit settings in the file settings.json")
    IP = input("Server IP: ")
    PORT = int(input("Connection port: "))
    ENC_KEY = input("Encryption key: ").encode()
    with open(os.path.join(PARENT, "settings.json"), "w") as file:
        json.dump({"ip": IP, "port": PORT, "enc_key": ENC_KEY.decode()}, file, indent=4)


def write(msg):
    sys.stdout.write("\r"+" "*60+"\r")
    sys.stdout.write(msg)
    sys.stdout.flush()


def download_exe(conn):
    print("Downloading latest Megalodon build...")
    conn.send({"type": "getexe"})
    data = conn.recv()
    if data["success"]:
        print("Build hash: {}".format(data["digest"]))
        print("Options:")
        for i in data["options"]:
            print(f"- {i}")
        if sha256(data["exe"]).hexdigest() != data["digest"]:
            print("Invalid hash. Aborting.")
            return {"status": False}
        path = os.path.join(PARENT, "Megalodon-Sharktest")
        print(f"Saving executable to {path}")
        with open(path, "wb") as file:
            file.write(data["exe"])
        os.system(f"chmod +x {path}")
    else:
        print("The server encountered an error. Please try again later.")
        return {"status": False}

    return {"status": True, "options": data["options"], "path": path}


def play_games(conn, key):
    game_num = 0
    while True:
        data = download_exe(conn)
        if not data["status"]:
            break

        options = data["options"]
        side = random.random() > 0.5
        opt = random.choice(list(options.keys()))
        value = random.randint(options[opt]["min"], options[opt]["max"])
        config = {o: options[o]["default"] for o in options}
        game_num += 1
        print(f"Playing game {game_num}.")
        print(f"- Tested option: {opt}")
        print(f"- New value: {value}")

        try:
            start = time.time()
            engine = chess.engine.SimpleEngine.popen_uci(data["path"])
            board = chess.Board()
            while not board.is_game_over():
                write(f"Playing ply {len(board.move_stack)+1}.")
                engine.configure(config)
                if board.turn == side:
                    engine.configure({opt: value})
                board.push(engine.play(board, chess.engine.Limit(time=TIME)).move)
            elapse = time.time() - start
            write(f"Game finished in {len(board.move_stack)} moves. Result is {board.result()}. {elapse} seconds elapsed.")
            engine.quit()
            print()
            print()

        except KeyboardInterrupt:
            engine.close()
            raise KeyboardInterrupt


def main():
    conn = pysocket.Client(IP, PORT, ENC_KEY)
    conn.send({"type": "isready"})
    if not conn.recv()["ready"]:
        print("The server is encountering errors. Please try again later.")
        return

    try:
        if input("Do you have a sharktest key? (y/N) ").lower().strip() == "y":
            key = input("Sharktest key: ")
            conn.send({"type": "keyinfo", "key": key})
            reply = conn.recv()
            print("Key information:")
            print("- Key exists: "+str(reply["exists"]))
            if reply["exists"]:
                print("- Results uploaded: "+str(reply["used"]))
                print("- Results limit: "+str(reply["limit"]))
                print("- Results remaining: "+str(reply["limit"]-reply["used"]))
                print("- You created this key: "+str(reply["you_own"]))
                print()
            else:
                return
        else:
            print("To prevent false results, we require testers to solve a CAPTCHA.")
            input("Press enter to download and save a CAPTCHA image as PNG. Press Ctrl+C and Enter to quit.")
            conn.send({"type": "newkey"})
            data = conn.recv()
            with open(asksaveasfilename(), "wb") as file:
                file.write(data)
            text = input("Enter the letters you see: ")
            conn.send(text)
            reply = conn.recv()
            if reply["success"]:
                print("Success! Your Sharktest key is {}".format(reply["key"]))
                print("You can upload 1000 results with this key, and you will need to generate a new one after that.")
                print()
                key = reply["key"]
            else:
                print("Validation failed.")
                conn.send({"type": "quit"})
                return

        play_games(conn, key)

    except KeyboardInterrupt:
        pass

    conn.send({"type": "quit"})


main()
