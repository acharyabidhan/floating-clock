from tkinter import*
from os import path
from tkinter import Canvas
from win32com.client import Dispatch
import time, nepali_datetime, pythoncom, darkdetect

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

bgColor = None
fgColor = None

if darkdetect.isDark():
    bgColor = "black"
    fgColor = "white"
else:
    bgColor = "white"
    fgColor = "black"

transparentColor = "pink"
app.config(background=transparentColor)

######################################################
#Variables for creating shortcut
username = (path.split(path.expanduser('~'))[-1])
appName = "nep-clock"
target = f"{appName}\\{appName}.exe"
wDir = f"C:\\{appName}"
######################
pythoncom.CoInitialize()    
shell = Dispatch("WScript.Shell")
shortcut = shell.CreateShortCut(f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{appName}.lnk")
shortcut.Targetpath = target
shortcut.WorkingDirectory = wDir
shortcut.save()
######################################################

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

canvas = Canvas(app, bg=transparentColor, highlightthickness=0)
canvas.pack(fill=BOTH, expand=1)

round_rectangle(0, 0, width, height, radius=50, color=bgColor)

offsetx = 0
offsety = 0
currentX = position_right
currentY = position_top

lightColor = "white"
darkColor = "black"

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

def savePstate(bg):
    pStateFile = open("pstate", "w")
    pStateFile.write(bg)
    pStateFile.close()

def lightTheme():
    round_rectangle(0, 0, width, height, radius=50, color=lightColor)
    timeLabel.config(background=lightColor, foreground=darkColor)
    dateLabel.config(background=lightColor, foreground=darkColor)
    dayLabel.config(background=lightColor, foreground=darkColor)
    savePstate("light")

def darkTheme():
    round_rectangle(0, 0, width, height, radius=50, color="black")
    timeLabel.config(background=darkColor, foreground=lightColor)
    dateLabel.config(background=darkColor, foreground=lightColor)
    dayLabel.config(background=darkColor, foreground=lightColor)
    savePstate("dark")

def makeTransparent():
    round_rectangle(0, 0, width, height, radius=50, color=transparentColor)
    timeLabel.config(background=transparentColor, foreground=lightColor)
    dateLabel.config(background=transparentColor, foreground=lightColor)
    dayLabel.config(background=transparentColor, foreground=lightColor)
    savePstate("clear")

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

    elif key == "d" or key == "D":darkTheme()
    elif key == "l" or key == "L":lightTheme()
    elif key == "t" or key == "T":makeTransparent()

def converToNepali(n):
    engNum = str(n)
    nepNumList = []
    for i in engNum:
        if i == "1":nepNumList.append("१")
        elif i == "2":nepNumList.append("२")
        elif i == "3":nepNumList.append("३")
        elif i == "4":nepNumList.append("४")
        elif i == "5":nepNumList.append("५")
        elif i == "6":nepNumList.append("६")
        elif i == "7":nepNumList.append("७")
        elif i == "8":nepNumList.append("८")
        elif i == "9":nepNumList.append("९")
        else:nepNumList.append("०")
    return "".join(nepNumList)

def updateTime():
    cHr = converToNepali(time.strftime("%I"))
    cMin = converToNepali(time.strftime("%M"))
    cSec = converToNepali(time.strftime("%S"))
    nepDate = nepali_datetime.date.today()
    nepDate = str(nepDate).split("-")
    nepYear, nepMonth, nepDay = int(nepDate[0]), int(nepDate[1]), int(nepDate[2])
    cDate = nepali_datetime.date(nepYear, nepMonth, nepDay).strftime("%N %D, %K")
    cDay = nepali_datetime.date(nepYear, nepMonth, nepDay).strftime("%G")
    cTime = f"{cHr}:{cMin}:{cSec}"
    timeLabel.config(text=cTime)
    dateLabel.config(text=cDate)
    dayLabel.config(text=cDay)
    app.after(1000, updateTime)

timeLabel = Label(app, font=("arial",30), background=bgColor, foreground=fgColor)
timeLabel.place(relx=0.50, rely=0.02, anchor=N)

dateLabel = Label(app, font=("arial",20), background=bgColor, foreground=fgColor)
dateLabel.place(relx=0.50, rely=0.50, anchor=CENTER)

dayLabel = Label(app, font=("arial",20), background=bgColor, foreground=fgColor)
dayLabel.place(relx=0.50, rely=0.90, anchor=S)

if path.isfile("pstate"):
    pStateDetail = open("pstate", "r")
    whatToDo = pStateDetail.read()
    pStateDetail.close()
    if whatToDo == "light":lightTheme()
    elif whatToDo == "dark":darkTheme()
    elif whatToDo == "clear":makeTransparent()

updateTime()

def doNothing():pass

app.wm_attributes("-transparentcolor", "pink")
app.bind("<Button-1>", click)
app.bind("<B1-Motion>", drag)
app.bind("<KeyPress>", keySc)
app.protocol("WM_DELETE_WINDOW", doNothing)

app.mainloop()
#Made with ❤ by Bidhan Acharya