from threading import Thread
import time
from dataclasses import dataclass
import telnetlib
import os
from time import sleep
import re

def run(tn, command):
    try:
        cmd_s = command + "\n"
        tn.write(cmd_s.encode('utf-8'))
    except:
        print("Telnet failed to run a command!")
        pass

@dataclass
class Coords:
    x: float
    y: float
    z: float

@dataclass
class Angle:
    pitch: float
    yaw: float

def run(tn, command):
	try:
		cmd_s = command + "\n"
		tn.write(cmd_s.encode('utf-8'))
	except:
		pass

class budget_showpos():
    def __init__(self, tn):
        self.tn = tn
        self.active = False
        self.coords = Coords(0.0, 0.0, 0.0)
        self.angle = Angle(0.0, 0.0)

        t = Thread(target=self.getpos_loop, name="budget_showpos.getpos_loop()")
        t.start()

        t2 = Thread(target=self.showpos_loop, name="budget_showpos.showpos_loop()")
        t2.start()

    def print_setup(self):
        run(self.tn, "developer -1; con_filter_enable 2; con_filter_text \"‎\"")

    def getpos_loop(self):
        while True:
            if self.active:
                run(self.tn, "spec_pos")
            sleep(0.01)

    def showpos_loop(self):
        while True:
            try:
                result = self.tn.expect([b"\r\n"])
                lines = result[2].decode("utf-8").splitlines()
                line = lines[len(lines) - 1]

                if ("!showpos" in line):
                    self.active = not self.active
                    if self.active:
                        self.print_setup()
                        print(f"showpos turned on!")
                    else:
                        print(f"showpos turned off!")

                if (re.match(r"^(-?[0-9]{1,10}\.[0-9]{1}[ ]?){5}$", line) and self.active):
                    posAndAngle = line.split()
                    self.coords.x = float(posAndAngle[0])
                    self.coords.y = float(posAndAngle[1])
                    self.coords.z = float(posAndAngle[2])

                    self.angle.pitch = float(posAndAngle[3])
                    self.angle.yaw = float(posAndAngle[4])

                    run(self.tn, f"clear;" +
                        f"echo \"‎pos: {self.coords.x:0.1f} {self.coords.y:0.1f} {self.coords.z:0.1f}\"" +
                        f"\"‎ang: {self.angle.pitch:0.1f} {self.angle.yaw:0.1f}\"")
            except Exception as e:
                sleep(0.1)
                pass

def main():
    os.system('cls')
    print(f"Make sure to add -netconport 2121 to your launch options!\n")
    print(f"Connecting to: 127.0.0.1:2121")
    while True:
        try:
            tn = telnetlib.Telnet("127.0.0.1", "2121")
            break
        except ConnectionRefusedError:
            sleep(3)
            pass
    print(f"Successfully Connected!")
    print(f"type !showpos in console to toggle the showpos")
    budget_showpos(tn)

main()