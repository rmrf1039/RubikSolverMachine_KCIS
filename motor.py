import RPi.GPIO as GPIO
import libmotor as lib
import time
    
class MotorInterpreter:
    def __init__(self):
        self.stepDelay = .00075
        
        '''
        Pin 36(U-B), 38(R-F)are direction
        '''
        
        self.M_U = lib.A4988Nema(16, 19, 26)
        self.M_B = lib.A4988Nema(16, 6, 13)
        self.M_R = lib.A4988Nema(16, 10, 25)
        self.M_L = lib.A4988Nema(20, 8, 7)
        self.M_F = lib.A4988Nema(20, 23, 24)
        self.M_D = lib.A4988Nema(20, 27, 22)
        
    def move(self, order_str, doInit=True):
        side_alp = order_str[0]
        steps_num = self.degree2step(self.determine_rotatation(order_str))
        direction = False #+
        
        if steps_num < 0:
            direction = True
        
        steps_num = int(abs(steps_num))
        
        if side_alp == 'U':
            self.M_U.rotate(direction, steps_num, self.stepDelay, False, doInit)
        elif side_alp == 'L':
            self.M_L.rotate(direction, steps_num, self.stepDelay, False, doInit)
        elif side_alp == 'F':
            self.M_F.rotate(direction, steps_num, self.stepDelay, False, doInit)
        elif side_alp == 'R':
            self.M_R.rotate(direction, steps_num, self.stepDelay, False, doInit)
        elif side_alp == 'B':
            self.M_B.rotate(direction, steps_num, self.stepDelay, False, doInit)
        else: #D
            self.M_D.rotate(direction, steps_num, self.stepDelay, False, doInit)
        
    def determine_rotatation(self, order_str):
        if len(order_str) == 2:
            if order_str[1] == "'":
                return -90
            else:
                return 180
        else:
            return 90
        
    def degree2step(self, deg):
        return deg / 1.8
    
    def initAll(self):
        time.sleep(.05)
        self.M_U.initlize()
        self.M_B.initlize()
        self.M_L.initlize()
        self.M_R.initlize()
        self.M_F.initlize()
        self.M_D.initlize()
        
        
m_interp = MotorInterpreter()
'''m_interp.initAll()


for i in range(4):
    m_interp.move("U")
    time.sleep(.5)
    m_interp.move("U'")
    
time.sleep(1)
m_interp.initAll()


for i in range(3):
    m_interp.move("U")
    m_interp.move("L")
    m_interp.move("B")
    m_interp.move("R")
    m_interp.move("F")
    m_interp.move("D")
    m_interp.move("D'")
    m_interp.move("F'")
    m_interp.move("R'")
    m_interp.move("B'")
    m_interp.move("L'")
    m_interp.move("U'")
time.sleep(1)
m_interp.initAll()
'''
