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
import pysocket
import chess
import chess.engine
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
Tk().withdraw()

PARENT = os.path.dirname(os.path.realpath(__file__))
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


def play_games(conn, key, i):
    pass


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
                key = reply["key"]
            else:
                print("Validation failed.")
                conn.send({"type": "quit"})
                return

        play_games(conn, key, 0)

    except KeyboardInterrupt:
        pass

    conn.send({"type": "quit"})


main()
