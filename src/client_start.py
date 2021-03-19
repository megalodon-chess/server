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
import subprocess

PARENT = os.path.dirname(os.path.realpath(__file__))
CL_PATH = os.path.join(PARENT, "client.py")
IP = input("IP: ")


def main():
    num = int(input("Number of instances: "))
    procs = []
    files = []

    for i in range(num):
        in_path = os.path.join(PARENT, f"in{i}.txt")
        out_path = os.path.join(PARENT, f"out{i}.txt")
        with open(in_path, "w") as file:
            file.write(f"{IP}\n")
            file.write("y" if i == 0 else "n")
            file.write("\n")
        fin = open(in_path, "r")
        fout = open(out_path, "w")
        proc = subprocess.Popen(["python", CL_PATH], stdin=fin, stdout=fout)
        files.append(fin)
        files.append(fout)
        procs.append(proc)
        time.sleep(0.01)

    print("Successfully started processes")
    input("Press enter to quit.")
    for p in procs:
        p.terminate()
    for f in files:
        f.close()


main()
