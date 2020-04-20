# RubikSolverMachine
This program supports the machine to solve a 3x3 rubik machine, including color detection, stepper motor controlling, and Kociemba algorithm. The code is written of Python3.7 and tested in Raspberry Pi 3B+.

### Features
1. The program only works with Raspberry Pi 3. Some libraries are required before running the program, like PiCamera and Adafruit Neopixel.
2. The color detection becomes more stable and accurate if with a [circular led ring](https://www.rhydolabz.com/images/2400.jpg).
3. The stepper motor driver is tested with [DRV8825](http://www.ti.com/lit/gpn/drv8825), and work just fine(it is possible to fail rotate exact 90 deg.).
4. The camera is using Raspberry's original camera. You can adjust the focus points by coordinating x and y axises.
5. Everything works automatically.

### Credits
Thanks to [@kkoomen](https://github.com/kkoomen/qbr)'s program. Even though his program does not fit perfectly to my machine but still give a big fundation to this program.
