#
#  Megalodon Server
#  Server programs for decentralized computing.
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

import socket
import threading


def client(conn, addr):
    pass


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((input("IP: "), 5555))
    server.listen()
    while True:
        conn, addr = server.accept()
        threading.Thread(target=client, args=(conn, addr)).start()


main()
