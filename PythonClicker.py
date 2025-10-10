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

def createSave(saveName: str, p_saveData):
    if saveName in DISSALLOWEDFILENAMES:
        return None

    shutil.copy(pcl.filesDir.templateSaveFile, "data/savedata/" + saveName + ".json")

    if p_saveData != None:
        save = open("data/savedata/" + saveName + ".json","w")

        json.dump(p_saveData, save, indent=4)

        save.close()

def saveList(forDisplay):
    if forDisplay:
        return gf.returnFilesInFolder("data/savedata/",".json",False,False)
    else:
        return gf.returnFilesInFolder("data/savedata/",".json",True,True)

def loadSave(saveName: str, justName = False):
    if justName:
        save = open("data/savedata/" + saveName + ".json", "r")
    else:
        save = open(saveName, "r")
    jsonData = json.load(save)

    return jsonData

def updateSave(saveName: str, p_saveData):
    if saveName in DISSALLOWEDFILENAMES:
        return None
    
    if not os.path.exists("data/savedata/" + saveName + ".json"):
        return None

    save = open("data/savedata/" + saveName + ".json","w")

    json.dump(p_saveData, save, indent=4)

    save.close()

# -- Item Data -- #

def retrieveByTag(TAG,commit,type="Name",menuLeaveMessage="Leave Shop"):
    if not commit:
        return TAG
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

    autosaveDelay = jsonData["autosaveDelay"]

    lying = jsonData["funstuff"]["lying"]

else:
    debug = False

    screenWidth = 500
    screenHeight = 500

    antialiasing = True
    abbreviate = False

    autosaveDelay = 10

    jsonData = {
        "debug": False,
        "autosaveDelay": 10,
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

# -- Save Data -- #

if os.path.exists("data/savedata/autosave.json"):
    saveData = loadSave("autosave", True)
else:
    createSave("autosave", None)
    saveData = loadSave("autosave", True)

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

isShopMenuOpen = False

isInformationMenuOpen = False
informationMenuContents = "WRA"
informationButton = None

isProducerShopMenuOpen = False

isCreateSaveMenuOpen = False
isLoadSaveMenuOpen = False

# - Subprograms - #

def openMenu(colour=(170,170,170),bg=True,bgcolour=(220,220,220)):
    if bg:
        pygame.draw.rect(screen, bgcolour,[0,0, screenWidth, screenHeight])
    pygame.draw.rect(screen, colour,[(screenWidth - screenWidth*0.6)/2, ((screenHeight - screenHeight*0.75)/2) + screenHeight*0.08, screenWidth*0.6, screenHeight*0.6])

def closableOpenMenu(colour=(170,170,170),bg=True,bgcolour=(220,220,220)):
    if bg:
        pygame.draw.rect(screen, bgcolour,[0,0, screenWidth, screenHeight])
    pygame.draw.rect(screen, colour,[(screenWidth - screenWidth*0.6)/2, ((screenHeight - screenHeight*0.85)/2) + screenHeight*0.08, screenWidth*0.6, screenHeight*0.65])

def multipleOptionMenu(buttonsList,buttonPage,menuName="",visible=True,byTAG=False,bg=False):
    if visible:
        closableOpenMenu(bg=bg)

        makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.3, menuButtonSizeX/3, menuButtonSizeY, 40, -100, "Back", ComicSansSmall, mousePos)
        makeButton((screenWidth - menuButtonSizeX)/2 + menuButtonSizeX/1.5, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.3, menuButtonSizeX/3, menuButtonSizeY, 40, -100, "Next", ComicSansSmall, mousePos)

        makeButton((screenWidth - menuButtonSizeX) + menuButtonSizeX/1.5, (menuButtonSizeY) - screenHeight*-0.07, menuButtonSizeX/9, menuButtonSizeY/1.2, 40, -10000, "x", ComicSansSmall, mousePos)

        if len(buttonsList) > 0:
            makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.2, menuButtonSizeX, menuButtonSizeY, 40, -100, retrieveByTag(buttonsList[(buttonPage - 1)*5 + 0], byTAG), ComicSansSmall, mousePos)
    
        if len(buttonsList) - (buttonPage - 1)*5 + 0 > 1:
            makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.1, menuButtonSizeX, menuButtonSizeY, 40, -100, retrieveByTag(buttonsList[(buttonPage - 1)*5 + 1], byTAG), ComicSansSmall, mousePos)
        if len(buttonsList) - (buttonPage - 1)*5 + 0 > 2:
            makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.0, menuButtonSizeX, menuButtonSizeY, 40, -100, retrieveByTag(buttonsList[(buttonPage - 1)*5 + 2], byTAG), ComicSansSmall, mousePos)
        if len(buttonsList) - (buttonPage - 1)*5 + 0 > 3:
            makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.1, menuButtonSizeX, menuButtonSizeY, 40, -100, retrieveByTag(buttonsList[(buttonPage - 1)*5 + 3], byTAG), ComicSansSmall, mousePos)
        if len(buttonsList) - (buttonPage - 1)*5 + 0 > 4:
            makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.2, menuButtonSizeX, menuButtonSizeY, 40, -100, retrieveByTag(buttonsList[(buttonPage - 1)*5 + 4], byTAG), ComicSansSmall, mousePos)

        screen.blit((ComicSansTiny.render(menuName, antialiasing, (0,0,0))), [(screenWidth/2) - ComicSansTiny.size(menuName)[0]/2,screenHeight*0.15])

        tbp = totalButtonPages(buttonsList)

        if tbp == 0:
            tbp = 1

        screen.blit(ComicSansTiny.render(str(buttonPage) + " / " + str(tbp), antialiasing, (0,0,0)), [screenWidth/2.15,screenHeight*0.73])

def multipleOptionInput(buttonsList,buttonPage):
    #Previous Page
    if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.3, menuButtonSizeX/3, menuButtonSizeY, mousePos):
        if buttonPage != 1:
            return pcl.menus.prevpage
    #Next Page
    if onButton((screenWidth - menuButtonSizeX)/2 + menuButtonSizeX/1.5, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.3, menuButtonSizeX/3, menuButtonSizeY, mousePos):
        tbp = totalButtonPages(buttonsList)

        if tbp == 0:
            tbp = 1
        
        if tbp != buttonPage:
            return pcl.menus.nextpage
    
    #Close Menu
    if onButton((screenWidth - menuButtonSizeX) + menuButtonSizeX/1.5, (menuButtonSizeY) - screenHeight*-0.07, menuButtonSizeX/9, menuButtonSizeY/1.2, mousePos):
        return pcl.menus.close
    
    #Buttons 0-4
    if len(buttonsList) > 0 and onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.2, menuButtonSizeX, menuButtonSizeY, mousePos):
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

def informationMenu(TAG,visible=True):
    if visible:
        openMenu(bg=False)

        pygame.draw.rect(screen, (160, 160, 160),[(screenWidth - screenWidth*0.55)/2, ((screenHeight - screenHeight*0.45)/2) + screenHeight*0.08, screenWidth*0.55, screenHeight*0.342])

        pygame.draw.rect(screen, (160, 160, 160),[(screenWidth - screenWidth*0.55)/2, ((screenHeight - screenHeight*0.72)/2) + screenHeight*0.08, screenWidth*0.55, screenHeight*0.12])

        makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.3, menuButtonSizeX/3, menuButtonSizeY, 40, -100, "Shop", ComicSansSmall, mousePos)
        makeButton((screenWidth - menuButtonSizeX)/2 + menuButtonSizeX/1.5, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.3, menuButtonSizeX/3, menuButtonSizeY, 40, -100, "Buy", ComicSansSmall, mousePos)

        screen.blit((ComicSansSmall.render(retrieveByTag(TAG,commit=True), antialiasing, (0,0,0))), [(screenWidth/4.3), screenHeight*0.215])

        screen.blit((ComicSansTiny.render(str(retrieveByTag(TAG,type="Price",commit=True))  + " Pythons", antialiasing, (0,0,0))), [(screenWidth/4.3), screenHeight*0.29])

        screen.blit((ComicSansTiny.render(retrieveByTag(TAG,type="Description",commit=True), antialiasing, (0,0,0))), [(screenWidth/4.3), screenHeight*0.35])

def informationInput():
    #Go back
    if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.3, menuButtonSizeX/3, menuButtonSizeY, mousePos):
        return pcl.menus.back
    #Buy item
    if onButton((screenWidth - menuButtonSizeX)/2 + menuButtonSizeX/1.5, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.3, menuButtonSizeX/3, menuButtonSizeY, mousePos):
        return pcl.menus.buy
    
    return None

def loadSaveMenu(saveMenuPage):
    multipleOptionMenu(saveList(True),saveMenuPage,"Load Save",bg=True)

def wrappedText(font,text,XPosOffset,MaxXSize):
    counting = 0
    if font.size(text)[x] > MaxXSize:
        print("")
    for x in range(0,1):
        print("")

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

loadSaveMenuPage = 1
shopMenuPage = 1

# --- Game Loop --- #

autosaveTimer = 0

running = True

lastRunTime = int(time.time())

while running:

    deltatime = int(time.time()) - lastRunTime

    autosaveTimer += deltatime

    multipleOptionShop = None

    multipleOptionLoad = None

    informationButton = None

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # --- Python Button --- #
            if not isSettingsOpen and not isInformationMenuOpen and not isProducerShopMenuOpen and not isShopMenuOpen:
                if onButton(screenWidth/2 - buttonSizeX/2, screenHeight/2 - buttonSizeY/2, buttonSizeX, buttonSizeY, mousePos):
                    saveData["Pythons"] += 1
                
                if onButton(screenWidth - buttonSizeX/1.2, screenHeight/30 - buttonSizeY/4.2, buttonSizeX/1.4, buttonSizeY/1.5, mousePos):
                    isSettingsOpen = True

                if onButton(screenWidth - buttonSizeX/1.5, screenHeight/1.06 - buttonSizeY/4.2, buttonSizeX/1.86, buttonSizeY/1.5, mousePos):
                    print("indev")
                
                if onButton(screenWidth/30, screenHeight/1.06 - buttonSizeY/4.2, buttonSizeX/2, buttonSizeY/1.5, mousePos):
                    isShopMenuOpen = True

            # --- Multiple Option Menu --- #
            
            if isProducerShopMenuOpen:
                multipleOptionShop = multipleOptionInput(list(itemsList.keys()), shopMenuPage)

            if isLoadSaveMenuOpen:
                multipleOptionLoad = multipleOptionInput(saveList(False),loadSaveMenuPage)

            if isInformationMenuOpen:
                informationButton = informationInput()

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
                        isLoadSaveMenuOpen = True
                        isSettingsOpen = False

                    if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.1, menuButtonSizeX, menuButtonSizeY, mousePos):
                        firstSelect = True
                        isCreateSaveMenuOpen = True
                        takingTextInput = True
                        fileInput = True
                        isSettingsOpen = False

                    if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.0, menuButtonSizeX, menuButtonSizeY, mousePos):
                        running = False

                    if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.1, menuButtonSizeX, menuButtonSizeY, mousePos):
                        resolutionsMenu =  True
                    
                    if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.2, menuButtonSizeX, menuButtonSizeY, mousePos):
                        textMenu =  True
                    
                    if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.3, menuButtonSizeX, menuButtonSizeY, mousePos):
                        isSettingsOpen = False
            elif isShopMenuOpen:
                if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.2, menuButtonSizeX, menuButtonSizeY, mousePos):
                    isProducerShopMenuOpen = True
                    isShopMenuOpen = False
                
                if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.1, menuButtonSizeX, menuButtonSizeY, mousePos):
                    print("Indev")
                
                if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.0, menuButtonSizeX, menuButtonSizeY, mousePos):
                    print("Indev")
                
                if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.1, menuButtonSizeX, menuButtonSizeY, mousePos):
                    print("Indev")
                
                if onButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.2, menuButtonSizeX, menuButtonSizeY, mousePos):
                    isShopMenuOpen = False

        if event.type == pygame.QUIT:
            updateSave("autosave",saveData)
            print("autosave")
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            keysDown = pygame.key.get_pressed()

            if isKeybindDown("Back",keysDown):
                if not takingTextInput:
                    if isInformationMenuOpen:
                        isInformationMenuOpen = False
                    elif isProducerShopMenuOpen:
                        isProducerShopMenuOpen = False
                    elif isShopMenuOpen:
                        isShopMenuOpen = False
                    elif isLoadSaveMenuOpen:
                        isLoadSaveMenuOpen = False
                        isSettingsOpen = True
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
                if isInformationMenuOpen or isProducerShopMenuOpen:
                    isInformationMenuOpen = False
                    isProducerShopMenuOpen = False
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
                if loadSaveMenuPage != 1:
                    multipleOptionLoad = pcl.menus.prevpage
            elif isKeybindDown("Next",keysDown):
                tbp = totalButtonPages(itemsList.keys())
                if tbp == 0:
                    tbp = 1
                if tbp != shopMenuPage:
                    multipleOptionShop = pcl.menus.nextpage
                
                tbp = totalButtonPages(saveList(True))
                if tbp == 0:
                    tbp = 1
                if tbp != loadSaveMenuPage:
                    multipleOptionLoad = pcl.menus.nextpage
    
    # --- Multiple Page Menu --- #
    if isProducerShopMenuOpen:
        if multipleOptionShop == pcl.menus.prevpage:
            shopMenuPage -= 1
        elif multipleOptionShop == pcl.menus.nextpage:
            shopMenuPage += 1
        elif multipleOptionShop == "EXIT":
            isProducerShopMenuOpen = False
        for x in range(0, len(list(itemsList.keys()))):
            if multipleOptionShop == list(itemsList.keys())[x]:
                informationMenu(multipleOptionShop)
                informationMenuContents = multipleOptionShop
                isInformationMenuOpen = True

    if isLoadSaveMenuOpen:
        if multipleOptionLoad == pcl.menus.prevpage:
            loadSaveMenuPage -= 1
        elif multipleOptionLoad == pcl.menus.nextpage:
            loadSaveMenuPage += 1
        elif multipleOptionLoad == "EXIT":
            isLoadSaveMenuOpen = False
        elif isinstance(multipleOptionLoad, str):
            saveData = loadSave(multipleOptionLoad)

            isLoadSaveMenuOpen = False
    
    if isInformationMenuOpen:
        if informationButton == pcl.menus.back or informationButton == pcl.menus.close:
            isProducerShopMenuOpen = True
            isInformationMenuOpen = False
        if informationButton == pcl.menus.buy:
            if saveData["Pythons"] >= retrieveByTag(informationMenuContents,True,type="Price"):
                saveData["Pythons"] -= retrieveByTag(informationMenuContents,True,type="Price")

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

    screen.blit((ComicSansSmall.render('pythons: ' + gf.NumberToText(saveData["Pythons"], abbreviated=abbreviate), antialiasing, (0,0,0))), [screenWidth/40,0])

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
                createSave(textInput, saveData)
            isCreateSaveMenuOpen = False
            textInput = ""
            fileInput = False

    if isLoadSaveMenuOpen:
        loadSaveMenu(loadSaveMenuPage)

    if isShopMenuOpen:
        openMenu(bg = False)

        makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.2, menuButtonSizeX, menuButtonSizeY, 40, -100, "Producers", ComicSansSmall, mousePos)

        makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.1, menuButtonSizeX, menuButtonSizeY, 40, -100, "Upgrades", ComicSansSmall, mousePos)

        makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*0.0, menuButtonSizeX, menuButtonSizeY, 40, -100, "Items", ComicSansSmall, mousePos)
        
        makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.1, menuButtonSizeX, menuButtonSizeY, 40, -100, "Decorations", ComicSansSmall, mousePos)

        makeButton((screenWidth - menuButtonSizeX)/2, (screenHeight/2 - menuButtonSizeY) - screenHeight*-0.2, menuButtonSizeX, menuButtonSizeY, 40, -100, "Leave Shop", ComicSansSmall, mousePos)

        screen.blit((ComicSansTiny.render('Shop:', antialiasing, (0,0,0))), [screenWidth/2 - ComicSansTiny.size("Shop:")[0]/2,screenHeight*0.1])

    if isProducerShopMenuOpen:
        multipleOptionMenu(list(itemsList.keys()),shopMenuPage,"Producer Shop",byTAG=True)
    
    if isInformationMenuOpen:
        isProducerShopMenuOpen = False
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
    if autosaveDelay > 0:
        if autosaveTimer >= autosaveDelay:
            updateSave("autosave",saveData)
            print("autosave")
            autosaveTimer = 0

    lastRunTime = int(time.time())

    pygame.display.update()

pygame.quit()