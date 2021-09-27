'''
    This file comprises of the code required to get the algorithm to solve the cube within 20 moves
    The different face values as selected by me were as follows:
        FRONT: green
           UP: white
        RIGHT: red
         DOWN: yellow
         LEFT: orange
         BACK: blue
'''

import cv2
import kociemba
import numpy as np
import time

'''
    Function used to create box references for each cubelet on the frame
'''
def createBoxes(frame, x, y, factor, thickness, color):
    for i in x:
        for j in y:
            rect = cv2.rectangle(frame, (i-factor, j-factor), (i+factor, j+factor), color, thickness)

def check(region):
    if(region[0] > w['lower'][0] and region[0] < w['upper'][0] and region[1] > w['lower'][1] and region[1] < w['upper'][1] and region[2] > w['lower'][2] and region[2] < w['upper'][2]):
        # print('W', end = " ")
        return "U"
    elif(region[0] > r['lower'][0] and region[0] < r['upper'][0] and region[1] > r['lower'][1] and region[1] < r['upper'][1] and region[2] > r['lower'][2] and region[2] < r['upper'][2]):
        # print('R', end = " ")
        return "R"
    elif(region[0] > g['lower'][0] and region[0] < g['upper'][0] and region[1] > g['lower'][1] and region[1] < g['upper'][1] and region[2] > g['lower'][2] and region[2] < g['upper'][2]):
        # print('G', end = " ")
        return "F"
    elif(region[0] > y['lower'][0] and region[0] < y['upper'][0] and region[1] > y['lower'][1] and region[1] < y['upper'][1] and region[2] > y['lower'][2] and region[2] < y['upper'][2]):
        # print('Y', end = " ")
        return "D"
    elif(region[0] > o['lower'][0] and region[0] < o['upper'][0] and region[1] > o['lower'][1] and region[1] < o['upper'][1] and region[2] > o['lower'][2] and region[2] < o['upper'][2]):
        # print('O', end = " ")
        return "L"
    elif(region[0] > b['lower'][0] and region[0] < b['upper'][0] and region[1] > b['lower'][1] and region[1] < b['upper'][1] and region[2] > b['lower'][2] and region[2] < b['upper'][2]):
        # print('B', end = " ")
        return "B"
    else:
        # print("-")
        return "-"


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    '''
        Replace these values with the configured values from 'setup.py' if these values show errors.
    '''
    w = {'lower': [45, 0, 108], 'upper': [179, 70, 255]} # UP
    r = {'lower': [159, 147, 89], 'upper':[179, 255, 255]} # RIGHT
    g = {'lower': [45, 86, 70], 'upper': [79, 194, 170]} # FRONT
    y = {'lower': [14, 100, 94], 'upper': [50, 255, 255]} # DOWN
    o = {'lower': [0, 150, 127], 'upper': [11, 255, 255]} # LEFT
    b = {'lower': [91, 100, 106], 'upper': [117, 230, 209]} # BACK

    faces = ["Up", "Right", "Front", "Down", "Left", "Back"]

    xAxis = [240, 340, 440]
    yAxis = [140, 240, 340]
    factor = 22
    thickness = 2
    color = (255, 255, 255)
    offset = factor - thickness

    captured = False
    counter = 0

    capturedHSV = []

    while True:
        ret, frame = cap.read()
        # frame = cv2.flip(frame, 1)
        hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height, width = frame.shape[:2]

        regions = []

        if not captured:
            createBoxes(frame, xAxis, yAxis, factor, thickness, color)

            for j in yAxis:
                for i in xAxis:
                    region = frame[j - offset:j + offset, i - offset:i + offset]
                    regions.append(region)

            '''
                Capture faces by pressing the 'A' key
                Faces to be captured in the following order:
                    Up, Right, Front, Down, Left, Back => white, red, green, yellow, orange, blue
                in this scenario
            '''
            if(cv2.waitKey(1) & 0xFF == ord('a')):
                faceValue = []
                
                for region in regions:
                    regionHSV = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
                    h, s, v = cv2.split(regionHSV)
                    h, s, v = np.average(h), np.average(s), np.average(v) 
                    faceValue.append([h, s, v])
                capturedHSV.append(faceValue)
                print("FACE CAPTURED: {}".format(faces[counter]))
                # cv2.imwrite("./" + faces[counter] + ".jpg", frame)
                counter += 1
                if(counter == 6): 
                    print("Captured all faces...")
                    captured = True
                    time.sleep(1)
                    break

            cv2.imshow('Frame', frame)
            
            # cv2.imshow('final', final)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()
    cap.release()


    ''' 
        The output will comprise of an algorithm string which when executed correctly will 
        help solve the cube. 
    '''
    print("Generating result...")
    inputString = ""
    for face in enumerate(capturedHSV):
        for region in enumerate(face):
            position = check(region)
            if(position == "-"):
                print("Fix the mask ranges and try again...")
                break
            inputString += position
        print(" ")
    if(len(inputString) == 54):
        print(inputString)
        try:
            solution = kociemba.solve(inputString)
            print(solution)
        except:
            print("Detected a bad colour, try again!")
    else: print("Could not capture all, please try again!")
