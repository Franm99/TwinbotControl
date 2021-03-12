import tkinter as tk
import requests

class TwinbotClient():

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


    def __init__(self, root, geometryString, name, url):

        self.root = root
        self.url = url

        self.robotWindow = tk.Toplevel(root)
        self.robotWindow.geometry(geometryString)
        self.robotWindow.title(name)

        self.label = tk.Label(self.robotWindow, text=url)
        self.label.grid(row=0, sticky="n", columnspan=3)

        self.w = 7
        self.h = 3

        self.pos = ["", "", ""]

        #### Grid de botones de control ####
        self.robotFw = tk.Button(self.robotWindow, text="\u2B9D", command=self.forward)
        self.robotFw.config(height=self.h, width=self.w)
        self.robotFw.grid(row=1, column=1, columnspan=1, sticky="WE")

        self.robotL  = tk.Button(self.robotWindow, text="\u2B9C", command=self.left)
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
        self.robotTl.grid(row=3, column=0, columnspan=1, sticky="WE")

        self.robotTr = tk.Button(self.robotWindow, text="\u2B6F", command=self.turnright)
        self.robotTr.configure(height=self.h, width=self.w)
        self.robotTr.grid(row=3, column=2, columnspan=1, sticky="WE")

        self.robotUp = tk.Button(self.robotWindow, text="\u2303", command=self.up)
        self.robotUp.configure(height=self.h, width=self.w)
        self.robotUp.grid(row=1, column=2, columnspan=1, sticky="WE")

        self.robotDown = tk.Button(self.robotWindow, text="\u2304", command=self.down)
        self.robotDown.configure(height=self.h, width=self.w)
        self.robotDown.grid(row=1, column=0, columnspan=1, sticky="WE")
        #### --------------------------- ####

        ####  Slider para control de velocidad ####
        self.sliderVel = tk.Scale(self.robotWindow, from_=0, to=200, sliderlength=10, width=10,
                                  orient=tk.VERTICAL, command=self.setVelocityPctg)
        self.sliderVel.set(0)
        self.sliderVel.grid(row=1, column=4, columnspan=1, rowspan=3, sticky="NS")

        self.label2 = tk.Label(self.robotWindow, text="% Z Vel")
        self.label2.grid(row=0, column=4, sticky="WE", columnspan=1)
        #### --------------------------------- ####

        #### Tomar posición actual (x, y, z) ####
        self.buttonGetPos = tk.Button(self.robotWindow, text="Get\nPos", command=self.getPosition)
        self.buttonGetPos.grid(row=5, column=0, columnspan=1, rowspan=3, sticky="WENS")

        self.labelPosX = tk.Label(self.robotWindow, text=self.pos[0])
        self.labelPosX.grid(row=5, column=1, columnspan=2, sticky="W")
        self.labelPosY = tk.Label(self.robotWindow, text=self.pos[1])
        self.labelPosY.grid(row=6, column=1, columnspan=2, sticky="W")
        self.labelPosZ = tk.Label(self.robotWindow, text=self.pos[2])
        self.labelPosZ.grid(row=7, column=1, columnspan=2, sticky="W")
        #### ------------------------------- ####

    def forward(self):
        r = requests.get(self.url + self.comm["fw"])

    def backward(self):
        requests.get(self.url + self.comm["bw"])

    def left(self):
        requests.get(self.url + self.comm["l"])

    def right(self):
        requests.get(self.url + self.comm["r"])

    def up(self):
        requests.get(self.url + self.comm["u"])

    def down(self):
        requests.get(self.url + self.comm["d"])

    def turnleft(self):
        requests.get(self.url + self.comm["tl"])

    def turnright(self):
        requests.get(self.url + self.comm["tr"])

    def stop(self):
        requests.get(self.url + self.comm["stop"])

    def setVelocityPctg(self, val):
        vel_values = "X=0&Y=0&Z=0,1&AZ=0&PERCENTAGE=" + val
        requests.get(self.url + self.comm["vel"] + vel_values)
        # http://localhost:8000/setVelocity?X=0,1&Y=0&Z=0&AZ=0&PERCENTAGE=100

    def setVelocity(self, x_vel, y_vel, z_vel, za_vel, vel_pctg):
        x_vel = -x_vel
        y_vel = -y_vel
        x_vel  = str(x_vel).replace(".", ",")
        y_vel  = str(y_vel).replace(".", ",")
        z_vel  = str(z_vel).replace(".", ",")
        za_vel = str(za_vel).replace(".", ",")
        vel_values = "X="+y_vel+"&Y="+x_vel+"&Z="+z_vel+"&AZ="+za_vel+"&PERCENTAGE="+str(vel_pctg)
        requests.get(self.url + self.comm["vel"] + vel_values)

    def getPosition(self):
        req = requests.get(self.url + self.comm["pos"])
        pos_json = req.json()
        self.labelPosX['text'] = "x = " + str(round(pos_json["x"], 6))
        self.labelPosY['text'] = "y = " + str(round(pos_json["y"], 6))
        self.labelPosZ['text'] = "z = " + str(round(pos_json["z"], 6))

        self.pos = (pos_json["x"], pos_json["y"], pos_json["z"])
        return self.pos








