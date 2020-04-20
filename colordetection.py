#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename      : colordetection.py
# Author        : Kim K
# Created       : Tue, 26 Jan 2016
# Last Modified : Sun, 31 Jan 2016


from sys import exit as Die
try:
    import sys
except ImportError as err:
    Die(err)

class ColorDetection:

    def get_color_name(self, hsv):
        """ Get the name of the color based on the hue.

        :returns: string
        """
        (h,s,v) = hsv
        print((h,s,v))
        if (h >= 160 and h <= 180) and (s >= 180 and s <= 250):
            return 'R' #red
        elif (h >= 25 and h <= 40) and (s >= 130 and s <= 220) and (v >= 170):
            return 'D' #yellow
        elif (h >= 0 and h <= 30) and (s >= 100 and s <= 200) and (v >= 210):
            return 'L' #orange
        elif (h >= 30 and h <= 60) and (s >= 110 and s <= 200) and (v >= 150):
            return 'F' #green
        elif (h >= 90 and h <= 110) and (s > 180):
            return 'B' #blue
        elif (h >= 100 and h <= 140) and (s <= 60) and (v >= 210):
            return 'U' #white
        
        return 'U'

    def name_to_rgb(self, name):
        """
        Get the main RGB color for a name.

        :param name: the color name that is requested
        :returns: tuple
        """
        color = {
            'R'    : (0,0,255),
            'L' : (0,165,255),
            'B'   : (255,0,0),
            'F'  : (0,255,0),
            'U'  : (255,255,255),
            'D' : (0,255,255)
        }
        return color[name]

    def average_hsv(self, roi):
        """ Average the HSV colors in a region of interest.

        :param roi: the image array
        :returns: tuple
        """
        h   = 0
        s   = 0
        v   = 0
        num = 0
        for y in range(len(roi)):
            if y % 10 == 0:
                for x in range(len(roi[y])):
                    if x % 10 == 0:
                        chunk = roi[y][x]
                        num += 1
                        h += chunk[0]
                        s += chunk[1]
                        v += chunk[2]
        h /= num
        s /= num
        v /= num
        return (int(h), int(s), int(v))

ColorDetector = ColorDetection()
