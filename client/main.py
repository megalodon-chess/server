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

import pysocket
from getpass import getpass
from hashlib import sha256

IP = input("IP address: ")


def login(conn: pysocket.Client):
    print("Please enter login information.")
    print("Please use a password that is not used for other accounts.")
    print("This will keep your password safe in the event of a data breach.")
    print("If the username does not exist, a new account will be created.")
    while True:
        uname = input("Username: ")
        pword = sha256(getpass("Password: ")).hexdigest()
        conn.send({"type": "login", "uname": uname, "pword": pword})
        reply = conn.recv()
        if reply["status"]:
            print("Successfully logged in.")
            return (uname, pword)
        else:
            print("Error: {}".format(reply["error"]))


def main():
    conn = pysocket.Client(IP, 5555, b"ZpwRHLnL816lggGgAOY80dtq9cgALp-YW2EUBqa0pwQ=")
    login_info = login(conn)


main()
