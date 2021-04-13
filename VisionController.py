from threading import Thread
from Utils.PIDController import PIDController
import tkinter as tk

class VisionController(Thread):
    def __init__(self, root, geometryString, name, ref_area, ref_x, ref_y):
        Thread.__init__(self)
        self.ref_area = ref_area
        self.ref_x = ref_x
        self.ref_y = ref_y
        self.stop = False
        self.allowVisionControl = True

        # Control parameters
        P = [2, 2, 2]
        I = [0, 0, 0]
        D = [0, 0, 0]
        self.timesleep = 0.1
        self.output_lims = (-0.2, 0.2)
        self.pid = PIDController(P, I, D, self.timesleep, self.output_lims)

        self.pid.setpoint((self.ref_area, self.ref_x, self.ref_y))

        # GUI
        self.startControl = tk.Button()


    # def run(self):
    #     while (not self.stop):
    #         if self.allowVisionControl:
    #             area =




