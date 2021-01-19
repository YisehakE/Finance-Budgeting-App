import tkinter as tk
from tkinter import *
from FinancialObj import *
import config

LINEBREAK = "________________________________________\n"


def readFileToArr(file):
    fileArr = []
    with open(file, "r") as userAccount:
        for line in userAccount:
            fileArr.append(line)
    return fileArr


''' REGISTRATION METHODS'''
def sendRegistration(userBox, passBox):
    username = userBox.get()
    password = passBox.get()

    if bool(username) and bool(password):
        with open("LoginRecord.txt", "a") as loginTxt:
            loginTxt.write("\n" + username + " ---> " + password)

        with open(username + " Money.txt", "w+") as newFile:
            newFile.write("")


''' DASHBOARD METHODS'''
def sendInfo(user, date, inc, fix, roll, curr):
    income = inc.get("1.0", 'end-1c')
    fixed = fix.get("1.0", 'end-1c')
    rolling = roll.get("1.0", 'end-1c')
    current = curr.get("1.0", 'end-1c')

    if bool(income) and bool(fixed) and bool(rolling) and bool(current):
        numOfWeeks = getWeekNum(user) + 1
        file = user + " Money.txt"
        prevBalance = config.currentBalance
        with open(file, "a") as userAccount:
            userAccount.write("\n" + "              Week " + str(numOfWeeks) + "\n")
            userAccount.write("            " + date.get())
            userAccount.write("\n              Money Left")

            userAccount.write("\n            $" + str(prevBalance))

            userAccount.write("\n\nIncome Source(s)\n-" + income)
            userAccount.write("\nFixed Expenses\n-" + fixed)
            userAccount.write("\nMiscellaneous")
            userAccount.write("\n* Rolling Purchases\n-" + rolling)
            userAccount.write("\n* Current Purchase\n" + current)
            userAccount.write("\n" + LINEBREAK)

        setUserData(user)
        currWeekKey = "Week " + str(config.weekNum)
        #Gather values for new balance
        addInc = config.weekData[currWeekKey]["Income"]["Value"]
        subFix = config.weekData[currWeekKey]["Fixed Expenses"]["Value"]
        subRoll = config.weekData[currWeekKey]["Rolling Purchases"]["Value"]
        subCurr = config.weekData[currWeekKey]["Current Purchases"]["Value"]
        newBalance = prevBalance + addInc - subFix - subRoll - subCurr

        #Update line with old balance with new (within file)
        prevFileArr = readFileToArr(file)
        updateFileArr = readFileToArr(file)

        index = len(prevFileArr) - 1
        isLineFound = False
        replaceIndex = -1

        while not isLineFound and index > 0:
            if prevFileArr[index] == "            $" + str(prevBalance) + "\n":
                replaceIndex = index
                isLineFound = True
            index -= 1

        updateFileArr[replaceIndex] = "            $" + str(newBalance) + "\n"

        with open(file, 'w') as updateFile:
            for line in updateFileArr:
                updateFile.write(line)

        #Update global variables once again
        checkFile = readFileToArr(file)
        if len(checkFile) != 0:
            setUserData(user)
            config.weekBar.menu.add_command(label=currWeekKey, command=lambda: display_week(currWeekKey))
        else:
            print("File is Empty!")


def getWeekNum(user):
    count = 0
    with open(user + " Money.txt", "r") as userAccount:
        for line in userAccount:
            if line == LINEBREAK:
                count += 1

    return count

def getBalance(fileArr):
    if len(fileArr) == 0:
        return 0
    count = len(fileArr) - 1

    balance = " "
    balanceFound = False
    while not balanceFound:
        test = fileArr[count]
        if test == "         Money Left\n":
            balance = fileArr[count + 1]
            balanceFound = True
        count -= 1
    balance = balance.strip()[1:]

    for char in balance:
        if char == ',':
            balance = balance.replace(char, '')

    balance = float(balance)
    return balance


def setUserData(user):
    dummy = FinWeek(user + " Money.txt")

    if bool(dummy.refinedWeekList):
        config.weekNum = len(dummy.splitWeekList)
        config.currentBalance = dummy.currentBalance
        config.weekData = dummy.refinedWeekList
    else:
        config.weekData = {}


def show_curr_balance(cont):
    balanceTxt = "Current Balance:\n$" + str(config.currentBalance)
    balanceLabel = tk.Label(cont, text=balanceTxt, font=("Verdana", 20), fg="green")
    balanceLabel.grid(row=2, column=0, pady=10, padx=10)


'''WEEKDATA Methods'''
def place_week_selector(cont):
    config.weekBar = tk.Menubutton(cont, text="Select Week")
    config.weekBar.grid(row=0, column=7)

    config.weekBar.menu = tk.Menu(config.weekBar, tearoff=0)
    config.weekBar["menu"] = config.weekBar.menu

    for i in range(config.weekNum):
        weekKey = "Week " + str(i + 1)
        config.weekBar.menu.add_command(label=weekKey, command=lambda x=i: display_week("Week " + str(x + 1)))

def display_week(key):
    #balanceOfWeek = tk.Label(cont, text="Balance Up to This Week: ", font=("Verdana", 20), fg="red")

    config.weekLabel.configure(text=key)
    config.incomeSrc.delete(0.0, tk.END)
    config.fixedSrc.delete(0.0, tk.END)
    config.rollingSrc.delete(0.0, tk.END)
    config.currentSrc.delete(0.0, tk.END)

    incomeTxt = createSourceTxt(key, "Income", "Sources")
    config.incomeSrc.insert(tk.END, incomeTxt)

    fixedTxt = createSourceTxt(key, "Fixed Expenses", "Sources")
    config.fixedSrc.insert(tk.END, fixedTxt)

    rollingTxt = createSourceTxt(key, "Rolling Purchases", "Sources")
    config.rollingSrc.insert(tk.END, rollingTxt)

    currentTxt = createSourceTxt(key, "Current Purchases", "Sources")
    config.currentSrc.insert(tk.END, currentTxt)


def createSourceTxt(weekKey, finDataKey, infoKey):
    sourceTxt = ""
    for source in config.weekData[weekKey][finDataKey][infoKey]:
        sourceTxt = sourceTxt + source
    return sourceTxt


def buildEmptyPage(cont):
    emptyTxt = "YOU HAVE EMPTY DATASET\n(ADD FINANCIAL INFO :)"
    config.emptyLabel = tk.Label(cont, text=emptyTxt, fg="blue")
    config.emptyLabel.grid(row=1, column=1)



