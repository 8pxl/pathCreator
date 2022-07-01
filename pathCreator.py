from pynput import keyboard
from tkinter import *
import tkinter
import pyautogui as pg

# boring tkinter stuff
canvas_width = 18*40 + 200
canvas_height = 18*40 + 100
master = Tk()
master.title("g")
w = Canvas(master, width=canvas_width, height=canvas_height)
#draw field, 720 = 18in * 40
w.create_rectangle(0 + 100 ,720 + 100 ,720+50 ,0+50) 
w.pack(expand=YES, fill=BOTH)

#draws a point. does this really need a comment
def drawPoint(x,y):
    pythonGreen = "#476042"
    x1, y1 = (x - 5), (y - 5)
    x2, y2 = (x + 5), (y + 5)
    w.create_oval(x1, y1, x2, y2, width = 0, fill=pythonGreen)

#draws a line. does this really need a comment
def drawLine(p1,p2):
    w.create_line(p1[0], p1[1], p2[0], p2[1])

#list of points on the path
path = []
#list of buttons
points = []
#dwabi
replace = False
prevIndex = 0

#is called on lmb click, redraws the whole canvas, plots every point in path[]
# changes selected point when edit mode is enabeled
def createPath(event):
    w.delete("all")
    w.create_rectangle(0 + 100 ,720 + 100 ,720+50 ,0+50) 
    
    for i in range(len(points)):
        points[i].place_forget()

    x, y = (event.x), (event.y)
    global replace
    if(not replace):
        path.append((x,y))
        point = tkinter.Button(width = 2, height = 1,command = lambda t = len(path)-1: edit(t), bg= "black")
        points.append(point)
    if(replace):
        path[prevIndex] = (x,y)
        point = tkinter.Button(width = 2, height = 1,command = lambda t = len(path)-1: edit(t), bg= "black")
        points[prevIndex] = (point)
        replace = False

    # print(path)
    for i in range(len(path)):
        drawPoint(path[i][0], path[i][1])
        try:
            drawLine((path[i][0], path[i][1]), (path[i+1][0], path[i+1][1]))
        except IndexError:
            pass


            

def showPoints(event):
    for i in range(len(points)):
        points[i].place(x = path[i][0] - 10,y = path[i][1] - 10)

def edit(t):
    global prevIndex
    global replace
    prevIndex = t
    replace = True

def importPath(path):   
    for i in range(len(path)):
        drawPoint(path[i][0], path[i][1])


def export():
    name = input("path name ")
    f = open("robotics/" + name + ".cpp",'w')
    f.write("coordinate cords[] = {")
    for i in range(len(path)):
        f.write("coordinate(" + str(path[i][0]) + "," + str(path[i][1]) + "), ")
    f.write("};")
    f.close()

    f = open ("robotics/" + name +".keej", 'w')
    for i in range(len(path)):
        f.write(str(path[i]))
    f.close()


exportButton = tkinter.Button(width = 5, height = 2,command = export, bg= "black", text="export")
exportButton.place(x = 10,y = 10)

importPath(path)
w.bind("<Button-1>", createPath)
w.bind("<Button-2>", showPoints)   

# message = Label(master, text="Press and Drag the mouse to draw")
# message.pack(side=BOTTOM)
mainloop()