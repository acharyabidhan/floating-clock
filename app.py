#Importing required libraries
from tkinter import*
from os import path
from tkinter import Canvas, messagebox
from win32com.client import Dispatch
import time, nepali_datetime, pythoncom, darkdetect
from win32api import GetMonitorInfo, MonitorFromPoint
#Geometry management of the widget
app = Tk()
app.overrideredirect(True)
app.resizable(0,0)
width = 200
height = 110

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

monitorInfo = GetMonitorInfo(MonitorFromPoint((0,0)))
screenSize = monitorInfo.get("Monitor")
taskarHeight = monitorInfo.get("Work")
position_top = (screen_height//2) - (height//2)
position_right = (screen_width//2) - (width//2)
app.geometry(f'{width}x{height}+{position_right}+{position_top}')
#Setting the background anf foreground color
bgColor = None
fgColor = None
#Detecting your PC's current theme and changing the values accordingly
if darkdetect.isDark():
    bgColor = "black"
    fgColor = "white"
else:
    bgColor = "white"
    fgColor = "black"
#Setting some random color for transparency of window
transparentColor = "pink"
app.config(background=transparentColor)
######################################################
#Variables for creating shortcut
#The below code creates the shortcut in start menu, so that everytime you logon, it starts the widget
# username = (path.split(path.expanduser('~'))[-1])
# appName = "nep-clock"
# target = f"C:\\{appName}\\{appName}.exe"
# wDir = f"C:\\{appName}"
# pythoncom.CoInitialize()    
# shell = Dispatch("WScript.Shell")
# shortcut = shell.CreateShortCut(f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{appName}.lnk")
# shortcut.Targetpath = target
# shortcut.WorkingDirectory = wDir
# shortcut.save()
######################################################
#Creating the rectangle with round borders
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
#Setting the position of widget
offsetx = 0
offsety = 0
currentX = position_right
currentY = position_top
#Some color variables
lightColor = "white"
darkColor = "black"
currentClock = "nepali"
clockMode = "nepali"
priority = "yes"
themeNow = darkdetect.theme()
#Functio to drag the widget around your screen
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
#function to save the current state of the widget in local disk
#so that everytime it starts, it will apply the previous state
def savePstate():
    allDetails = f"{themeNow}\n{currentClock}\n{clockMode}"
    pStateFile = open("pstate", "w")
    pStateFile.write(allDetails)
    pStateFile.close()
#Function to change the theme to light
def lightTheme():
    global themeNow
    themeNow = "Light"
    round_rectangle(0, 0, width, height, radius=50, color=lightColor)
    timeLabel.config(background=lightColor, foreground=darkColor)
    dateLabel.config(background=lightColor, foreground=darkColor)
    dayLabel.config(background=lightColor, foreground=darkColor)
    pinLabel.config(background=lightColor, foreground=darkColor)
    savePstate()
#Function to change the theme to dark
def darkTheme():
    global themeNow
    themeNow = "Dark"
    round_rectangle(0, 0, width, height, radius=50, color="black")
    timeLabel.config(background=darkColor, foreground=lightColor)
    dateLabel.config(background=darkColor, foreground=lightColor)
    dayLabel.config(background=darkColor, foreground=lightColor)
    pinLabel.config(background=darkColor, foreground=lightColor)
    savePstate()
#Function to change the theme to transparent
def makeTransparent():
    global themeNow
    themeNow = "Clear"
    round_rectangle(0, 0, width, height, radius=50, color=transparentColor)
    timeLabel.config(background=transparentColor, foreground=lightColor)
    dateLabel.config(background=transparentColor, foreground=lightColor)
    dayLabel.config(background=transparentColor, foreground=lightColor)
    pinLabel.config(background=transparentColor, foreground=lightColor)
    savePstate()
#function to switch the clock between AD to BS
def switchClock():
    global currentClock
    if currentClock == "english":
        currentClock = "nepali"
    else:
        currentClock = "english"
    savePstate()
#function to change the mode of the clock (available for BS clock only)
#Displaying everything in either in English or Nepali language
def changeMode():
    global clockMode
    if currentClock == "nepali":
        if clockMode == "nepali":
            clockMode = "english"
        else:
            clockMode = "nepali"
    savePstate()
#function to pot widget on top of window
def givePriority():
    global priority
    if priority == "yes":
        app.attributes('-topmost',True)
        pinLabel.config(text="📌")
        priority = "no"
    else:
        app.attributes('-topmost',False)
        pinLabel.config(text="")
        priority = "yes"
#function to show instructions
instructions = """
Use R key to reset position to center.
Use arrow keys to move across the screen (or click and drag using mouse).

Initial theme will be according to system theme.
Use D, L, T, B key for Dark mode, Light mode, Transparent, Blue theme respectively.

Use S key to switch between English and Nepali Date.
Use M key to switch between English and Nepali font (Only in Nepali Date).
Use P Key to give priority (keep this widget on top of all other apps or remain in the background).

All the changes you've made will be saved automatically.
All the above keys bindings will work only when the widget is focused.
"""
def showInstructions():
    messagebox.showinfo("Instructions", instructions)
#Function to get the key event and do the task accordingly
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
    elif key == "m" or key == "M":changeMode()
    elif key == "s" or key == "S":switchClock()
    elif key == "p" or key == "P":givePriority()
    elif key == "b" or key == "B":blueColor()
    elif key == "h" or key == "H": showInstructions()
#function to change background color to cool blue
def blueColor():
    global themeNow
    themeNow = "Blue"
    round_rectangle(0, 0, width, height, radius=50, color="#0059ff")
    timeLabel.config(background="#0059ff", foreground=lightColor)
    dateLabel.config(background="#0059ff", foreground=lightColor)
    dayLabel.config(background="#0059ff", foreground=lightColor)
    pinLabel.config(background="#0059ff", foreground=lightColor)
    savePstate()
#function to convert english numbers to nepali
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
#function to update time every one second
def updateTime():
    nepDate = nepali_datetime.date.today()
    nepDate = str(nepDate).split("-")
    nepYear, nepMonth, nepDay = int(nepDate[0]), int(nepDate[1]), int(nepDate[2])
    cHr = time.strftime("%I")
    cMin = time.strftime("%M")
    cSec = time.strftime("%S")
    if clockMode == "nepali" and currentClock == "nepali":
        cHr = converToNepali(cHr)
        cMin = converToNepali(cMin)
        cSec = converToNepali(cSec)
        cDate = nepali_datetime.date(nepYear, nepMonth, nepDay).strftime("%N %D, %K")
        cDay = nepali_datetime.date(nepYear, nepMonth, nepDay).strftime("%G")
    else:
        cDate = nepali_datetime.date(nepYear, nepMonth, nepDay).strftime("%B %d, %Y")
        cDay = time.strftime("%A")
    if currentClock == "english":
        cDate = time.strftime("%B %d, %Y")
        cDay = time.strftime("%A")
    cTime = f"{cHr}:{cMin}:{cSec}"
    timeLabel.config(text=cTime)
    dateLabel.config(text=cDate)
    dayLabel.config(text=cDay)
    app.after(1000, updateTime)
#tkinter label objects
timeLabel = Label(app, font=("arial",20), background=bgColor, foreground=fgColor)
timeLabel.place(relx=0.50, rely=0.02, anchor=N)

pinLabel = Label(app, font=("arial",15), background=bgColor, foreground=fgColor)
pinLabel.place(relx=0.95, rely=0.05, anchor=NE)

dateLabel = Label(app, font=("arial",15), background=bgColor, foreground=fgColor)
dateLabel.place(relx=0.50, rely=0.50, anchor=CENTER)
dayLabel = Label(app, font=("arial",15), background=bgColor, foreground=fgColor)
dayLabel.place(relx=0.50, rely=0.90, anchor=S)
#getting and applying the previous state of the clock and other deatils
if path.isfile("pstate"):
    pStateDetail = open("pstate", "r")
    whatToDo = pStateDetail.readlines()
    tcolor = whatToDo[0][:-1]
    pStateDetail.close()
    if whatToDo[1][:-1] == "nepali":
        currentClock = "nepali"
    else:
        currentClock = "english"
    if whatToDo[2][:-1] == "nepali":
        clockMode = "nepali"
    else:
        clockMode = "english"
    if tcolor == "Light":
        lightTheme()
    elif tcolor == "Dark":
        darkTheme()
    elif tcolor == "Clear":
        makeTransparent()
    elif tcolor == "Blue":
        blueColor()
else:
    savePstate()

#function that does nothing
def doNothing():pass
#Setting the pink color as transparent color
app.wm_attributes("-transparentcolor", "pink")
#binding the mouse left button to click function
app.bind("<Button-1>", click)
#binding the motion of mouse to drag function
app.bind("<B1-Motion>", drag)
#binding the key events to keySc function
app.bind("<KeyPress>", keySc)
#preventing widget from being closed. if you attempt to close the widget by pressing Alt+F4, it calls the doNothing function above,
#where the function does nothing
app.protocol("WM_DELETE_WINDOW", doNothing)
#calling the updateTime function
updateTime()
#running widget forever in mainloop
app.mainloop()
#Thanku for the developer of nepali-datetime library:)
#Made with ❤ by Bidhan Acharya