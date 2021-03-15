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
import time
import socket
import threading

PARENT = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(PARENT, "movegen.txt")


class DataManager:
    def __init__(self):
        self.queue = []
        self.msgs = []
        self.written = 0
        threading.Thread(target=self.writer).start()

    def write(self, msg):
        self.queue.append(msg)

    def writer(self):
        while True:
            time.sleep(0.01)
            if len(self.queue) > 0:
                msg = self.queue.pop(0)
                if msg not in self.msgs:
                    with open(DATA_PATH, "a") as file:
                        file.write(msg)
                        file.write("\n")
                    self.msgs.append(msg)
                    self.written += 1

                sys.stdout.write("\r"+" "*50+"\r")
                sys.stdout.write(f"Received {self.written} failed sequences.")
                sys.stdout.flush()


def client(conn, addr, dataman):
    length = int(conn.recv(64))
    moves = conn.recv(length).decode()
    conn.close()
    dataman.write(moves)


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((input("IP: "), 5555))
    server.listen()
    dataman = DataManager()
    while True:
        conn, addr = server.accept()
        threading.Thread(target=client, args=(conn, addr, dataman)).start()


main()
