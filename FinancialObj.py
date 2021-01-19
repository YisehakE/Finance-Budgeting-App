import Backend as Back


class FinWeek():
    def __init__(self, fileTxt):
        self.allWeeksArr = Back.readFileToArr(fileTxt)
        self.currentBalance = Back.getBalance(self.allWeeksArr)
        self.file = fileTxt
        self.splitWeekList = {}
        self.refinedWeekList = {}
        self.splitWeeks()
        self.refineWeeks()

    def splitWeeks(self):
        if len(self.allWeeksArr) != 0:
            weekNum = 1
            breakFound = False
            count = 0
            while count < len(self.allWeeksArr):

                eachWeekArr = []
                while not breakFound:
                    line = self.allWeeksArr[count]
                    if line != Back.LINEBREAK:
                        eachWeekArr.append(line)
                        count += 1
                    else:
                        count += 1
                        breakFound = True

                eachWeekArr.append(Back.LINEBREAK)
                self.splitWeekList["Week " + str(weekNum)] = eachWeekArr
                breakFound = False
                weekNum += 1

    def refineWeeks(self):

        if bool(self.splitWeekList):
            for key in self.splitWeekList:
                finData = {}
                weekData = {}
                unrefinedWeek = self.splitWeekList[key]

                finData["Income"] = {"Sources": IncSrc(unrefinedWeek).sources,
                                     "Value": IncSrc(unrefinedWeek).getTotalValue()}
                weekData.update(finData)

                finData["Fixed Expenses"] = {"Sources": FixExp(unrefinedWeek).sources,
                                             "Value": FixExp(unrefinedWeek).getTotalValue()}
                weekData.update(finData)

                finData["Rolling Purchases"] = {"Sources": RollPurc(unrefinedWeek).sources,
                                                "Value": RollPurc(unrefinedWeek).getTotalValue()}
                weekData.update(finData)

                finData["Current Purchases"] = {"Sources": CurrPurc(unrefinedWeek).sources,
                                                "Value": CurrPurc(unrefinedWeek).getTotalValue()}
                weekData.update(finData)

                self.refinedWeekList[key] = weekData



class FinData():

    def __init__(self, weekArr):
        self.weekArr = weekArr
        self.sources = []
        self.totalValue = 0

    def fillSources(self, startLine, endLine):
        catchFound = False

        for i in range(len(self.weekArr)):
            line = self.weekArr[i]
            if line == startLine:
                count = i + 1
                while not catchFound:
                    line = self.weekArr[count]
                    if line != endLine:
                        self.sources.append(line)
                        self.totalValue += self.getValue(line)
                        count += 1
                    else:
                        catchFound = True
            if catchFound:
                break

    def getValue(self, line):
        value = ""
        #Checks case with no item
        if line.find("NONE") != -1:
            return 0

        arr = line.split(":")
        if len(arr) == 2:
            temp = []
            value = arr[1].strip()[1:]

            for char in value:
                if char == ',':
                    value = value.replace(char, '')
                if char == " ":
                    temp = value.split(" ")
                    value = temp[0]

            value = float(value)
            return value
        return 0

    def getTotalValue(self):
        total = 0
        for i in self.sources:
            total += self.getValue(i)

        return total

    # def toString

class IncSrc(FinData):

    def __init__(self, weekArr):
        super(IncSrc, self).__init__(weekArr)
        self.fillSources("Income Source(s)\n", "Fixed Expenses\n")
        self.totalValue = self.getTotalValue()


class FixExp(FinData):
    def __init__(self, arr):
        super(FixExp, self).__init__(arr)
        self.fillSources("Fixed Expenses\n", "Miscellaneous\n")
        self.totalValue = self.getTotalValue()


class RollPurc(FinData):
    def __init__(self, weekArr):
        super(RollPurc, self).__init__(weekArr)
        self.fillSources("* Rolling Purchases\n", "* Current Purchase\n")
        self.totalValue = self.getTotalValue()


class CurrPurc(FinData):
    def __init__(self, weekArr):
        super(CurrPurc, self).__init__(weekArr)
        self.fillSources("* Current Purchase\n", Back.LINEBREAK)
        self.totalValue = self.getTotalValue()



