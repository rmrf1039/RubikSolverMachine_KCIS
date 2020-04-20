#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import exit as Die
try:
    import sys
    
    from video import webcam
    from motor import m_interp
except ImportError as err:
    Die(err)

if __name__ == '__main__':
    algorithm = webcam.scan()
    length = len(algorithm.split(' '))
    
    print('-- SOLUTION --')
    print(algorithm, '({0} moves)'.format(length))
    
    for step in algorithm.split(' '):
        m_interp.move(step, doInit=False)
        
    m_interp.initAll()

    Die(0)
