# --- Libraries --- #

import pygame, sys, os.path

import time

from data import gabisfunctions as gf

from data import pyclickerClasses as pcl

import json

import pyperclip

import shutil

import math

# --- CONSTANTS --- #

DISSALLOWEDFILENAMES = ("CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9", ".", "..")

# --- Initiate Pygame --- #

pygame.init()

# --- Subprogram --- #

# -- Savedata -- #

def createSave(saveName: str):
    shutil.copy(pcl.filesDir.templateSaveFile, "data/savedata/" + saveName + ".json")

    save = open("data/savedata/" + saveName + ".json", "r")

    jsonData = json.load(save)
    save.close()

    jsonData["Pythons"] = pythons

    save = open("data/savedata/" + saveName + ".json","w")

    json.dump(jsonData, save, indent=4)

    save.close()

def saveList(forDisplay):
    if forDisplay:
        gf.returnFilesInFolder("data/savedata/",".json",False,False)
    else:
        gf.returnFilesInFolder("data/savedata/",".json",True,True)

def loadSave(saveName: str):
    save = open("data/savedata/" + saveName + ".json", "r")
    jsonData = json.load(save)

    return jsonData

def saveUpdatePythons(saveName):
    save = open("data/savedata/" + saveName + ".json", "r")
    jsonData = json.load(save)
    save.close()

    jsonData["Pythons"] = pythons

    save = open("data/savedata/" + saveName + ".json","w")

    json.dump(jsonData, save, indent=4)

    save.close()

# -- Item Data -- #

def retrieveByTag(TAG,type="Name",menuLeaveMessage="Leave Shop"):
    if TAG == "EXIT":
        return menuLeaveMessage
    else:
        return itemsList[TAG][type]

# -- Settings -- #

# - Resolution - #

def settingsResolutionEdit(X, Y):
    settingsFile = open(pcl.filesDir.settingsFile,"r")
    jsonData = json.load(settingsFile)
    settingsFile.close()

    jsonData["resolution"]["X"] = X
    jsonData["resolution"]["Y"] = Y

    settingsFile = open(pcl.filesDir.settingsFile,"w")

    json.dump(jsonData, settingsFile, indent=4)

    settingsFile.close()

def resetResolution(screen, screenWidth, screenHeight, w=None, h=None):
    if w == None and h == None:
        settingsFile = open(pcl.filesDir.settingsFile,"r")
        jsonData = json.load(settingsFile)
        settingsFile.close()

        if w == None:
            w = jsonData["resolution"]["X"]
        if h == None:
            h = jsonData["resolution"]["Y"]

    if screenWidth != w and screenHeight != h:
        return pygame.display.set_mode((w, h)), w, h, True
    else:
        return screen, screenWidth, screenHeight, False

def settingsTextEdit(Value, Insert):
    settingsFile = open(pcl.filesDir.settingsFile,"r")
    jsonData = json.load(settingsFile)
    settingsFile.close()

    jsonData["text"][Value] = Insert

    settingsFile = open(pcl.filesDir.settingsFile,"w")

    json.dump(jsonData, settingsFile, indent=4)

    settingsFile.close()

# - Keybinds - #

def getKeybind(name):
    settingsFile = open(pcl.filesDir.settingsFile,"r")
    jsonData = json.load(settingsFile)
    settingsFile.close()
    return jsonData["keybind"][name]

def isKeybindDown(name: str, keysDown):
    flag = True
    keybind = getKeybind(name)
    if isinstance(keybind, list):
        for x in range(0, len(keybind)):
            if not keysDown[keybind[x]]:
                flag = False
    else:
        if not keysDown[keybind]:
            flag = False
    return flag

def setKeybind(name,keyvalue):
    settingsFile = open(pcl.filesDir.settingsFile,"r")
    jsonData = json.load(settingsFile)
    settingsFile.close()

    jsonData["keybind"][name] = keyvalue

    settingsFile = open(pcl.filesDir.settingsFile,"w")

    json.dump(jsonData, settingsFile, indent=4)

    settingsFile.close()

# -- Python Calculations -- #

def addPythonsByElement(dataElement, saveElement, deltatime, outputType=0): # 0 - how many to add, 1 - how many per second, singular 2 - how many per second, multiple
    if outputType == "0":
        return dataElement["PPS"] * saveElement["amount"] * saveElement["modifier"] * deltatime
    if outputType == "1":
        return dataElement["PPS"] * saveElement["modifier"]
    if outputType == "2":
        return dataElement["PPS"] * saveElement["amount"] * saveElement["modifier"]

def addPythonsByDictionary(gameDat, saveDat, deltatime, outputType=0): # 0 - how many to add, 1 - how many per second, singular 2 - how many per second, multiple
    if outputType == "0":
        for x in range(0,len(gameDat)):
            gameDat[x]

# --- Importing Files --- #

# -- Importing Settings -- #

if os.path.exists(pcl.filesDir.settingsFile):
    settingsFile = open(pcl.filesDir.settingsFile,"r")
    jsonData = json.load(settingsFile)
    settingsFile.close()

    debug = jsonData["debug"]

    screenWidth = jsonData["resolution"]["X"]
    screenHeight = jsonData["resolution"]["Y"]

    if screenWidth <= 200:
        screenWidth = 200

    if screenHeight <= 200:
        screenHeight = 200

    antialiasing = jsonData["text"]["antialiasing"]
    abbreviate = jsonData["text"]["abbreviate"]

    lying = jsonData["funstuff"]["lying"]

else:
    debug = False

    screenWidth = 500
    screenHeight = 500

    antialiasing = True
    abbreviate = False

    jsonData = {
        "debug": False,
        "resolution": { 
            "X":800,
            "Y":800
        },
        "text":{ 
            "antialiasing": True,
            "abbreviate": False
        },
        "funstuff": {
		    "lying": False
	    },
        "keybind": {
            "Back": 27,
            "ShopMenu": 101,
            "KeyboardTest": 1073741882,
            "EnableDebug": [
                1073741883,
                1073742048
            ],
            "Paste": [
                1073742048,
                118
            ],
            "Prev": 1073741904,
            "Next": 1073741903
        }
    }

    settingsFile = open(pcl.filesDir.settingsFile,"w")

    json.dump(jsonData, settingsFile, indent=4)

    settingsFile.close()

# -- Importing Gamefiles -- #

if os.path.exists("data/gamefiles/gamedata.json"):
    gameFile = open("data/gamefiles/gamedata.json","r")
    jsonData = json.load(gameFile)
    gameFile.close()

    itemsList = jsonData["Items"]

    gameFile = open("data/gamefiles/savefile template/savefile.json","r")
    jsonData = json.load(gameFile)
    gameFile.close()

else:
    jsonData = {
        "Items": {
            "WRA": {
                "Price": 80,
                "PPS": 0.1,
                "Requirement": 0,
                "Name": "Wrangler",
                "Description": "If you can't click em', catch em'"
            },
            "BRE": {
                "Price": 600,
                "PPS": 0.5,
                "Requirement": 0,
                "Name": "Breeder",
                "Description": "Look a mathmatician in the eyes, and say '1 + 1 = 3'"
            },
            "THI": {
                "Price": 1000,
                "PPS": 1,
                "Requirement": 500,
                "Name": "Theif",
                "Description": "Finders, keepers. You found the Python in their home though, so that doesn't work."
            },
            "LAB": {
                "Price": 2000,
                "PPS": 10,
                "Requirement": 900,
                "Name": "Python Laboritory",
                "Description": "Put the green stuff with the blue stuff and boom, Python."
            },
            "BRO": {
                "Price": 10000,
                "PPS": 30,
                "Requirement": 900,
                "Name": "Broker",
                "Description": "Invest, then invest more, then when you've invested that, you invest it again, then you... you get the idea."
            },
            "PRO": {
                "Price": 100000,
                "PPS": 100,
                "Requirement": 8000,
                "Name": "Python Programmer",
                "Description": "It's slave labour."
            }
        }
    }

    gameFile = open("data/gamefiles/gamedata.json","w")

    json.dump(jsonData, gameFile, indent=4)

    gameFile.close()

# --- Window Management --- #

if debug: print(itemsList)

# - Screen Values - #

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Python Clicker')

winodowImage = pygame.image.load('data/pythonClickerIcon.png')
pygame.display.set_icon(winodowImage)

mousePos = [0,0]

# --- Text Values --- #

# - Fonts - #

largefontsize = ((screenHeight + screenWidth)/2)/7.1
bigfontsize = ((screenHeight + screenWidth)/2)/10.65
mediumfontsize = ((screenHeight + screenWidth)/2)/14.2
smallfontsize = ((screenHeight + screenWidth)/2)/21.3
tinyfontsize = ((screenHeight + screenWidth)/2)/28.4

ComicSansLarge = pygame.font.Font('data/Comic Sans MS.ttf', round(largefontsize))
ComicSansBig = pygame.font.Font('data/Comic Sans MS.ttf', round(bigfontsize))
ComicSansMedium = pygame.font.Font('data/Comic Sans MS.ttf', round(mediumfontsize))
ComicSansSmall = pygame.font.Font('data/Comic Sans MS.ttf', round(smallfontsize))
ComicSansTiny = pygame.font.Font('data/Comic Sans MS.ttf', round(tinyfontsize))

# - DefaultTexts - #

buttonTextDark = ComicSansMedium.render('python', antialiasing, (0,0,0))
buttonTextLight = ComicSansMedium.render('python', antialiasing, (40,40,40))

# - Subprogram - #

def ComicSansCustomSize(customSize):
    x = ((screenHeight + screenWidth)/2)/customSize
    return pygame.font.Font('data/Comic Sans MS.ttf', round(x))

# --- Button Values --- #

buttonSizeX = screenWidth/3.5
buttonSizeY = screenHeight/9.5

buttonColour = (160, 205, 255)
darkButtonColour = (75, 90, 115)
lightButtonColour = (171, 211, 255)

# --- Menu Management --- #

takingTextInput = False
textInput = ""
fileInput = False
dirtyStop = False
firstSelect = True

isSettingsOpen = False
resolutionsMenu = False
textMenu = False

isInformationMenuOpen = False
informationMenuContents = "WRA"
informationButton = None

isShopMenuOpen = False

isCreateSaveMenuOpen = False

# - Subprograms - #

def openMenu(colour=(170,170,170),bg=True,bgcolour=(155,155,155)):
    if bg:
        pygame.draw.rect(screen, bgcolour,[0,0, screenWidth, screenHeight])
    pygame.draw.rect(screen, colour,[(screenWidth - screenWidth*0.6)/2, ((screenHeight - screenHeight*0.75)/2) + screenHeight*0.08, screenWidth*0.6, screenHeight*0.6])

def multipleOptionMenu(buttonsList,buttonPage,menuName="",visible=True):
    if visible:
        openMenu(bg=False)

        makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.3, menuButtonSizeX/3, menuButtonSizeY, 40, -100, "Back", ComicSansSmall, mousePos)
        makeButton((screenWidth - menuButtonSizeX)/2 + menuButtonSizeX/1.5, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.3, menuButtonSizeX/3, menuButtonSizeY, 40, -100, "Next", ComicSansSmall, mousePos)
        makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.2, menuButtonSizeX, menuButtonSizeY, 40, -100, retrieveByTag(buttonsList[(buttonPage - 1)*5 + 0]), ComicSansSmall, mousePos)
    
        if len(buttonsList) - (buttonPage - 1)*5 + 0 > 1:
            makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.1, menuButtonSizeX, menuButtonSizeY, 40, -100, retrieveByTag(buttonsList[(buttonPage - 1)*5 + 1]), ComicSansSmall, mousePos)
        if len(buttonsList) - (buttonPage - 1)*5 + 0 > 2:
            makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.0, menuButtonSizeX, menuButtonSizeY, 40, -100, retrieveByTag(buttonsList[(buttonPage - 1)*5 + 2]), ComicSansSmall, mousePos)
        if len(buttonsList) - (buttonPage - 1)*5 + 0 > 3:
            makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.1, menuButtonSizeX, menuButtonSizeY, 40, -100, retrieveByTag(buttonsList[(buttonPage - 1)*5 + 3]), ComicSansSmall, mousePos)
        if len(buttonsList) - (buttonPage - 1)*5 + 0 > 4:
            makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.2, menuButtonSizeX, menuButtonSizeY, 40, -100, retrieveByTag(buttonsList[(buttonPage - 1)*5 + 4]), ComicSansSmall, mousePos)

        screen.blit((ComicSansTiny.render(menuName, antialiasing, (0,0,0))), [(screenWidth/2) - ComicSansTiny.size(menuName)[0]/2,screenHeight*0.15])

        screen.blit(ComicSansTiny.render(str(buttonPage) + " / " + str(totalButtonPages(buttonsList)), antialiasing, (0,0,0)), [screenWidth/2.15,screenHeight*0.73])

def informationMenu(TAG,visible=True):
    if visible:
        openMenu(bg=False)

        pygame.draw.rect(screen, (160, 160, 160),[(screenWidth - screenWidth*0.55)/2, ((screenHeight - screenHeight*0.45)/2) + screenHeight*0.08, screenWidth*0.55, screenHeight*0.342])

        pygame.draw.rect(screen, (160, 160, 160),[(screenWidth - screenWidth*0.55)/2, ((screenHeight - screenHeight*0.72)/2) + screenHeight*0.08, screenWidth*0.55, screenHeight*0.12])

        makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.3, menuButtonSizeX/3, menuButtonSizeY, 40, -100, "Shop", ComicSansSmall, mousePos)
        makeButton((screenWidth - menuButtonSizeX)/2 + menuButtonSizeX/1.5, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.3, menuButtonSizeX/3, menuButtonSizeY, 40, -100, "Buy", ComicSansSmall, mousePos)

        screen.blit((ComicSansSmall.render(retrieveByTag(TAG), antialiasing, (0,0,0))), [(screenWidth/4.3), screenHeight*0.215])

        screen.blit((ComicSansTiny.render(str(retrieveByTag(TAG,"Price"))  + " Pythons", antialiasing, (0,0,0))), [(screenWidth/4.3), screenHeight*0.29])

        screen.blit((ComicSansTiny.render(retrieveByTag(TAG,"Description"), antialiasing, (0,0,0))), [(screenWidth/4.3), screenHeight*0.35])

def informationInput():
    #Previous Page
    if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.3, menuButtonSizeX/3, menuButtonSizeY, mousePos):
        return pcl.menus.prevpage
    #Next Page
    if onButton((screenWidth - menuButtonSizeX)/2 + menuButtonSizeX/1.5, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.3, menuButtonSizeX/3, menuButtonSizeY, mousePos):
        return pcl.menus.nextpage
    
    return None

def multipleOptionInput(buttonsList,buttonPage):
    #Previous Page
    if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.3, menuButtonSizeX/3, menuButtonSizeY, mousePos):
        if buttonPage != 1:
            return pcl.menus.prevpage
    #Next Page
    if onButton((screenWidth - menuButtonSizeX)/2 + menuButtonSizeX/1.5, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.3, menuButtonSizeX/3, menuButtonSizeY, mousePos):
        if totalButtonPages(buttonsList) != buttonPage:
            return pcl.menus.nextpage
    #Buttons 0-4
    if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.2, menuButtonSizeX, menuButtonSizeY, mousePos):
        return buttonsList[(buttonPage - 1)*5 + 0]
    elif len(buttonsList) - (buttonPage - 1)*5 + 0 > 1 and onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.1, menuButtonSizeX, menuButtonSizeY, mousePos):
        return buttonsList[(buttonPage - 1)*5 + 1]
    elif len(buttonsList) - (buttonPage - 1)*5 + 0 > 2 and onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.0, menuButtonSizeX, menuButtonSizeY, mousePos):
        return buttonsList[(buttonPage - 1)*5 + 2]
    elif len(buttonsList) - (buttonPage - 1)*5 + 0 > 3 and onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.1, menuButtonSizeX, menuButtonSizeY, mousePos):
        return buttonsList[(buttonPage - 1)*5 + 3]
    elif len(buttonsList) - (buttonPage - 1)*5 + 0 > 4 and onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.2, menuButtonSizeX, menuButtonSizeY, mousePos):
        return buttonsList[(buttonPage - 1)*5 + 4]
    else:
        return None

def totalButtonPages(buttonList):
    return math.ceil(len(buttonList) / 5)

def loadSaveMenu(saveMenuPage):
    multipleOptionInput(saveList(),saveMenuPage)

def takeInput(topMessage:str = ""):
    openMenu(bg=True)

    if ComicSansTiny.size(textInput)[0] >= (screenWidth*0.55)*4:
        pygame.draw.rect(screen, (160, 160, 160),[(screenWidth - screenWidth*0.55)/2, ((screenHeight - screenHeight*0.6)/2) + screenHeight*0.08, screenWidth*0.55, (screenHeight*0.08)*5])
    elif ComicSansTiny.size(textInput)[0] >= (screenWidth*0.55)*3:
        pygame.draw.rect(screen, (160, 160, 160),[(screenWidth - screenWidth*0.55)/2, ((screenHeight - screenHeight*0.6)/2) + screenHeight*0.08, screenWidth*0.55, (screenHeight*0.08)*4])
    elif ComicSansTiny.size(textInput)[0] >= (screenWidth*0.55)*2:
        pygame.draw.rect(screen, (160, 160, 160),[(screenWidth - screenWidth*0.55)/2, ((screenHeight - screenHeight*0.6)/2) + screenHeight*0.08, screenWidth*0.55, (screenHeight*0.08)*3])
    elif ComicSansTiny.size(textInput)[0] >= screenWidth*0.55:
        pygame.draw.rect(screen, (160, 160, 160),[(screenWidth - screenWidth*0.55)/2, ((screenHeight - screenHeight*0.6)/2) + screenHeight*0.08, screenWidth*0.55, (screenHeight*0.08)*2])
    else:
        pygame.draw.rect(screen, (160, 160, 160),[(screenWidth - screenWidth*0.55)/2, ((screenHeight - screenHeight*0.6)/2) + screenHeight*0.08, screenWidth*0.55, screenHeight*0.08])
    
    screen.blit((ComicSansSmall.render(topMessage, antialiasing, (0,0,0))), [(screenWidth/4.3), screenHeight*0.215])

    screen.blit((ComicSansTiny.render(textInput, antialiasing, (0,0,0))), [(screenWidth/4.3), screenHeight*0.29])

    if math.floor(time.time()) % 2 == 0:
        screen.blit((ComicSansTiny.render("|", antialiasing, (0,0,0))), [(screenWidth/4.3) + ComicSansTiny.size(textInput)[0], screenHeight*0.29])

def makeButton(XPos, YPos, XSize, YSize, textModifX, textModifY, textValue, font, p_mousePos, textColour=(0,0,0), surface=screen, colourNormal=buttonColour, colourHover=lightButtonColour, textStyle=pcl.text.centred):
    # surface,  colour,  [  X Position,  Y Position,  X Size,  Y Size  ]
    # pygame.draw.rect(screen, lightButtonColour,[screenWidth/2 - buttonSizeX/2, screenHeight/2 - buttonSizeY/2, buttonSizeX, buttonSizeY])

    if onButton(XPos, YPos, XSize, YSize, p_mousePos):
        pygame.draw.rect(surface, colourHover,[XPos, YPos, XSize, YSize])
        if textStyle == pcl.text.left:
            screen.blit(font.render(textValue, antialiasing, textColour), (XPos + screenWidth/textModifX, YPos - screenHeight/textModifY))
        elif textStyle == pcl.text.centred:
            screen.blit(font.render(textValue, antialiasing, textColour), (XPos + XSize/2 - font.size(textValue)[0]/2, YPos - screenHeight/textModifY))
    
    else:
        pygame.draw.rect(screen, colourNormal,[XPos, YPos, XSize, YSize])
        if textStyle == pcl.text.left:
            screen.blit(font.render(textValue, antialiasing, textColour), (XPos + screenWidth/textModifX, YPos - screenHeight/textModifY))
        elif textStyle == pcl.text.centred:
            screen.blit(font.render(textValue, antialiasing, textColour), (XPos + XSize/2 - font.size(textValue)[0]/2, YPos - screenHeight/textModifY))

def onButton(XPos, YPos, XSize, YSize, p_mousePos):
    # if   X Position   <=   mousePosX   <=   X Position   +   X Size   and   Y Position   <=   mousePosY   <=   Y Position   +   Y Size
    # if screenWidth/2 - buttonSizeX/2 <= mousePos[0] <= screenWidth/2 - buttonSizeX/2 + buttonSizeX and screenHeight/2 - buttonSizeY/2 <= mousePos[1] <= screenHeight/2 - buttonSizeY/2 + buttonSizeY:

    if XPos <= p_mousePos[0] <= XPos + XSize and YPos <= p_mousePos[1] <= YPos + YSize:
        return True
    else:
        return False

# - Buttons - #

menuButtonSizeX = 2*(screenWidth/3.5)
menuButtonSizeY = (screenHeight/9.5)/1.2

# --- Game Variables --- #

shopMenuPage = 1

if os.path.exists("data/savedata/pythons.txt"):
    pythonFile = open("data/savedata/pythons.txt","r")
    pythonsList = pythonFile.readlines()
    pythonFile.close()

    for i in range(len(pythonsList)):
        x = gf.NoSlashN(pythonsList[i])
        if x == "":
            pythons = 0
            break
        pythons = int(x)
else:
    pythons = 0

# --- Game Loop --- #

running = True

lastRunTime = int(time.time())

while running:

    deltatime = int(time.time()) - lastRunTime

    multipleOptionShop = None

    informationButton = None

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # --- Python Button --- #
            if not isSettingsOpen and not isInformationMenuOpen and not isShopMenuOpen:
                if onButton(screenWidth/2 - buttonSizeX/2, screenHeight/2 - buttonSizeY/2, buttonSizeX, buttonSizeY, mousePos):
                    pythons += 1
                
                if onButton(screenWidth - buttonSizeX/1.2, screenHeight/30 - buttonSizeY/4.2, buttonSizeX/1.4, buttonSizeY/1.5, mousePos):
                    isSettingsOpen = True

                if onButton(screenWidth - buttonSizeX/1.5, screenHeight/1.06 - buttonSizeY/4.2, buttonSizeX/1.86, buttonSizeY/1.5, mousePos):
                    print("indev")
                
                if onButton(screenWidth/30, screenHeight/1.06 - buttonSizeY/4.2, buttonSizeX/2, buttonSizeY/1.5, mousePos):
                    isShopMenuOpen = True

            # --- Settings Buttons --- #

            if isSettingsOpen:

                # - Resolution - #

                if resolutionsMenu:
                    if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.2, menuButtonSizeX, menuButtonSizeY, mousePos):
                        settingsResolutionEdit(200, 200)

                    if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.1, menuButtonSizeX, menuButtonSizeY, mousePos):
                        settingsResolutionEdit(300, 300)

                    if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.0, menuButtonSizeX, menuButtonSizeY, mousePos):
                        settingsResolutionEdit(500, 500)

                    if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.1, menuButtonSizeX, menuButtonSizeY, mousePos):
                        settingsResolutionEdit(800, 800)

                    if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.2, menuButtonSizeX, menuButtonSizeY, mousePos):
                        settingsResolutionEdit(1000, 1000)

                    if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.3, menuButtonSizeX, menuButtonSizeY, mousePos):
                        resolutionsMenu = False

                elif textMenu:
                    if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.2, menuButtonSizeX, menuButtonSizeY, mousePos):
                        settingsTextEdit("antialiasing", not antialiasing)
                        antialiasing = not antialiasing

                    if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.1, menuButtonSizeX, menuButtonSizeY, mousePos):
                        settingsTextEdit("abbreviate", not abbreviate)
                        abbreviate = not abbreviate

                    if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.0, menuButtonSizeX, menuButtonSizeY, mousePos):
                        textMenu = False

                else:
                    if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.2, menuButtonSizeX, menuButtonSizeY, mousePos):
                        print("hi")

                    if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.1, menuButtonSizeX, menuButtonSizeY, mousePos):
                        firstSelect = True
                        isCreateSaveMenuOpen = True
                        takingTextInput = True
                        fileInput = True
                        isSettingsOpen = False
                        if os.path.exists("data/savedata/pythons.txt"):
                            gf.editFile("data/savedata/pythons.txt", 0, str(pythons))
                        else:
                            pythonFile = open("data/savedata/pythons.txt", "w")
                            pythonFile.write(str(pythons))
                            pythonFile.close()

                    if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.0, menuButtonSizeX, menuButtonSizeY, mousePos):
                        running = False

                    if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.1, menuButtonSizeX, menuButtonSizeY, mousePos):
                        resolutionsMenu =  True
                    
                    if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.2, menuButtonSizeX, menuButtonSizeY, mousePos):
                        textMenu =  True
                    
                    if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.3, menuButtonSizeX, menuButtonSizeY, mousePos):
                        isSettingsOpen = False

            # --- Shop Menu --- #
            
            if isShopMenuOpen:
                multipleOptionShop = multipleOptionInput(gf.addToTempList(list(itemsList.keys()), "EXIT"), shopMenuPage)

            if isInformationMenuOpen:
                informationButton = informationInput()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            keysDown = pygame.key.get_pressed()

            if isKeybindDown("Back",keysDown):
                if not takingTextInput:
                    if isInformationMenuOpen:
                        isInformationMenuOpen = False
                    elif isShopMenuOpen:
                        isShopMenuOpen = False
                    else:
                        isSettingsOpen = not isSettingsOpen
                else:
                    takingTextInput = False
                    dirtyStop = True
            elif takingTextInput:
                if isKeybindDown("Paste",keysDown):
                    print(textInput)
                    paste = pyperclip.paste()
                    textInput += paste
                elif event.key == pygame.K_BACKSPACE:
                    textInput = textInput[:-1]
                elif event.key == pygame.K_RETURN:
                    takingTextInput = False
                    dirtyStop = False
                elif event.unicode != "":
                    if fileInput:
                        if not event.unicode in ["#","!",'"',"'","%","&","<",">","*","?","/","|","\\",":","`"]:
                            textInput += event.unicode
                    else:
                        textInput += event.unicode
            elif isKeybindDown("ShopMenu", keysDown) and not isSettingsOpen:
                shopMenuPage = 1
                isShopMenuOpen = not isShopMenuOpen
                if isInformationMenuOpen:
                    isInformationMenuOpen = False
                    isShopMenuOpen = False
            elif isKeybindDown("KeyboardTest",keysDown) and debug:
                takingTextInput = not takingTextInput
            elif isKeybindDown("EnableDebug",keysDown):
                debug = not debug
                print("debug")
                settingsTextEdit("debug", debug)
            elif isKeybindDown("Prev",keysDown):
                if shopMenuPage != 1:
                    multipleOptionShop = pcl.menus.prevpage
            elif isKeybindDown("Next",keysDown):
                if totalButtonPages(gf.addToTempList(list(itemsList.keys()), "EXIT")) != shopMenuPage:
                    multipleOptionShop = pcl.menus.nextpage
    
    # --- Multiple Page Menu --- #
    if isShopMenuOpen:
        if multipleOptionShop == pcl.menus.prevpage:
            shopMenuPage -= 1
        elif multipleOptionShop == pcl.menus.nextpage:
            shopMenuPage += 1
        elif multipleOptionShop == "EXIT":
            isShopMenuOpen = False
        for x in range(0, len(list(itemsList.keys()))):
            if multipleOptionShop == list(itemsList.keys())[x]:
                informationMenu(multipleOptionShop)
                informationMenuContents = multipleOptionShop
                isInformationMenuOpen = True
    
    if isInformationMenuOpen:
        if informationButton == pcl.menus.prevpage:
            isShopMenuOpen = True
            isInformationMenuOpen = False

    # --- Screen Size --- #

    screen, screenWidth, screenHeight, resolutionChanged = resetResolution(screen, screenWidth, screenHeight)
    if resolutionChanged:
        menuButtonSizeX = 2*(screenWidth/3.5)
        menuButtonSizeY = (screenHeight/9.5)/1.2

        buttonSizeX = screenWidth/3.5
        buttonSizeY = screenHeight/9.5

        largefontsize = ((screenHeight + screenWidth)/2)/7.1
        bigfontsize = ((screenHeight + screenWidth)/2)/10.65
        mediumfontsize = ((screenHeight + screenWidth)/2)/14.2
        smallfontsize = ((screenHeight + screenWidth)/2)/21.3
        tinyfontsize = ((screenHeight + screenWidth)/2)/28.4

        ComicSansLarge = pygame.font.Font('data/Comic Sans MS.ttf', round(largefontsize))
        ComicSansBig = pygame.font.Font('data/Comic Sans MS.ttf', round(bigfontsize))
        ComicSansMedium = pygame.font.Font('data/Comic Sans MS.ttf', round(mediumfontsize))
        ComicSansSmall = pygame.font.Font('data/Comic Sans MS.ttf', round(smallfontsize))
        ComicSansTiny = pygame.font.Font('data/Comic Sans MS.ttf', round(tinyfontsize))

    # --- Variables --- #

    mousePos = pygame.mouse.get_pos()

    # --- Calculations --- #

    # --- Screen Management --- #

    screen.fill((255,255,255))

    # - Python Amount Text - #

    screen.blit((ComicSansSmall.render('pythons: ' + gf.NumberToText(pythons, abbreviated=abbreviate), antialiasing, (0,0,0))), [screenWidth/40,0])

    # --- Button Rendering --- #

    makeButton(screenWidth/2 - buttonSizeX/2, screenHeight/2 - buttonSizeY/2, buttonSizeX, buttonSizeY, 30, 175, "python", ComicSansMedium, mousePos)

    makeButton(screenWidth/30, screenHeight/1.06 - buttonSizeY/4.2, buttonSizeX/2, buttonSizeY/1.5, 85, 270, "Shop", ComicSansSmall, mousePos, colourNormal=(200, 200, 200),colourHover=(200, 200, 200))

    makeButton(screenWidth - buttonSizeX/1.5, screenHeight/1.06 - buttonSizeY/4.2, buttonSizeX/1.86, buttonSizeY/1.5, 85, 270, "Items", ComicSansSmall, mousePos, colourNormal=(200, 200, 200),colourHover=(210, 210, 210))

    makeButton(screenWidth - buttonSizeX/1.2, screenHeight/30 - buttonSizeY/4.2, buttonSizeX/1.4, buttonSizeY/1.5, 85, 270, "Settings", ComicSansSmall, mousePos, colourNormal=(200, 200, 200),colourHover=(210, 210, 210))

    # --- Menu Rendering --- #

    screen.blit((ComicSansTiny.render(textInput, antialiasing, (0,0,0))), [screenWidth/2.6,screenHeight*0.1])

    # -- Settings -- #

    if textMenu and resolutionsMenu:
        resolutionsMenu = False
        textMenu = False

    if isCreateSaveMenuOpen:
        takeInput("Enter Save Name")
        firstSelect = False
        if takingTextInput == False:
            if not dirtyStop:
                createSave(textInput)
            isCreateSaveMenuOpen = False
            textInput = ""
            fileInput = False


    if isShopMenuOpen:
        multipleOptionMenu(gf.addToTempList(list(itemsList.keys()), "EXIT"),shopMenuPage,"Shop")
    
    if isInformationMenuOpen:
        isShopMenuOpen = False
        informationMenu(informationMenuContents)

    if isSettingsOpen:
        openMenu(bgcolour=(220,220,220))

        # - Resolution Menu - #
        
        if resolutionsMenu:

            makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.2, menuButtonSizeX, menuButtonSizeY, 40, -100, "Resolution - 200x200", ComicSansSmall, mousePos)

            makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.1, menuButtonSizeX, menuButtonSizeY, 40, -100, "Resolution - 300x300", ComicSansSmall, mousePos)

            makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.0, menuButtonSizeX, menuButtonSizeY, 40, -100, "Resolution - 500x500", ComicSansSmall, mousePos)

            makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.1, menuButtonSizeX, menuButtonSizeY, 40, -100, "Resolution - 800x800", ComicSansSmall, mousePos)

            makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.2, menuButtonSizeX, menuButtonSizeY, 40, -100, "Resolution - 1000x1000", ComicSansSmall, mousePos)

            makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.3, menuButtonSizeX, menuButtonSizeY, 40, -100, "Back To Settings", ComicSansSmall, mousePos)

            screen.blit((ComicSansTiny.render('Resolution:', antialiasing, (0,0,0))), [screenWidth/2.6,screenHeight*0.1])
            
        # - Text Menu - #

        elif textMenu:

            isAntialiasing = "on" if antialiasing == True else "off"

            isAbbreviating = "on" if abbreviate == True else "off"

            if lying:
                isAntialiasing = "off" if antialiasing == True else "on"

                isAbbreviating = "off" if abbreviate == True else "on"

            makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.2, menuButtonSizeX, menuButtonSizeY, 40, -100, "Antialiasing - " + isAntialiasing, ComicSansSmall, mousePos)
    
            makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.1, menuButtonSizeX, menuButtonSizeY, 40, -80, "Abbreviate Numbers - " + isAbbreviating, ComicSansCustomSize(23), mousePos)
    
            makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.0, menuButtonSizeX, menuButtonSizeY, 40, -100, "Back To Settings", ComicSansSmall, mousePos)
    
            screen.blit((ComicSansTiny.render('Text Settings:', antialiasing, (0,0,0))), [screenWidth/2.6,screenHeight*0.1])
        
        # - Main Settings Menu - #
        
        else:
            makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.2, menuButtonSizeX, menuButtonSizeY, 40, -100, "Load Save", ComicSansSmall, mousePos, textStyle=pcl.text.centred)

            makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.1, menuButtonSizeX, menuButtonSizeY, 40, -100, "Create Save", ComicSansSmall, mousePos, textStyle=pcl.text.centred)

            makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.0, menuButtonSizeX, menuButtonSizeY, 40, -100, "Leave Game", ComicSansSmall, mousePos)

            makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.1, menuButtonSizeX, menuButtonSizeY, 40, -100, "Change Resolution", ComicSansSmall, mousePos)

            makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.2, menuButtonSizeX, menuButtonSizeY, 40, -100, "Text Settings", ComicSansSmall, mousePos)

            makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.3, menuButtonSizeX, menuButtonSizeY, 40, -100, "Close Settings", ComicSansSmall, mousePos)
            
            screen.blit((ComicSansTiny.render('Game Settings:', antialiasing, (0,0,0))), [screenWidth/2.6,screenHeight*0.1])

    lastRunTime = int(time.time())

    pygame.display.update()

pygame.quit()