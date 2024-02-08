# The Rubik Solver Machine
The program supports the machine to solve a 3x3 rubik machine. Available functions include color detection, stepper motor controlling, and the usage of Kociemba algorithm. The code is written of Python3.7 and tested in Raspberry Pi 3B+.

*You may visit my [instagram's post](https://www.instagram.com/p/CDGQNNfpWr7/) for seeing how does my machine work and the finalized product.*

### Features
1. Just one pressm then everything works automatically.
2. The progen is used to control TI's [DRV8825](http://www.ti.com/lit/gpn/drv8825) chip.
3. The camera uses Raspberry's original camera. Focus points for locating each cube cells can be altered by ajusting the x and y axises(variable *stickers\['main']*) in the **video.py**.

*The engineering notebook is included in this git. You may checkout for the technical details.*

### Warnings
1. Dependent libraries are required before running the program, such as **PiCamera** and **Adafruit Neopixel**.
2. The color detection becomes more stable and accurate if installing a [circular led ring](https://www.rhydolabz.com/images/2400.jpg) besides the camera to eliminate environmental light noise.
3. For some reasons, stepper motor won't rotate exactly 90 degrees when the machine boots in the first time. Just kill the program immediately, readjust the motor and rerun the program agiain. It should work fine. (I don't know why does the error cause.T-T)

### Credits
Thanks to [@kkoomen](https://github.com/kkoomen/qbr)'s open source code. Even though his program does not fit perfectly to my machine but still give a big fundation in this program.
