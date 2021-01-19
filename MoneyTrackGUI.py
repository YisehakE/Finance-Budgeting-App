import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import Backend as back
from FinancialObj import *
import config

LARGE_FONT = ("Verdana", 30)


class MoneyTrack(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        self.menuArr = []

        for F in (LoginPage, RegisterPage, DashBoard, WeekData):

            if F is not LoginPage and F is not RegisterPage:
                self.menuArr.append(F)

            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, cont):
        if cont.__name__ == "DashBoard":
            self.title(config.currentUser + "'s " + cont.__name__)
            back.setUserData(config.currentUser)
            back.show_curr_balance(self.frames[cont])

        elif cont.__name__ == "LoginPage":
            self.title(cont.__name__)
        elif cont.__name__ == "RegisterPage":
            self.title(cont.__name__)
        elif cont.__name__ == "WeekData":
            self.title(config.currentUser + "'s " + cont.__name__)

        self.toggleMenu(cont)
        frame = self.frames[cont]
        frame.configure(bg="light grey")
        frame.tkraise()

    def show_frame_alt(self, cont):

        if cont.__name__ == "DashBoard":
            self.title(config.currentUser + "'s " + cont.__name__)
        elif cont.__name__ == "WeekData":
            self.title(config.currentUser + "'s " + cont.__name__)
            config.destroy_frame_widgits(self.frames[cont])
            if bool(config.weekData):
                self.frames[cont].buildCurrentPage()
            else:
                back.buildEmptyPage(self.frames[cont])

        self.toggleMenu(cont)
        frame = self.frames[cont]
        frame.configure(bg="light grey")
        frame.tkraise()

    def toggleMenu(self, cont):
        colNum = 0
        if cont is not LoginPage and cont is not RegisterPage:
            for item in self.menuArr:
                btnName = item.__name__
                navBtn = tk.Button(self.frames[cont], text=btnName, command=lambda x=item: self.show_frame_alt(x))
                navBtn.grid(row=0, column=colNum, colum=1)
                colNum += 1


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Login Page", font=LARGE_FONT, bg="light grey")
        label.grid(row=0, column=0, pady=10, padx=10)
        self.controller = controller

        userLabel = tk.Label(self, text="Username: ", bg="light grey")
        userLabel.grid(row=1, column=0)

        self.userEntry = ttk.Entry(self)
        self.userEntry.grid(row=2, column=0)

        passLabel = tk.Label(self, text="Password: ", bg="light grey")
        passLabel.grid(row=3, column=0)

        self.passEntry = ttk.Entry(self)
        self.passEntry.grid(row=4, column=0)

        enterButton = ttk.Button(self, text="Enter", command=lambda: self.checkLogin())
        enterButton.grid(row=5, column=0)

        registerButton = tk.Button(self, text="Press to Register",
                                   command=lambda: controller.show_frame(RegisterPage))
        registerButton.grid(row=6, column=0)

    def checkLogin(self):
        username = self.userEntry.get()
        password = self.passEntry.get()

        with open("LoginRecord.txt", "r") as loginTxt:

            for line in loginTxt:
                logLine = line.split(" ---> ")
                logLine[1] = logLine[1].replace("\n", "")
                if username == logLine[0]:
                    if password == logLine[1]:
                        config.currentUser = username
                        self.userEntry.delete(0, tk.END)
                        self.passEntry.delete(0, tk.END)
                        return self.controller.show_frame(DashBoard)
                else:
                    pass

            self.userEntry.delete(0, tk.END)
            self.passEntry.delete(0, tk.END)


class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Registration", font=LARGE_FONT, bg="light grey")
        label.pack(pady=10, padx=10)
        self.controller = controller

        userLabel = tk.Label(self, text="Create username: ", bg="light grey")
        userLabel.pack()

        userEntry = tk.Entry(self)
        userEntry.pack()

        passLabel = tk.Label(self, text="Create password: ", bg="light grey")
        passLabel.pack()

        passEntry = tk.Entry(self)
        passEntry.pack()

        enterButton = tk.Button(self, text="Enter", command=lambda: back.sendRegistration(userEntry, passEntry))
        enterButton.pack()

        logPageButton = tk.Button(self, text="Back to login",
                                  command=lambda: controller.show_frame(LoginPage))
        logPageButton.pack()


class DashBoard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        pageLabel = tk.Label(self, text="Dashboard", font=LARGE_FONT, bg="light grey")
        pageLabel.grid(row=1, column=0, pady=10, padx=10)

        # Date inputs
        dateLabel = tk.Label(self, text="Enter date (xx/xx/xxxx): ", bg="light grey")
        dateLabel.grid(row=3, column=1)

        dateEntry = ttk.Entry(self)
        dateEntry.grid(row=3, column=2, pady=10, padx=10)

        # Income inputs
        incomeLabel = tk.Label(self, text="Enter income sources: ", bg="light grey")
        incomeLabel.grid(row=4, column=1)

        incomeEntry = tk.Text(self, width=25, height=5)
        incomeEntry.grid(row=4, column=2, pady=10, padx=10)

        # Fixed expenses
        fixedExpLabel = tk.Label(self, text="Enter fixed expenses: ", bg="light grey")
        fixedExpLabel.grid(row=5, column=1)

        fixedExpEntry = tk.Text(self, width=25, height=5)
        fixedExpEntry.grid(row=5, column=2, pady=10, padx=10)

        """ MISCELLANEOUS EXPENSES
            TODO - Find way to not ask for rolling later
        """
        rollingLabel = tk.Label(self, text="Enter rolling purchases: ", bg="light grey")
        rollingLabel.grid(row=6, column=1)

        rollingEntry = tk.Text(self, width=25, height=5)
        rollingEntry.grid(row=6, column=2, pady=10, padx=10)

        currentPurchaseLabel = tk.Label(self, text="Enter current purchases: ", bg="light grey")
        currentPurchaseLabel.grid(row=7, column=1)

        currentPurchaseText = tk.Text(self, width=25, height=5)
        currentPurchaseText.grid(row=7, column=2, pady=10, padx=10)

        sendInfoBtn = tk.Button(self, bg="blue", text="Send info",
                                command=lambda: back.sendInfo(config.currentUser, dateEntry, incomeEntry,
                                                              fixedExpEntry, rollingEntry,
                                                              currentPurchaseText))
        sendInfoBtn.grid(row=8, column=2, pady=10, padx=10)


        # Sign out button
        signOutBtn = tk.Button(self, text="Signout",
                               command=lambda: self.signOutFunc())
        signOutBtn.grid(row=9, column=2, pady=10, padx=10)

    def signOutFunc(self):
        config.resetGlobals()
        self.controller.show_frame(LoginPage)


class WeekData(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

    def buildCurrentPage(self):
        back.place_week_selector(self)
        currWeekKey = "Week " + str(config.weekNum)

        config.weekLabel = tk.Label(self, text=currWeekKey, font=LARGE_FONT, bg="light grey")
        config.weekLabel.grid(row=0, column=2)

        config.incomeLabel = tk.Label(self, text="Income Sources:", font=("Verdana", 20), fg="red", bg="light grey")
        config.incomeLabel.grid(row=2, column=1, pady=10, padx=10)

        config.incomeSrc = tk.Text(self, font=("Verdana", 12), width=30, height=10)
        config.incomeSrc.grid(row=3, column=1, pady=10, padx=10)

        config.fixedLabel = tk.Label(self, text="Fixed Expenses:", font=("Verdana", 20), fg="red", bg="light grey")
        config.fixedLabel.grid(row=2, column=3, pady=10, padx=10)

        config.fixedSrc = tk.Text(self, font=("Verdana", 12), width=30, height=10)
        config.fixedSrc.grid(row=3, column=3, pady=10, padx=10)

        config.rollingLabel = tk.Label(self, text="Rolling Purchases:", font=("Verdana", 20), fg="red", bg="light grey")
        config.rollingLabel.grid(row=4, column=1, pady=10, padx=10)

        config.rollingSrc = tk.Text(self, font=("Verdana", 12), width=30, height=10)
        config.rollingSrc.grid(row=5, column=1, pady=10, padx=10)

        config.currentLabel = tk.Label(self, text="Current Purchases:", font=("Verdana", 20), fg="red", bg="light grey")
        config.currentLabel.grid(row=4, column=3, pady=10, padx=10)

        config.currentSrc = tk.Text(self, font=("Verdana", 12), width=30, height=10)
        config.currentSrc.grid(row=5, column=3, pady=10, padx=10)

        back.display_week(currWeekKey)


app = MoneyTrack()
app.mainloop()

