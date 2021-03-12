import tkinter as tk
import requests

class LeaderFollowerClient():

    # Commands
    comm = {"fw": '/forward',
            "bw": '/backward',
            "stop": '/stop',
            "l": '/left',
            "r": '/right',
            "tl": '/turnright',  # interchanged commands
            "tr": '/turnleft',
            "u": '/up',
            "d": '/down',
            "vel": '/setVelocity?',
            "pos": '/getPosition'
            }

    def __init__(self, root, geometryString, name, r1, r2):

        self.root = root
        self.name = name
        self.r1 = r1
        self.r2 = r2

        self.robotWindow = tk.Toplevel(root)
        self.robotWindow.geometry(geometryString)
        self.label = tk.Label(self.robotWindow, text="Control conjunto")
        self.label.grid(row=0, sticky="n", columnspan=3)

        self.w = 7
        self.h = 3

        self.posr1 = ["", "", ""]
        self.posr2 = ["", "", ""]

        #### Grid de botones de control ####
        self.robotFw = tk.Button(self.robotWindow, text="\u2B9D", command=self.forward)
        self.robotFw.config(height=self.h, width=self.w)
        self.robotFw.grid(row=1, column=1, columnspan=1, sticky="WE")

        self.robotL = tk.Button(self.robotWindow, text="\u2B9C", command=self.left)
        self.robotL.configure(height=self.h, width=self.w)
        self.robotL.grid(row=2, column=0, columnspan=1, sticky="WE")

        self.robotR = tk.Button(self.robotWindow, text="\u2B9E", command=self.right)
        self.robotR.configure(height=self.h, width=self.w)
        self.robotR.grid(row=2, column=2, columnspan=1, sticky="WE")

        self.robotBw = tk.Button(self.robotWindow, text="\u2B9F", command=self.backward)
        self.robotBw.configure(height=self.h, width=self.w)
        self.robotBw.grid(row=3, column=1, columnspan=1, sticky="WE")

        self.robotStop = tk.Button(self.robotWindow, text="\u23F8", command=self.stop)
        self.robotStop.configure(height=self.h, width=self.w)
        self.robotStop.grid(row=2, column=1, columnspan=1, sticky="WE")

        self.robotTl = tk.Button(self.robotWindow, text="\u2B6E", command=self.turnleft)
        self.robotTl.configure(height=self.h, width=self.w)
        self.robotTl.grid(row=3, column=2, columnspan=1, sticky="WE")

        self.robotTr = tk.Button(self.robotWindow, text="\u2B6F", command=self.turnright)
        self.robotTr.configure(height=self.h, width=self.w)
        self.robotTr.grid(row=3, column=0, columnspan=1, sticky="WE")

        self.robotUp = tk.Button(self.robotWindow, text="\u2303", command=self.up)
        self.robotUp.configure(height=self.h, width=self.w)
        self.robotUp.grid(row=1, column=2, columnspan=1, sticky="WE")

        self.robotDown = tk.Button(self.robotWindow, text="\u2304", command=self.down)
        self.robotDown.configure(height=self.h, width=self.w)
        self.robotDown.grid(row=1, column=0, columnspan=1, sticky="WE")
        #### --------------------------- ####

        ###  Slider para control de velocidad ####
        self.sliderVel = tk.Scale(self.robotWindow, from_=0, to=200, sliderlength=10, width=10,
                                  orient=tk.VERTICAL, command=self.setVelocityPctg)
        self.sliderVel.set(0)
        self.sliderVel.grid(row=1, column=4, columnspan=1, rowspan=3, sticky="NS")

        self.label2 = tk.Label(self.robotWindow, text="% Vel")
        self.label2.grid(row=0, column=4, sticky="WE", columnspan=1)
        #### --------------------------------- ####

        #### Tomar posición actual (x, y, z) ####
        self.buttonGetPos = tk.Button(self.robotWindow, text="Get Position", command=self.getPosition)
        self.buttonGetPos.grid(row=5, column=0, columnspan=4, rowspan=3, sticky="WENS")

        self.labelPosXr1 = tk.Label(self.robotWindow, text=self.posr1[0])
        self.labelPosXr1.grid(row=5, column=1, columnspan=2, sticky="W")
        self.labelPosYr1 = tk.Label(self.robotWindow, text=self.posr1[1])
        self.labelPosYr1.grid(row=6, column=1, columnspan=2, sticky="W")
        self.labelPosZr1 = tk.Label(self.robotWindow, text=self.posr1[2])
        self.labelPosZr1.grid(row=7, column=1, columnspan=2, sticky="W")

        self.labelPosXr1 = tk.Label(self.robotWindow, text=self.posr2[0])
        self.labelPosXr1.grid(row=5, column=1, columnspan=2, sticky="W")
        self.labelPosYr1 = tk.Label(self.robotWindow, text=self.posr2[1])
        self.labelPosYr1.grid(row=6, column=1, columnspan=2, sticky="W")
        self.labelPosZr1 = tk.Label(self.robotWindow, text=self.posr2[2])
        self.labelPosZr1.grid(row=7, column=1, columnspan=2, sticky="W")
        #### ------------------------------- ####

    def forward(self):
        self.r1.forward()
        self.r2.forward()

    def backward(self):
        self.r1.backward()
        self.r2.backward()

    def left(self):
        self.r1.left()
        self.r2.left()

    def right(self):
        self.r1.right()
        self.r2.right()

    def up(self):
        self.r1.up()
        self.r2.up()

    def down(self):
        self.r1.down()
        self.r2.down()

    def turnleft(self):
        self.r1.turnleft()
        self.r2.turnleft()

    def turnright(self):
        self.r1.turnright()
        self.r2.turnright()

    def stop(self):
        self.r1.stop()
        self.r2.stop()

    def setVelocityPctg(self, val):
        self.r1.setVelocityPctg(val)
        self.r2.setVelocityPctg(val)

    def getPosition(self):
        self.posr1 = self.r1.getPosition()
        self.posr2 = self.r2.getPosition()

    # TODO: Arreglar esto
    def getPosition(self):
        req = requests.get(self.url + self.comm["pos"])
        pos_json = req.json()
        self.labelPosX['text'] = "x = " + str(round(pos_json["x"], 6))
        self.labelPosY['text'] = "y = " + str(round(pos_json["y"], 6))
        self.labelPosZ['text'] = "z = " + str(round(pos_json["z"], 6))

        self.pos = (pos_json["x"], pos_json["y"], pos_json["z"])
        return self.pos