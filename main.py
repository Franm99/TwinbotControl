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
                r1 = TwinbotClient(root, "250x260+420+100", "MiniCernBot1", "http://127.0.0.1:8000")
                r2 = TwinbotClient(root, "250x260+420+400", "MiniCernBot2", "http://127.0.0.1:8010")

    # # Ex4: Cameras Feedback & 2 robot user-synchronized control with Tkinter # #
                if v >= 4:
                    lf = LeaderFollowerClient(root, "250x260+678+100", "Leader-Follower (Manual)", r1, r2)

                    if v >= 5:
                        lfm = LeaderFollowerMissionClient(root, "250x260+678+400", "LeaderFollower", r1, r2)
                        lfm.start()

    print(f"TWINBOT Control Interface (v.{v})")
    root.mainloop()

if __name__ == "__main__":

    # # Main window (host) # #
    root = tk.Tk()
    # root.geometry("50x50+10+10")
    #
    # # # Ex2: External Cameras (2 cameras) Feedback # #
    # c1 = CameraClient(root, "Girona5001 Camera", "http://127.0.0.1:8001")
    # c1.cameraWindow.geometry("+10+100")
    # c2 = CameraClient(root, "Girona5002 Camera", "http://127.0.0.1:8011")
    # c2.cameraWindow.geometry("+10+400")
    # c1.isImageColor = True
    # c1.isImageColor = False
    # c1.imageScalePercentage = 50
    # c2.imageScalePercentage = 50
    #
    # c1.start()
    # c2.start()
    #
    #
    # # # Ex3: Cameras Feedback & 2 robots teleoperated control with tkinter # #
    # r1 = TwinbotClient(root, "250x260+420+100", "MiniCernBot1", "http://127.0.0.1:8000")
    # r2 = TwinbotClient(root, "250x260+420+400", "MiniCernBot2", "http://127.0.0.1:8010")
    #
    # # # Ex4: Cameras Feedback & 2 robot user-synchronized control with Tkinter # #
    # lf = LeaderFollowerMissionClient(root, "250x260+600+100", "LeaderFollower", r1, r2)
    # lf.start()
    #
    # label1 = tk.Label(root, text="MAIN WINDOW")
    # label1.pack()
    # buttonClose = tk.Button(root, text="CLOSE ALL", command=root.destroy)
    # buttonClose.pack()

    execute_version(root, 5)
    # root.mainloop()