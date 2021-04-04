import tkinter as tk
from CameraClient import CameraClient
from TwinbotClient import TwinbotClient
from LeaderFollowerClient import LeaderFollowerClient
from LeaderFollowerMissionClient import LeaderFollowerMissionClient


def execute_version(root, v=1):
    # # Main window (host) # #
    if v >= 1:
        root.geometry("50x50+10+10")
        label1 = tk.Label(root, text="MAIN WINDOW")
        label1.pack()
        buttonClose = tk.Button(root, text="CLOSE ALL", command=root.destroy)
        buttonClose.pack()

    # # Ex2: External Cameras (2 cameras) Feedback # #
        if v >= 2:
            c1 = CameraClient(root, "Girona5001 Camera", "http://127.0.0.1:8001")
            c1.cameraWindow.geometry("+10+100")
            c2 = CameraClient(root, "Girona5002 Camera", "http://127.0.0.1:8011")
            c2.cameraWindow.geometry("+10+400")
            c1.isImageColor = True
            c1.isImageColor = False
            c1.imageScalePercentage = 50
            c2.imageScalePercentage = 50

            c1.start()
            c2.start()

    # # Ex3: Cameras Feedback & 2 robots teleoperated control with tkinter # #
            if v >= 3:
                r1 = TwinbotClient(root, "294x260+420+100", "Girona5001 Control",
                                   "http://127.0.0.1:8000")
                r2 = TwinbotClient(root, "294x260+420+400", "Girona5002 Control",
                                   "http://127.0.0.1:8010")  # Leader

    # # Ex4: Cameras Feedback & 2 robot user-synchronized control with Tkinter # #
                if v >= 4:
                    lf = LeaderFollowerClient(root, "294x260+722+100", "LF Manual", r1, r2)
                    lf.start()

                    if v >= 5:
                        lfm = LeaderFollowerMissionClient(root, "294x260+722+400", "LF Mission", r1, r2)
                        lfm.start()

    print(f"TWINBOT Control Interface (v.{v})")
    root.mainloop()


if __name__ == "__main__":
    mainroot = tk.Tk()
    execute_version(mainroot, 5)
