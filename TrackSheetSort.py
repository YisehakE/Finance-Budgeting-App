
'''First just initially sort OG file into copy'''
with open("MoneyTrackOG.txt", "r") as OG:
    with open("Yisehak Money.txt", "w") as writeFile:
        for line in OG:
            writeFile.write(line)



