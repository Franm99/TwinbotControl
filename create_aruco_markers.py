# """
# JUST ONE EXECUTION IS NEEDED.
# Two png files will appear in markers directory.
# Each time you open the TWINBOT simulator, disable the aruco markers of the Girona 500 1,
# and adjust the aruco markers of the Girona 500 2 to the new ones.
# C:\Users\Usuario\Desktop\Sistemas Inteligentes UJI\Asignaturas\2o trimestre\Robótica Cooperativa\TwinbotControl\markers
# """

import cv2 as cv
import cv2.aruco as aruco

numMarkers = 2
markerSize = 4
CUSTOM_DICT = aruco.custom_dictionary(numMarkers, markerSize, 0)


def get_custom_dict():
    return CUSTOM_DICT


if __name__ == "__main__":
    pixels_per_cell = 20
    for i in range(numMarkers):
        img = aruco.drawMarker(CUSTOM_DICT, i, pixels_per_cell*(markerSize+2))
        cv.imwrite("markers/marker{:d}.png".format(i), img)