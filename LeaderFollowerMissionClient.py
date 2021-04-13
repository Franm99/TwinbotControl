from threading import Thread
import tkinter as tk
from Utils.PIDController import PIDController
import time


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
        self.LFWindow.title(name)
        self.label = tk.Label(self.LFWindow, text="Leader-Follower")
        self.label.grid(row=0, sticky="n", column=1, columnspan=2)

        # Gui
        self.startButton = tk.Button(self.LFWindow, text="Start", command=self.startControlFunc,
                                     width=5)
        self.startButton.grid(row=1, column=1, sticky="WE")
        self.stopButton = tk.Button(self.LFWindow, text="Stop", command=self.stopControlFunc,
                                    width=5)
        self.stopButton.grid(row=1, column=2, sticky="WE")

        self.sep1 = tk.Label(self.LFWindow, text="", width=4)
        self.sep1.grid(row=0, rowspan=6, column=0)
        self.lbl = tk.Label(self.LFWindow, text="STAGE", width=7, pady=8, relief="solid", padx=3, fg="blue")
        self.lbl.grid(row=3, column=1)
        self.lbl = tk.Label(self.LFWindow, text="STATE", width=7, pady=8, relief="solid", padx=3, fg="blue")
        self.lbl.grid(row=3, column=2)
        self.sep1 = tk.Label(self.LFWindow, text="", width=5)
        self.sep1.grid(row=2, rowspan=1, column=0, columnspan=2)
        self.lbl = tk.Label(self.LFWindow, text="Inmersing", width=7, pady=8, relief="solid", padx=3)
        self.lbl.grid(row=4, column=1)
        self.lbl = tk.Label(self.LFWindow, text="Grasping", width=7, pady=8, relief="solid", padx=3)
        self.lbl.grid(row=5, column=1)
        self.lbl = tk.Label(self.LFWindow, text="Emerging", width=7, pady=8, relief="solid", padx=3)
        self.lbl.grid(row=6, column=1)

        self.lbl1 = tk.Label(self.LFWindow, text="", width=7, pady=8, relief="solid", padx=3)
        self.lbl1.grid(row=4, column=2)
        self.lbl2 = tk.Label(self.LFWindow, text="", width=7, pady=8, relief="solid", padx=3)
        self.lbl2.grid(row=5, column=2)
        self.lbl3 = tk.Label(self.LFWindow, text="", width=7, pady=8, relief="solid", padx=3)
        self.lbl3.grid(row=6, column=2)

        self.stop = False
        self.startControl = False
        self.stopControl = False
        self.timesleep = 0.1
        self.output_lims = (-0.2, 0.2)

        Pr1 = [2 , 2 , 2 ]
        Ir1 = [0 , 0 , 0 ]
        Dr1 = [0 , 0 , 0 ]
        self.ref_r1  = [-3.2, 1.239, 15]
        self.ref2_r1 = [-3.2, 1.239, 0.3]

        Pr2 = [2, 2, 2]
        Ir2 = [0, 0, 0]
        Dr2 = [0, 0, 0]
        self.ref_r2 = [-1.733, 1.905, 15.113]
        self.ref2_r2 = [-1.733, 1.905, 0.3]

        self.pid_r1 = PIDController(Pr1, Ir1, Dr1, self.timesleep, self.output_lims)
        self.pid_r2 = PIDController(Pr2, Ir2, Dr2, self.timesleep, self.output_lims)

        # Mission parameters
        self.stage = 0
        self.grasping_time = 13.5 # 6.774 # seg
        self.error_range1 = [i * 0.01 for i in self.ref_r1]
        self.error_range2 = [i * 0.01 for i in self.ref_r2]
        self.error2_range1 = [i * 0.01 for i in self.ref2_r1]
        self.error2_range2 = [i * 0.01 for i in self.ref2_r2]

    def set_control_stage(self, ref_r1, ref_r2):
        self.pid_r1.setpoint(ref_r1)
        self.pid_r2.setpoint(ref_r2)

    def run(self):
        while (not self.stop):
            if self.startControl:
                # 1st: inmersing stage
                if self.stage == 0:
                    self.lbl1['text'] = "..."
                    self.set_control_stage(self.ref_r1, self.ref_r2)  # target position: bottom
                    actual_pos_r1 = self.r1.getPosition()
                    actual_pos_r2 = self.r2.getPosition()
                    e = [abs(self.ref_r1[2] - actual_pos_r1[2]), abs(self.ref_r2[2] - actual_pos_r2[2])]
                    while (e[0] > self.error_range1[2]) or (e[1] > self.error_range2[2]):
                        v1 = self.pid_r1(actual_pos_r1)
                        v2 = self.pid_r2(actual_pos_r2)
                        self.r1.setVelocity(v1[0], v1[1], v1[2], 0, 100)
                        self.r2.setVelocity(v2[0], v2[1], v2[2], 0, 100)
                        actual_pos_r1 = self.r1.getPosition()
                        actual_pos_r2 = self.r2.getPosition()
                        e = [abs(self.ref_r1[2] - actual_pos_r1[2]), abs(self.ref_r2[2] - actual_pos_r2[2])]
                    self.r1.setVelocity(0, 0, 0, 0, 0)
                    self.r2.setVelocity(0, 0, 0, 0, 0)
                    self.lbl1['text'] = "\u2714"
                    self.lbl1['fg'] = "green"
                    self.stage = 1

                # 2nd: grasping stage
                elif self.stage == 1:
                    self.lbl2['text'] = "..."
                    self.r1.closeG()
                    self.r2.closeG()
                    time.sleep(self.grasping_time)
                    self.r1.stopG()
                    self.r2.stopG()
                    self.lbl2['text'] = "\u2714"
                    self.lbl2['fg'] = "green"
                    self.stage = 2

                # 3rd: emerging stage
                elif self.stage == 2:
                    self.lbl3['text'] = "..."
                    self.set_control_stage(self.ref2_r1, self.ref2_r2) # target position: surface
                    actual_pos_r1 = self.r1.getPosition()
                    actual_pos_r2 = self.r2.getPosition()
                    e = [abs(self.ref2_r1[2] - actual_pos_r1[2]), abs(self.ref2_r2[2] - actual_pos_r2[2])]
                    while (e[0] > self.error2_range1[2]) or (e[0] > self.error2_range2[2]):
                        v1 = self.pid_r1(actual_pos_r1)
                        v2 = self.pid_r2(actual_pos_r2)
                        self.r1.setVelocity(v1[0], v1[1], v1[2], 0, 100)
                        self.r2.setVelocity(v2[0], v2[1], v2[2], 0, 100)
                        actual_pos_r1 = self.r1.getPosition()
                        actual_pos_r2 = self.r2.getPosition()
                        e = [abs(self.ref2_r1[2] - actual_pos_r1[2]), abs(self.ref2_r2[2] - actual_pos_r2[2])]
                    self.r1.setVelocity(0, 0, 0, 0, 0)
                    self.r2.setVelocity(0, 0, 0, 0, 0)
                    self.lbl3['text'] = "\u2714"
                    self.lbl3['fg'] = "green"
                    self.stop = True

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


