import tkinter as tk

"All Page Associated Variables"
currentUser = "NONE"
currentBalance = 0
weekData = {}
weekNum = 0

"WeekData Page Associated Widgits"
weekLabel = None
emptyLabel = None

incomeLabel = None
fixedLabel = None
rollingLabel = None
currentLabel = None

incomeSrc = None
fixedSrc = None
rollingSrc = None
currentSrc = None
weekBar = None


''' Widgit based functions'''

def destroy_frame_widgits(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def removeWidgit(widgit):
    if bool(widgit):
        widgit.grid_remove()


'''Global Variable Functions'''
def resetGlobals():
    global currentUser
    currentUser = "NONE"
    global currentBalance
    currentBalance = 0
    global weekData
    weekData = {}
    global weekNum
    weekNum = 0
    global weekLabel
    weekLabel = None
    global incomeSrc
    incomeSrc = None
    global fixedSrc
    fixedSrc = None
    global rollingSrc
    rollingSrc = None
    global currentSrc
    currentSrc = None
