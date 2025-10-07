# Gabi's Functions
# Version 1.1

import random
import os
import json

# --- File Stuff --- #

def editFile(file, index, text):
    FileRead = open(file, "r")
    FileList = FileRead.readlines()
    FileRead.close()

    FileWrite = open(file, "w")

    for i in range(len(FileList)):
        x = FileList[i]
        if i == index:
            FileWrite.write(text + "\n")
        else:
            FileWrite.write(x)

def newSaveFolder(dir, savename, overrideAllow=True, overrideChoice=False):
    if dir[-1] != "/":
        dir += "/"
    if os.path.exists(dir + savename):  # Checks if folder exists
        if overrideAllow:
            if overrideChoice:
                if input("Are you sure you want to override this file? (y/n): ") in ("y", "yes", "Y", "YES", "of course kind sir!"):
                    os.makedirs(name=dir + savename, exist_ok=True)  # Creates folder, exist_ok makes it so it can override the file
                else:
                    exit()
            else:
                os.makedirs(name=dir + savename, exist_ok=True) # Creates folder, exist_ok makes it so it can override the file
        else:
            exit()
    else:
        os.makedirs(name=dir + savename) # Creates folder

    return dir + savename

def loadSaveAsList(save):
    File = open(save, "r")
    List = File.readlines()
    File.close()
    
    return List

def loadCSV(dir: str,exclude:list=None):
    file = open(dir, "r")
    list = file.read()

    list = list.split(',')

    if exclude != None:
        for index in sorted(exclude, reverse=True):
            del list[index]
    
    return list

def returnFilesInFolder(dir, ofFileType:str | tuple = "Any", includeExtension=True, includeDir=False):
    lis = []

    if os.path.exists(dir):
        files = os.listdir(dir)
        for x in range(0, len(files)):
            if os.path.isfile(dir + files[x]):
                if ofFileType == "Any":
                    p = ""
                    if not includeExtension:
                        p += os.path.splitext(files[x])[0]
                    else:
                        p += files[x]
                    if includeDir:
                        p = dir + p
                    lis.append(p)
                else:
                    if files[x].endswith(ofFileType):
                        p = ""
                        if not includeExtension:
                            p += os.path.splitext(files[x])[0]
                        else:
                            p += files[x]
                        if includeDir:
                            p = dir + p
                        lis.append(p)
    
    return lis

# --- Misc --- #

def NoSlashN(inString, endOnly=True):
    if not endOnly:
        return inString.replace("\n","")
    elif inString[-1:] == "\n":
        return inString[:-1]
    else:
        return inString

def NumberedList(List, line=": ", shuffle=False, iterationOutput=False):
    if shuffle:
        random.shuffle(List)
    for x in range(len(List)):
        print(str(x + 1) + " - " + List[x])
    if iterationOutput:
        return input(line)
    else:
        return List[int(input(line)) - 1]

def NumberToText(number, abbreviated=False, roundTo=2, exclude=("hundred","thousand")):
    if number >= pow(10,54) and not "septendecillion" in exclude:
        if abbreviated:
            return str(round(number/pow(10,54), roundTo)) + "Spd"
        return str(round(number/pow(10,54), roundTo)) + " Septendecillion"
    elif number >= pow(10,51) and not "sexdecillion" in exclude:
        if abbreviated:
            return str(round(number/pow(10,51), roundTo)) + "Sxd"
        return str(round(number/pow(10,51), roundTo)) + " Sexdecillion"
    elif number >= pow(10,48) and not "quindecillion" in exclude:
        if abbreviated:
            return str(round(number/pow(10,48), roundTo)) + "Qdc"
        return str(round(number/pow(10,48), roundTo)) + " Quindecillion"
    elif number >= pow(10,45) and not "quattuordecillion" in exclude:
        if abbreviated:
            return str(round(number/pow(10,45), roundTo)) + "Qt"
        return str(round(number/pow(10,45), roundTo)) + " Quattuordecillion"
    elif number >= pow(10,42) and not "tredecillion" in exclude:
        if abbreviated:
            return str(round(number/pow(10,42), roundTo)) + "Tr"
        return str(round(number/pow(10,42), roundTo)) + " Tredecillion"
    elif number >= pow(10,39) and not "duodecillion" in exclude:
        if abbreviated:
            return str(round(number/pow(10,39), roundTo)) + "Du"
        return str(round(number/pow(10,39), roundTo)) + " Duodecillion"
    elif number >= pow(10,36) and not "undecillion" in exclude:
        if abbreviated:
            return str(round(number/pow(10,36), roundTo)) + "Und"
        return str(round(number/pow(10,36), roundTo)) + " Undecillion"
    elif number >= pow(10,33) and not "decillion" in exclude:
        if abbreviated:
            return str(round(number/pow(10,33), roundTo)) + "De"
        return str(round(number/pow(10,33), roundTo)) + " Decillion"
    elif number >= pow(10,30) and not "nonillion" in exclude:
        if abbreviated:
            return str(round(number/pow(10,30), roundTo)) + "No"
        return str(round(number/pow(10,30), roundTo)) + " Nonillion"
    elif number >= pow(10,27) and not "octillion" in exclude:
        if abbreviated:
            return str(round(number/pow(10,27), roundTo)) + "Oc"
        return str(round(number/pow(10,27), roundTo)) + " Octillion"
    elif number >= pow(10,24) and not "septillion" in exclude:
        if abbreviated:
            return str(round(number/pow(10,24), roundTo)) + "Sp"
        return str(round(number/pow(10,24), roundTo)) + " Septillion"
    elif number >= pow(10,21) and not "sextillion" in exclude:
        if abbreviated:
            return str(round(number/pow(10,21), roundTo)) + "Sx"
        return str(round(number/pow(10,21), roundTo)) + " Sextillion"
    elif number >= pow(10,18) and not "quintillion" in exclude:
        if abbreviated:
            return str(round(number/pow(10,18), roundTo)) + "Qn"
        return str(round(number/pow(10,18), roundTo)) + " Quintillion"
    elif number >= pow(10,15) and not "quadrillion" in exclude:
        if abbreviated:
            return str(round(number/pow(10,15), roundTo)) + "Qd"
        return str(round(number/pow(10,15), roundTo)) + " Quadrillion"
    elif number >= pow(10,12) and not "trillion" in exclude:
        if abbreviated:
            return str(round(number/pow(10,12), roundTo)) + "Tr"
        return str(round(number/pow(10,12), roundTo)) + " Trillion"
    elif number >= pow(10,9) and not "billion" in exclude:
        if abbreviated:
            return str(round(number/pow(10,9), roundTo)) + "Bi"
        return str(round(number/pow(10,9), roundTo)) + " Billion"
    elif number >= pow(10,6) and not "million" in exclude:
        if abbreviated:
            return str(round(number/pow(10,6), roundTo)) + "Mi"
        return str(round(number/pow(10,2), roundTo)) + " Million"
    elif number >= pow(10,3) and not "thousand" in exclude:
        if abbreviated:
            return str(round(number/1000, roundTo)) + "K"
        return str(round(number/1000, roundTo)) + " Thousand"
    elif number >= pow(10,2) and not "hundred" in exclude:
        if abbreviated:
            return str(round(number/pow(10,2), roundTo)) + "Hun"
        return str(round(number/pow(10,2), roundTo)) + " Hundred"
    else:
        return str(round(number))
    
def addToTempList(list: list, newItem):
    list.append(newItem)
    return list