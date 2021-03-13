import tkinter as tk
import requests
import time

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
            "pos": '/getPosition',
            "open": '/OPEN',
            "close": '/CLOSE',
            "stopg": '/STOP'
            }

    def __init__(self, root, geometryString, name, r1, r2):

        self.root = root
        self.r1 = r1
        self.r2 = r2

        self.robotWindow = tk.Toplevel(root)
        self.robotWindow.geometry(geometryString)
        self.robotWindow.title(name)

        self.label = tk.Label(self.robotWindow, text="Group control")
        self.label.grid(row=0, sticky="n", columnspan=3)

        self.w = 7
        self.h = 3

        self.pos1 = ["", "", ""]
        self.pos2 = ["", "", ""]

        self.ts = 0
        self.te = 0

        #### Grid de botones de control ####
        self.robotDown = tk.Button(self.robotWindow, text="\u2304", command=self.down)
        self.robotDown.configure(height=self.h, width=self.w)
        self.robotDown.grid(row=1, column=0, columnspan=1, sticky="WE")

        self.robotFw = tk.Button(self.robotWindow, text="\u2B9D", command=self.forward)
        self.robotFw.config(height=self.h, width=self.w)
        self.robotFw.grid(row=1, column=1, columnspan=1, sticky="WE")

        self.robotUp = tk.Button(self.robotWindow, text="\u2303", command=self.up)
        self.robotUp.configure(height=self.h, width=self.w)
        self.robotUp.grid(row=1, column=2, columnspan=1, sticky="WE")

        self.robotL = tk.Button(self.robotWindow, text="\u2B9C", command=self.left)
        self.robotL.configure(height=self.h, width=self.w)
        self.robotL.grid(row=2, column=0, columnspan=1, sticky="WE")

        self.robotStop = tk.Button(self.robotWindow, text="\u23F8", command=self.stop)
        self.robotStop.configure(height=self.h, width=self.w)
        self.robotStop.grid(row=2, column=1, columnspan=1, sticky="WE")

        self.robotR = tk.Button(self.robotWindow, text="\u2B9E", command=self.right)
        self.robotR.configure(height=self.h, width=self.w)
        self.robotR.grid(row=2, column=2, columnspan=1, sticky="WE")

        self.robotTl = tk.Button(self.robotWindow, text="\u2B6E", command=self.turnleft)
        self.robotTl.configure(height=self.h, width=self.w)
        self.robotTl.grid(row=3, rowspan=2, column=0, columnspan=1, sticky="WENS")

        self.robotBw = tk.Button(self.robotWindow, text="\u2B9F", command=self.backward)
        self.robotBw.configure(height=self.h, width=self.w)
        self.robotBw.grid(row=3, rowspan=2, column=1, columnspan=1, sticky="WENS")

        self.robotTr = tk.Button(self.robotWindow, text="\u2B6F", command=self.turnright)
        self.robotTr.configure(height=self.h, width=self.w)
        self.robotTr.grid(row=3, rowspan=2, column=2, columnspan=1, sticky="WENS")
        #### --------------------------- ####

        self.separatorV = tk.Label(self.robotWindow, text=" ")
        self.separatorV.grid(row=0, column=4, rowspan=10)

        ###  Slider para control de velocidad ####
        self.sliderVel = tk.Scale(self.robotWindow, from_=0, to=200, sliderlength=10, width=10,
                                  orient=tk.HORIZONTAL, command=self.setVelocityPctg)
        self.sliderVel.set(0)
        self.sliderVel.grid(row=1, column=5, columnspan=2, rowspan=1, sticky="NSWE")

        self.label2 = tk.Label(self.robotWindow, text="% Z Vel")
        self.label2.grid(row=0, column=5, sticky="WE", columnspan=2)
        #### --------------------------------- ####

        #### Tomar posición actual (x, y, z) ####
        txt = "Get Position"
        self.buttonGetPos = tk.Button(self.robotWindow, text=txt, command=self.getPosition)
        self.buttonGetPos.configure(height=self.h, width=self.w*2)
        self.buttonGetPos.grid(row=2, column=5, columnspan=2, rowspan=1, sticky="WENS")

        self.labelPosr1 = tk.Label(self.robotWindow, text="")
        self.labelPosr1.config(font=('TkDefaultFont', 8))
        self.labelPosr1.grid(row=3, column=5, columnspan=2, sticky="W")

        self.labelPosr2 = tk.Label(self.robotWindow, text="")
        self.labelPosr2.config(font=('TkDefaultFont', 8))
        self.labelPosr2.grid(row=4, column=5, columnspan=2, sticky="W")

        # self.labelPosXr1 = tk.Label(self.robotWindow, text=self.pos1[0])
        # self.labelPosXr1.config(font=('TkDefaultFont', 8))
        # self.labelPosXr1.grid(row=3, column=5, columnspan=1, sticky="W")
        # self.labelPosYr1 = tk.Label(self.robotWindow, text=self.pos1[1])
        # self.labelPosYr1.config(font=('TkDefaultFont', 8))
        # self.labelPosYr1.grid(row=4, column=5, columnspan=1, sticky="W")
        # self.labelPosZr1 = tk.Label(self.robotWindow, text=self.pos1[2])
        # self.labelPosZr1.config(font=('TkDefaultFont', 8))
        # self.labelPosZr1.grid(row=5, column=5, columnspan=1, sticky="W")
        #
        # self.labelPosXr2 = tk.Label(self.robotWindow, text=self.pos2[0])
        # self.labelPosXr2.config(font=('TkDefaultFont', 8))
        # self.labelPosXr2.grid(row=3, column=6, columnspan=1, sticky="W")
        # self.labelPosYr2 = tk.Label(self.robotWindow, text=self.pos2[1])
        # self.labelPosYr2.config(font=('TkDefaultFont', 8))
        # self.labelPosYr2.grid(row=4, column=6, columnspan=1, sticky="W")
        # self.labelPosZr2 = tk.Label(self.robotWindow, text=self.pos2[2])
        # self.labelPosZr2.config(font=('TkDefaultFont', 8))
        # self.labelPosZr2.grid(row=5, column=6, columnspan=1, sticky="W")
        #### ------------------------------- ####

        self.separatorH = tk.Label(self.robotWindow, text=" ")
        self.separatorH.grid(row=6, column=0, columnspan=10)

        ### Controlar Gripper ###
        self.buttonOpenG = tk.Button(self.robotWindow, text="Open\nGripper", command=self.openG)
        self.buttonOpenG.grid(row=7, column=0, rowspan=2, sticky="NSWE")
        self.buttonCloseG = tk.Button(self.robotWindow, text="Close\nGripper", command=self.closeG)
        self.buttonCloseG.grid(row=7, column=1, rowspan=2, sticky="NSWE")
        self.buttonStopG = tk.Button(self.robotWindow, text="Stop\nGripper", command=self.stopG)
        self.buttonStopG.grid(row=7, column=2, rowspan=2, sticky="NSWE")

        self.lblTimeGripper = tk.Label(self.robotWindow, text="Time (s)")
        self.lblTimeGripper.grid(row=7, column=5, sticky="W")

        self.TimeGripper = tk.Label(self.robotWindow, text="")
        self.TimeGripper.grid(row=7, column=6, sticky="W")
        ### ----------------- ###

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
        req1 = requests.get(self.r1.url + self.comm["pos"])
        pos1_json = req1.json()
        x1 = str(round(pos1_json["x"], 3))
        y1 = str(round(pos1_json["y"], 3))
        z1 = str(round(pos1_json["z"], 3))
        self.labelPosr1['text'] = "(" + x1 + ", " + y1 + ", " + z1 + ")"
        # self.labelPosXr1['text'] = "x= " + str(round(pos1_json["x"], 3))
        # self.labelPosYr1['text'] = "y= " + str(round(pos1_json["y"], 3))
        # self.labelPosZr1['text'] = "z= " + str(round(pos1_json["z"], 3))
        self.pos1 = [pos1_json["x"], pos1_json["y"], pos1_json["z"]]

        req2 = requests.get(self.r2.url + self.comm["pos"])
        pos2_json = req2.json()
        x2 = str(round(pos2_json["x"], 3))
        y2 = str(round(pos2_json["y"], 3))
        z2 = str(round(pos2_json["z"], 3))
        self.labelPosr2['text'] = "(" + x2 + ", " + y2 + ", " + z2 + ")"
        # self.labelPosXr2['text'] = "x= " + str(round(pos2_json["x"], 3))
        # self.labelPosYr2['text'] = "y= " + str(round(pos2_json["y"], 3))
        # self.labelPosZr2['text'] = "z= " + str(round(pos2_json["z"], 3))
        self.pos2 = [pos2_json["x"], pos2_json["y"], pos2_json["z"]]

        return self.pos1, self.pos2

    def openG(self):
        self.r1.openG()
        self.r2.openG()

    def closeG(self):
        self.r1.closeG()
        self.r2.closeG()
        self.ts = time.time()

    def stopG(self):
        self.r1.stopG()
        self.r2.stopG()
        self.te = time.time() - self.ts
        self.TimeGripper['text'] = str(round(self.te, 3))
