#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import exit as Die

try:
    import sys
    import cv2
    import numpy as np
    import board
    import neopixel
    import time
    import kociemba
    from combiner import combine
    from picamera import PiCamera
    from colordetection import ColorDetector
    from motor import m_interp
except ImportError as err:
    Die(err)


class Webcam:
    def __init__(self):
        self.cam = PiCamera()
        
        self.cube_data = {
            'U': ['U','U','U',
                   'U','U','U',
                   'U','U','U'],
            'D': ['D','D','D',
                   'D','D','D',
                   'D','D','D'],
            'F': ['F','F','F',
                   'F','F','F',
                   'F','F','F'],
            'B': ['B','B','B',
                   'B','B','B',
                   'B','B','B'],
            'L': ['L','L','L',
                   'L','L','L',
                   'L','L','L'],
            'R': ['R','R','R',
                   'R','R','R',
                   'R','R','R'],
        }
        
        self.stickers = self.get_sticker_coordinates('main')
        self.preview_stickers = self.get_sticker_coordinates('preview')
        self.led = neopixel.NeoPixel(board.D18, 24)
        self.cam_once = False

    def get_sticker_coordinates(self, name):
        stickers = {
            'main' : [[230, 90], [280, 125], [345, 165], [410, 125], [465, 100],
                      [205, 140], [255, 170], [310, 215], [310, 280], [310, 330],
                      [480, 155], [430, 180], [376, 215], [365, 280], [360, 330]],
            'preview': {
                'U': [[35, 0], [45, 0], [55, 0],
                        [35, 10], [45, 10], [55, 10],
                        [35, 20], [45, 20], [55, 20]],
                'D': [[35, 70], [45, 70], [55, 70],
                        [35, 80], [45, 80], [55, 80],
                        [35, 90], [45, 90], [55, 90]],
                'F': [[35, 35], [45, 35], [55, 35],
                        [35, 45], [45, 45], [55, 45],
                        [35, 55], [45, 55], [55, 55]],
                'B': [[105, 35], [115, 35], [125, 35],
                        [105, 45], [115, 45], [125, 45],
                        [105, 55], [115, 55], [125, 55]],
                'L': [[0, 35], [10, 35], [20, 35],
                        [0, 45], [10, 45], [20, 45],
                        [0, 55], [10, 55], [20, 55]],
                'R': [[70, 35], [80, 35], [90, 35],
                        [70, 45], [80, 45], [90, 45],
                        [70, 55], [80, 55], [90, 55]],
            }
        }
        return stickers[name]


    def draw_main_stickers(self, frame):
        i = 0

        for x,y in self.stickers:
            cv2.rectangle(frame, (x,y), (x+15, y+15), (255,255,255), 1)
            cv2.putText(frame, str(i), (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
            i+=1

    def draw_current_cubes(self, frame, state):
        for key in self.preview_stickers:
            for index,(x,y) in enumerate(self.preview_stickers[key]):
                cv2.rectangle(frame, (x,y), (x+10, y+10), ColorDetector.name_to_rgb(state[key][index]), -1)

    def get_color(self, hsv, number):
        x = self.stickers[number][0]
        y = self.stickers[number][1]
        roi = hsv[y:y+14, x:x+14]
        avg_hsv = ColorDetector.average_hsv(roi)

        return ColorDetector.get_color_name(avg_hsv)

    def get_hsv(self, hsv, number):
        x = self.stickers[number][0]
        y = self.stickers[number][1]
        roi = hsv[y:y+14, x:x+14]
        avg_hsv = ColorDetector.average_hsv(roi)

        return avg_hsv
    
    def capture(self):
        self.led.fill((255, 255, 255))
        
        self.cam.resolution = (700, 470)
        self.cam.awb_mode = 'auto'
        
        time.sleep(2)
        
        self.cam.capture('./img/view.jpg')
        self.led.fill((0, 0, 0))
        
    def scan(self):
        # mid 10 = movement, 0 = [code], 1 = [code]', 2 = [code]2
        orders = [
        ['U', 2, 0], ['U', 1, 1], ['U', 0, 2], ['U', 3, 3], ['U', 6, 4],
        ['B', 0, 5], ['B', 1, 6], ['B', 2, 7], ['B', 5, 8], ['B', 8, 9],
        ['L', 0, 12], ['L', 1, 11], ['L', 2, 10], ['L', 3, 13], ['L', 6, 14],
        ['U', 2, 99], ['U', 7, 1], ['U', 8, 2], ['U', 5, 3], ['F', 0, 5], ['F', 1, 6], ['F', 2, 7], ['R', 0, 12], ['R', 1, 11], ['R', 2, 10], ['U', 2, 98], #top finish
        ['B', 2, 99], ['B', 3, 8], ['B', 6, 7], ['B', 7, 6], ['D', 6, 0], ['D', 7, 1], ['D', 8, 2], ['R', 5, 13], ['R', 8, 12], ['B', 2, 98],
        ['L', 2, 99], ['D', 0, 2], ['D', 3, 3], ['F', 3, 8], ['F', 6, 7], ['L', 5, 13], ['L', 7, 11], ['L', 8, 12], ['L', 2, 98],
        ['F', 2, 98], ['L', 1, 99], ['F', 8, 2], ['F', 5, 3], ['R', 6, 12], ['R', 3, 11], ['D', 2, 7], ['U', 0, 99], ['F', 7, 11], ['D', 1, 3], ['U', 1, 98], ['L', 0, 98], ['F', 2, 98],
        ['R', 1, 98], ['B', 0, 98], ['U', 1, 99], ['D', 5, 11], ['R', 5, 6], ['R', 7, 3], ['R', 8, 4], ['U', 0, 98], ['B', 1, 98], ['R', 0, 98]
        ]
        
        cv2.namedWindow('Cube_Camera', cv2.WINDOW_NORMAL)
        worked_steps = 0

        self.capture()
        
        while worked_steps < len(orders):
            code = orders[worked_steps][0] #cube side
            cid = orders[worked_steps][1] #cube side id
            mid = orders[worked_steps][2] #scan point
            
            frame = cv2.imread('./img/view.jpg')
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            #self.draw_main_stickers(frame)

            if mid >= 98:
                if cid == 1:
                    m_interp.move(code + "'")
                elif cid == 2:
                    m_interp.move(code + '2')
                else:
                    m_interp.move(code)
                    
                if mid == 99:
                    self.capture()
            else:
                self.cube_data[code][cid] = self.get_color(hsv, mid)
            
            worked_steps += 1
        
        m_interp.initAll()

        #for i, (x,y) in enumerate(self.stickers):
        #    cv2.putText(frame, str(self.get_hsv(hsv, i)), (x, y+21), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (0,0,0), 1)
    
        try:
            alg = kociemba.solve(combine.sides(self.cube_data))
            
            return alg
        except Exception as err:
            print('\033[0;33m[QBR SOLVE ERROR] Ops, you did not scan in all 6 sides correctly.')
            print('Please try again.\033[0m')
            
            fiFrame = np.zeros((100, 135, 3), dtype="uint8")
            self.draw_current_cubes(frame, self.cube_data)
            cv2.imshow("Cube_Camera", frame)
            cv2.resizeWindow('Cube_Camera', 1000, 800)
            cv2.waitKey(0) & 0xff
            cv2.destroyAllWindows()
            
            Die(1)

        return False

webcam = Webcam()
