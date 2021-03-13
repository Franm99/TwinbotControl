from threading import Thread
import tkinter as tk
from Utils.PIDController import PIDController
import time

# TODO: Complete interface   - Not the most important
# TODO: First mission point  - Change PID parameters
# TODO: Second mission point - Apply Time control to grid
# - Time to close grip: 6.774 seg
# TODO: Third mission point  - implement ascent
class LeaderFollowerMissionClient(Thread):

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
            "vel": '/setVelocity?'
            }

    def __init__(self, root, geometryString, name, r1, r2):
        Thread.__init__(self)

        self.root = root
        self.name = name
        self.r1 = r1
        self.r2 = r2

        self.LFWindow = tk.Toplevel(root)
        self.LFWindow.geometry(geometryString)
        self.label = tk.Label(self.LFWindow, text="Leader-Follower")
        self.label.grid(row=0, sticky="n", columnspan=1)

        self.startButton = tk.Button(self.LFWindow, text="Start", command=self.startControlFunc)
        self.startButton.grid(row=1, column=0, sticky="WE")
        self.stopButton = tk.Button(self.LFWindow, text="Stop", command=self.stopControlFunc)
        self.stopButton.grid(row=1, column=1, sticky="WE")

        self.stop = False
        self.startControl = False
        self.stopControl = False
        self.timesleep = 0.1
        self.output_lims = (-0.2, 0.2)

        Pr1 = [10, 10, 10]
        Ir1 = [0 , 0 , 0 ]
        Dr1 = [0 , 0 , 0 ]
        ref_r1 = [-3.2, 1.239, 15]  # TODO: modify (?)

        Pr2 = [2, 2, 2]
        Ir2 = [0, 0, 0]
        Dr2 = [0, 0, 0]
        ref_r2 = [-1.733, 1.905, 15.113]  # TODO: modify (?)

        self.pid_r1 = PIDController(Pr1, Ir1, Dr1, ref_r1, self.timesleep, self.output_lims)
        self.pid_r2 = PIDController(Pr2, Ir2, Dr2, ref_r2, self.timesleep, self.output_lims)

    def run(self):
        while (not self.stop):
            if self.startControl:
                actual_pos_r1 = self.r1.getPosition()
                actual_pos_r2 = self.r2.getPosition()

                v1 = self.pid_r1(actual_pos_r1)
                v2 = self.pid_r2(actual_pos_r2)

                self.r1.setVelocity(v1[0], v1[1], v1[2], 0, 100)
                self.r2.setVelocity(v2[0], v2[1], v2[2], 0, 100)

            elif self.stopControl:
                self.r1.setVelocity(0, 0, 0, 0, 0)
                self.r2.setVelocity(0, 0, 0, 0, 0)
                self.stopControl = not self.stopControl

            time.sleep(self.timesleep)

    def startControlFunc(self):
        self.startControl = True

    def stopControlFunc(self):
        self.stopControl = True
        self.startControl = False


