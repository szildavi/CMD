import os
import subprocess

CurrentPaths = "C:/"  #Változó létrehozása a jelenlegi útvonal eltárolásához

#Jézusom félek dolgozni ezzel a projectel már xd

def check(Inputpath): #Egy fájlkezelő és ellenörző metódus, amelynek van visszaadási értéke.
    global CurrentPaths
    tmpCurrentPaths = CurrentPaths
    if Inputpath.__contains__(":/"): #Abszolút útvonal megadása esetén egyből azzal kezdje a jelenlegei útvonalat és levágja a lemezséma részét.
        if os.path.exists(Inputpath[0:3]):
            tmpCurrentPaths = Inputpath[0:3]
            Inputpath = Inputpath[3:]
        else:
            return False, Inputpath[0:3], "Undefined", ""
    if Inputpath.__contains__("/"):
        Inputpathsplitted = Inputpath.split("/")
    else:
        Inputpathsplitted = Inputpath.split("\\")
    for i in range(len(Inputpathsplitted)):
        success = 0
        tmpCurrentFiles = os.scandir(tmpCurrentPaths)
        if Inputpathsplitted[i] == ".." and tmpCurrentPaths[1:] != ":/":
            if tmpCurrentPaths.__contains__("/"):
                tmpCurrentPathsSplitted = tmpCurrentPaths.split("/")
            else:
                tmpCurrentPathsSplitted = tmpCurrentPaths.split("\\")
            tmpCurrentPathsSplitted.pop()
            tmpCurrentPathsSplitted.pop()
            tmpCurrentPaths = ""
            for i in range(len(tmpCurrentPathsSplitted)):
                tmpCurrentPaths += tmpCurrentPathsSplitted[i] + "/"
            success = 1
        if Inputpathsplitted[i] != "" and Inputpathsplitted[i] != "..":
            for entry in tmpCurrentFiles:
                if entry.is_dir() or entry.is_file():
                    Loweredpaths = Inputpathsplitted[i]
                    Loweredentry = entry.name
                    if Loweredentry.lower() == Loweredpaths.lower():  # Ellenőrzi hogy talált-e ilyen nevű mappát
                        if entry.is_file():
                            tmpCurrentPaths += entry.name  # Hozzáadja a tmp változóhoz a jelenlegi útvonalat
                        else:
                            tmpCurrentPaths += entry.name + "/"
                            tmpCurrentFiles = os.scandir(tmpCurrentPaths)  # A jelenlegi útvonal fájljait belerakja
                        success = 1  # Teljesült, tehát talált mappát, így nem fogja a folyamatot megszakítani
                        break  # Kilép a ciklusból
        else:
            success = 1
        if success == 0:
            return False, Inputpathsplitted[i], i, tmpCurrentPaths
    return True, tmpCurrentPaths, "Undefined", ""

def kiiras(writedirectory):  # Függvény a kiiratásra, amely bekéri az útvonalat amit ki kell írnia.
    checkdirectory = os.scandir(writedirectory)  # Helyi változót hoz létre a fájlok listázására
    for entry in checkdirectory:  # Ciklus a fájlok listázására
        if entry.is_dir() or entry.is_file():  # Csak akkor listázza ki ha fájl vagy mappa van ott
            print(entry.name)  # Kiiratás



def cd(InputCommand):  # Mappaelhelyesés
    global CurrentPaths  # Globálissá kell tenni a változót
    ResultIsArgument = IsArgument(InputCommand)
    Paths = ResultIsArgument[0][4:]
    CheckedPaths = check(Paths)
    if not ResultIsArgument[1] and not CheckedPaths[0]:
        print(f"A megadott mappa vagy lemezséma nem létezik/található: {CheckedPaths[1]}")
    elif ResultIsArgument[1] and not CheckedPaths[0] and CheckedPaths[2] != "Undefined":
        MakeFolders(Paths)
    elif CheckedPaths[0] == 1:
        CurrentPaths = CheckedPaths[1]
    return

def IsArgument(InputCommand):
    IsThisR = False
    WhatArgument = ""
    OutputCommand = InputCommand
    if InputCommand[-3:] == " -r":
        IsThisR = True
        OutputCommand = InputCommand[:-3]
        WhatArgument += "r"
    return OutputCommand, IsThisR, WhatArgument

def PathsCutter(InputPaths):
    if InputPaths.__contains__("/"):
        OutputPaths = InputPaths.split("/")
    else:
        OutputPaths = InputPaths.split("\\")
    return OutputPaths

def MakeFolders(InputPath):
    global CurrentPaths
    SplittedPaths = PathsCutter(InputPath)
    FoundOneMissing = False
    for Folder in SplittedPaths:
        if Folder != "":
            if not FoundOneMissing:
                CheckedFolder = check(CurrentPaths + Folder)
                if not CheckedFolder[0]:
                   FoundOneMissing = True
            if FoundOneMissing:
                CurrentPaths += Folder + "/"
                os.mkdir(CurrentPaths)
            else:
                CurrentPaths += Folder + "/"

def execute(yourcommand):
    splittedcommand = yourcommand.split(" ")
    results = check(splittedcommand[1])
    if splittedcommand[1].__contains__("/") or splittedcommand[1].__contains__("\\"):
        if results[0]:
            subprocess.run(["start", results[1]], shell=True, check=True)
        elif not results[0]:
            print(f"Sajnos ez a mappa vagy fájl nem létezik/található: {results[1]}")
    elif results[0]:
        subprocess.run(["start", CurrentPaths + splittedcommand[1]], shell=True, check=True)
    else:
        print(f"Sajnos ez a mappa vagy fájl nem létezik/található: {results[1]}")

def main():
    global CurrentPaths
    command = ""
    while command.lower() != "exit":
        command = input(CurrentPaths)
        if command.lower().startswith("cd "):
            cd(command)
        if command.lower().startswith("dir"):
            kiiras(CurrentPaths)
        if command.lower().startswith("execute"):
            execute(command)
        if command.lower().startswith("exit"):
            exit()
        command = ""

main()
