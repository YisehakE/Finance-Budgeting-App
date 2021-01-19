from FinancialObj import *
import config


print(config.weekNum)
config.weekNum = 10
print(config.weekNum)
config.resetGlobals()
print(config.weekNum)

