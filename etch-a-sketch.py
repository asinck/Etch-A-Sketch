#!/usr/bin/env python
#Adam Sinck

#this is a list of import commands. If the user doesn't have Tkinter
#or other libraries installed, it will fail gracefully instead of
#crashing.
imports = [
    "from Tkinter import *",
    "import Tkinter as tk",
    "import serial",
]
#failedPackages will keep a record of the names of the packages that
#failed to import, so that the program can go through the entire list
#of packages that it wants to import. This will allow the program to
#give the user a complete list of packages that they need to install,
#instead of only telling the user one at a time.
failedPackages = ''
for i in imports:
    try:
        exec(i)
    except ImportError as error:
        failedPackages += str(error) + '\n'
#if there were any errors in the imports, tell the user what packages
#didn't import, and exit.
if len(failedPackages) > 0:
    print "Some packages could not be imported:"
    print failedPackages
    exit()

port = raw_input("What is the address of the arduino (ie, /dev/ttyACM0 )?  ")

ser = None

try:
    ser = serial.Serial(port, 9600)
except:
    print "Error: Could not connect to arduino."
    exit(1)

x = 0
y = 0
z = 0

max_move = 500.0
base_speed = 5.0 #px / iteration
delay = 10 #time per iteration

#this is for blanking it
def resetEasel():
    global easel
    if (easel != None):
        easel.pack_forget()
    easel = Canvas(mainFrame, width = easel_width, height = easel_height, bg = "#999")
    easel.pack(fill=BOTH, expand=YES)


#this takes a reading from the joystick, and draws
def draw():
    global x, y, delay, base_speed
    newx, newy, newz = (0, 0, 1)
    position = ser.readline().strip().split()
    print "pos: ", position
    try:
        newx, newy, newz = (float(i) for i in position)
        
        if (newz == 0): #if it's pressed
            resetEasel()
        else:
            newx = (newx / max_move) * base_speed
            newy = (newy / max_move) * base_speed
            
    except:
        newx = 0
        newy = 0

    newx, newy, newz = int(newx), int(newy), int(newz)
    print "(%d, %d, %d)" %(newx, newy, newz)
    print x, y
    easel.create_line(x, y, x+newx, y+newy)

    # x += 1
    # y += 2
    x += newx
    y += newy

    #bound checking
    if (x < 0):
        x = 0
    elif (x > easel_width):
        x = easel_width

    if (y < 0):
        y = 0
    elif (y > easel_height):
        y = easel_height

    root.after(delay, draw)


easel_width = 500;
easel_height = 500;

root = Tk()
root.title("Etch A Sketch")

mainFrame = Frame(root)

easel = None

resetEasel()

mainFrame.pack(fill=BOTH, expand=YES)
easel.pack(fill=BOTH, expand=YES)


root.after(0, draw)

root.mainloop()
