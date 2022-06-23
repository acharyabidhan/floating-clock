import random
from tkinter import*
from tkinter import Canvas
import time
import pythoncom
from win32com.client import Dispatch
from os import path
app = Tk()
app.overrideredirect(True)
app.resizable(0,0)
width = 250
height = 150
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
position_top = 10
position_right = int(screen_width - (width+10))
app.geometry(f'{width}x{height}+{position_right}+{position_top}')
bgColor = "blue"
app.config(background="black")
username = (path.split(path.expanduser('~'))[-1])
appName = "floating-clock"
appFolder = f"C:\\bidhanInc\\{appName}"
pythoncom.CoInitialize()    
target = f"{appFolder}\\app.exe"
wDir = f"{appFolder}\\app.exe"
shell = Dispatch("WScript.Shell")
shortcut = shell.CreateShortCut(f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{appName}.lnk")
shortcut.Targetpath = target
shortcut.WorkingDirectory = wDir
shortcut.save()
def round_rectangle(x1, y1, x2, y2, radius, color, **kwargs):
    points = [
            x1+radius, y1,
            x1+radius, y1,
            x2-radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1+radius,
            x1, y1
            ]
    return canvas.create_polygon(points, **kwargs, smooth=True, fill=color)
canvas = Canvas(app, bg="black", highlightthickness=0)
canvas.pack(fill=BOTH, expand=1)
round_rectangle(0, 0, width, height, radius=50, color=bgColor)
offsetx = 0
offsety = 0
currentX = position_right
currentY = position_top
def drag(event):
    global currentX, currentY
    x = app.winfo_pointerx() - app.offsetx
    y = app.winfo_pointery() - app.offsety
    app.geometry('+{x}+{y}'.format(x=x,y=y))
    currentX = x
    currentY = y
def click(event):
    app.offsetx = event.x
    app.offsety = event.y
colors = ["red", "green", "blue"]
def changeColor():
    color = random.choice(colors)
    round_rectangle(0, 0, width, height, radius=50, color=color)
    timeLabel.config(background=color)
    dateLabel.config(background=color)
    dayLabel.config(background=color)
def keySc(e):
    global currentX, currentY
    key = e.keysym
    increment = 10
    if key == "R" or key == "r":
        app.geometry(f'{width}x{height}+{position_right}+{position_top}')
        currentX = position_right
        currentY = position_top
    elif key == "Up" and currentY > 0:
        currentY = currentY - increment
        app.geometry(f"+{currentX}+{currentY}")
    elif key == "Down"  and currentY < (screen_height - height):
        currentY = currentY + increment
        app.geometry(f"+{currentX}+{currentY}")
    elif key == "Left" and currentX > 0:
        currentX = currentX - increment
        app.geometry(f"+{currentX}+{currentY}")
    elif key == "Right" and currentX < (screen_width - width):
        currentX = currentX + increment
        app.geometry(f"+{currentX}+{currentY}")
    if key == "c" or key == "C":
        changeColor()
def updateTime():
   cTime = time.strftime("%I:%M:%S")
   cDate = time.strftime("%B %d, %Y")
   cDay = time.strftime("%A")
   timeLabel.config(text=cTime)
   dateLabel.config(text=cDate)
   dayLabel.config(text=cDay)
   app.after(1000, updateTime)
timeLabel = Label(app, font=("arial",30), background=bgColor, foreground="white")
timeLabel.place(relx=0.50, rely=0.02, anchor=N)
dateLabel = Label(app, font=("arial",20), background=bgColor, foreground="white")
dateLabel.place(relx=0.50, rely=0.50, anchor=CENTER)
dayLabel = Label(app, font=("arial",20), background=bgColor, foreground="white")
dayLabel.place(relx=0.50, rely=0.90, anchor=S)
updateTime()
def doNothing():pass
app.wm_attributes("-transparentcolor", "black")
app.bind("<Button-1>", click)
app.bind("<B1-Motion>", drag)
app.bind("<KeyPress>", keySc)
app.protocol("WM_DELETE_WINDOW", doNothing)
app.mainloop()
#Made with ❤ by Bidhan Acharya