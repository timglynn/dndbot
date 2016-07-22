#!/usr/bin/env python


import random
import time
import requests
from bs4 import BeautifulSoup
import redis


def parseInput(rawCommand, cache):
    """Takes a raw command.  Parses for available responses"""
    commandList = rawCommand.split()
    if commandList[0].lower() == "roll":
        return_string = parseRoll(commandList)
        return(return_string)


    elif commandList[0].lower() == "weapon":
        commandString = cleanCommandList(commandList)
        return_string = getWeaponInfo(commandString)
        return return_string


    elif commandList[0].lower() == "armor":
        commandString = cleanCommandList(commandList)
        return_string = getArmorInfo(commandString)
        return return_string

    elif commandList[0].lower() == "spell":
        commandString = cleanCommandList(commandList)
        return_string = getSpellInfo(commandString, cache)
        return return_string

    # Return the help string

    else:
    
        return_string = "Hi! I'm dndbot.  Here's what I can do: \n" +\
                "Roll some die (`@dndbot roll 4d4`) \n" +\
                "Tell you about regular weapons (weapon broadsword or `weapon showall`)" +\
                "\n" +\
                "Tell you about regular armor (`armor hide` or `armor showall`)" +\
                "\n" +\
                "Tell you about spells (`spell fireball` or `spell Dispel Magic`)" +\
                "\n"
    
        return return_string



def parseRoll(commandList):
    """ Takes a list of command words.  Parses them, calls the required 
    rolling functions"""

        # Remove the command "roll"
    del commandList[0]
    
    # Let's allow "a" for the singular
    if commandList[0] == "a":
        del commandList[0]
        tmpVar = commandList[0]
        commandList[0] = "1" + tmpVar
        commandString = commandList[0]
    elif len(commandList) == 1:
        commandString = commandList[0]


    else:
        try:
            int(commandList[0])
            # Let's squish them all together
            commandString = str()
            for item in commandList:
                commandString = commandString + item
        except:
            return_string = "I'm not sure what to roll."
            return(return_string)
        
    return_string = rollSomeDie(commandString)  
    return(return_string)



def cleanCommandList(commandList):
    """ Takes a list of command words.  Parses them, formats the string
    to call the info functions"""

    # Pop off the command word
    del commandList[0]
    commandString = ""
    for item in commandList:
        commandString = commandString + item + " "
    
    return(commandString)




def rollSomeDie(dieCommand):
    """ Takes a string of a partial command, determines how many die to roll.
    Returns the result """
    help_string = " Rolling Die: \n" +\
            "Expected syntax is something like \n" +\
            "roll 4d6 \n" +\
            "or \n" + \
            "roll a d20"
    dieList = dieCommand.split('d')
    if len(dieList) == 2:
        if dieList[0] == "":
            return_string = "Rolled 1d"+ str(dieList[1]) + "\n" + "Result: " \
                + str(getDieResult(int(dieList[1])))
            return return_string
        elif int(dieList[0]):
            total = 0
            each_result = list()
            for x in range(0,int(dieList[0])):
                intermediate_result = getDieResult(int(dieList[1]))
                total = total + intermediate_result
                each_result.append(intermediate_result)
            return_string = "Rolled " + dieList[0] + "d" + dieList[1] + \
                "\n" + "Each result is: " + str(each_result) + "\n" + \
                "Total is: " + str(total) + "\n"
            return return_string
        else:
            return help_string
    else:
        return help_string


def getDieResult(dieNumber):
    """ Rolls a d$dieNumber die and returns the result """
    dieNumber = dieNumber + 1
    dieResult = random.randrange(1,dieNumber)
    return dieResult



def buildWeaponDictFromFile(weaponDict, fileName):
    """ Takes an existing weapon dict, a file with a dict dump from 
    the public d and d wepaons page.  Returns the weaponDict"""


    with open(fileName) as weapondata:
        rawcontent = weapondata.read()
        newDict = eval(rawcontent)
        weapondata.close()
        for key in newDict:
            newDict[key.lower()] = newDict.pop(key)
        returning_dict = dict(weaponDict.items() + newDict.items())
        return returning_dict


def getAllWeaponTypes():
    allWeapons = dict()
    allWeapons = buildWeaponDictFromFile(allWeapons, "./weapons/simplemelee.txt")
    allWeapons = buildWeaponDictFromFile(allWeapons, "./weapons/simpleranged.txt")
    allWeapons = buildWeaponDictFromFile(allWeapons, "./weapons/martialmelee.txt")
    allWeapons = buildWeaponDictFromFile(allWeapons, "./weapons/martialranged.txt")
    return allWeapons


def getWeaponInfo(commandString):
    commandString = commandString.strip()
    # First, build the weapon dict
    allWeapons = getAllWeaponTypes()
    if commandString.lower() == "showall":
        return_string = ""
        for weapon in allWeapons:
            return_string = return_string + "\n" + weapon
        return return_string
    elif commandString.lower() in allWeapons: 
        return_string = "Item: " + commandString +"\n" 
        for item in allWeapons[commandString.lower()]:
            return_string = return_string + item + " : " +\
            allWeapons[commandString.lower()][item] + "\n"
        return return_string
    else:
        return_string = "Hmm, I'm not sure I know that item"
        return return_string

def getArmorInfo(commandString):
    commandString = commandString.strip()
    # First, build the armor dict
    allArmor = getAllArmorTypes()
    if commandString.lower() == "showall":
        return_string = ""
        for armor in allArmor:
            return_string = return_string + "\n" + armor
        return return_string
    elif commandString.lower() in allArmor: 
        return_string = "Item: " + commandString +"\n" 
        for item in allArmor[commandString.lower()]:
            return_string = return_string + item + " : " +\
            allArmor[commandString.lower()][item] + "\n"
            
        return return_string
    else:
        return_string = "Hmm, I'm not sure I know that item"
        return return_string

def buildArmorDictFromFile(armorDict, fileName):
    """ Takes an existing armor dict, a file with a dict dump from 
    the public d and d armor page.  Returns the armorDict"""


    with open(fileName) as armordata:
        rawcontent = armordata.read()
        newDict = eval(rawcontent)
        armordata.close()
        for key in newDict:
            newDict[key.lower()] = newDict.pop(key)
        returning_dict = dict(armorDict.items() + newDict.items())
        return returning_dict


def getAllArmorTypes():
    allArmor= dict()
    allArmor= buildArmorDictFromFile(allArmor, "./armor/lightarmor.txt")
    allArmor = buildArmorDictFromFile(allArmor, "./armor/mediumarmor.txt")
    allArmor = buildArmorDictFromFile(allArmor, "./armor/heavyarmor.txt")
    return allArmor

#### Spells
def getSpellInfo(spellName, cache):
    url = "http://ephe.github.io/grimoire/spells/"
    spellName = cleanUpSpellName(spellName)
    if checkCache(cache, spellName):
        clean_output = cache.get(spellName)
    else:
        url = url + spellName
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        paragraphs = soup.find('article').find_all('p')
        clean_output = ""
        for paragraph in paragraphs:
            clean_output = clean_output + paragraph.text + "\n"
        addCache(cache, spellName, clean_output)
    return clean_output




def cleanUpSpellName(spellName):
    spellName = spellName.lower().strip()
    convertedName = ""
    for char in spellName:
        if char == " ":
            char = "-"
        else:
            pass
        convertedName = convertedName + char
    return convertedName


def checkCache(cache, spellName):
    """ Checks the local redis cache for spell definition"""
    if cache.exists(spellName):
        print(spellName + " is in the local cache")
        return True
    else:
        return False

def addCache(cache, spellName, spellDef):
    """ Adds a spell definition to the local redis cache """
    try:
        cache.set(spellName, spellDef)
        print("Added " + spellName + " to local cache")
    except:
        print("Cannot add to redis cache")
