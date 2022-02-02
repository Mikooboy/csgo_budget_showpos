from threading import Thread
from time import sleep
from dataclasses import dataclass
import telnetlib
import os

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
    roll: float

class budget_showpos():
    def __init__(self, tn):
        self.tn = tn
        self.active = True
        self.coords = Coords(0.0, 0.0, 0.0)
        self.angle = Angle(0.0, 0.0, 0.0)

        self.print_setup()

        t = Thread(target=self.getpos_loop, name="budget_showpos.getpos_loop()")
        t.start()

        t2 = Thread(target=self.showpos_loop, name="budget_showpos.showpos_loop()")
        t2.start()

    def print_setup(self):
        run(self.tn, "developer 1; con_filter_enable 2; con_filter_text \"‎\"")

    def getpos_loop(self):
        while True:
            if self.active:
                run(self.tn, "getpos")
            sleep(0.05)

    def showpos_loop(self):
        while True:
            try:
                result = self.tn.expect([b"\r\n"])
                lines = result[2].decode("utf-8").splitlines()
                line = lines[len(lines) - 1]

                if ("!showpos" in line):
                    self.active = not self.active
                    if self.active:
                        print(f"showpos turned on!")
                    else:
                        print(f"showpos turned off!")

                if ("setpos" in line):
                    splitted = line.split(";")
                    setpos = splitted[0]
                    setang = splitted[1]

                    coords = setpos.replace("setpos ", "")
                    coords = coords.split()
                    self.coords = Coords(float(coords[0]), float(coords[1]), float(coords[2]))

                    angle = setang.replace("setang ", "")
                    angle = angle.split()
                    self.angle = Angle(float(angle[0]), float(angle[1]), float(angle[2]))

                    run(self.tn, f"clear;" +
                        f"echo \"‎pos: {self.coords.x:0.2f} {self.coords.y:0.2f} {self.coords.z:0.2f}\"" +
                        f"\"‎ang: {self.angle.pitch:0.2f} {self.angle.yaw:0.2f} {self.angle.roll:0.2f}\"")
            except Exception as e:
                print(e)
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
    budget_showpos(tn)

main()