import os
import subprocess

CurrentPaths = "C:/"


def check(Inputpath):
    """
    A check function that is very complex, because yet I haven't write it to more clean.
    Sidenote: In the future I want it to be more understandable and rewrite.
    It gets a path and check if the path is absolute or relative.
    After that from absolute it makes relative path.
    It has back or forward to go from folders to folders.
    Also the method for it uses the same.
    Check folder --> if exist it means success/if not it means fail.
    That's how it gives back a lot of information.
    First is a bool. It means if the file/folder exist or not in that path.
    Second is which file is not exist if it's fail.
    Third is a counter in that path, which is got fail.
    Fourth is where the method stopped or get done.
    """
    global CurrentPaths
    tmpCurrentPaths = CurrentPaths
    if Inputpath.__contains__(":/"):
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

def FileShowing(writedirectory):
    """
    The core controll for the dir command.
    Not much command is here and it is not complex, so it is only one function.
    """
    checkdirectory = os.scandir(writedirectory)
    for entry in checkdirectory:
        if entry.is_dir() or entry.is_file():
            print(entry.name)



def Cd(InputCommand):
    """
    The core controll for the complex cd command.
    It would be very complicated if I would put everything to only one function.
    This provides functions calling and their data to set up properly.
    Sidenote: .. is still not works properly.
    """
    global CurrentPaths
    ResultIsArgument = IsArgument(InputCommand)
    Paths = ResultIsArgument[0][4:]
    CheckedPaths = check(Paths)
    if not ResultIsArgument[1] and not CheckedPaths[0]:
        print(f"Sorry but this disk or folder doesn't exist: {CheckedPaths[1]}")
    elif ResultIsArgument[1] and not CheckedPaths[0] and CheckedPaths[2] != "Undefined":
        MakeFolders(Paths)
    elif CheckedPaths[0] == 1:
        CurrentPaths = CheckedPaths[1]
    return

def IsArgument(InputCommand):
    """
    If the command has arguments it returns it. For now it is a bitly simplier than it should.
    Not yet used that much and also needs some upgrades to work fine with every command.
    For now the CD uses only.
    It returns the pure command without the argument, so we can use it properly. After the bool for
    now only dedicated for "cd" command and for later use what argument is the command use.
    """
    IsThisR = False
    WhatArgument = ""
    OutputCommand = InputCommand
    if InputCommand[-3:] == " -r":
        IsThisR = True
        OutputCommand = InputCommand[:-3]
        WhatArgument += "r"
    return OutputCommand, IsThisR, WhatArgument

def PathsCutter(InputPaths):
    """
    It's a simply path splitter. It is necessary to get the paths into a List and return it.
    """
    if InputPaths.__contains__("/"):
        OutputPaths = InputPaths.split("/")
    else:
        OutputPaths = InputPaths.split("\\")
    return OutputPaths

def MakeFolders(InputPath):
    """
    It is for now a folder maker function. For now it is a helper function for the cd [folder/folders] -r command.
    Later it will have more functions.
    We can give it any path that is possible, and it makes it. For example:
    The "dog" folder is avaliable in C:/ volume, but you give it as C:/dog/foods/fruits/.
    It will make a foods folder in the dog folder and in foods it create a fruits folder too.
    """
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

def Execute(yourcommand):
    """
    It is an execute program for the execute command. It split the command, check is the file is avaliable, is
    the absolute or relative path(if we give to the command) is avaliable and the file is exist.
    It uses for this the Check function, which return that is the file/folder is avaliable and if yes which one etc.
    """
    splittedcommand = yourcommand.split(" ")
    results = check(splittedcommand[1])
    if splittedcommand[1].__contains__("/") or splittedcommand[1].__contains__("\\"):
        if results[0]:
            subprocess.run(["start", results[1]], shell=True, check=True)
        elif not results[0]:
            print(f"Sorry but this file or folder doesn't exist: {results[1]}")
    elif results[0]:
        subprocess.run(["start", CurrentPaths + splittedcommand[1]], shell=True, check=True)
    else:
        print(f"Sorry but this file or folder doesn't exist: {results[1]}")

def main():
    """
    It is the Main Function. The function, that provides connection between user and program.
    It gets the command and forward it to the functions.
    """
    global CurrentPaths
    command = ""
    while command.lower() != "exit":
        command = input(CurrentPaths)
        if command.lower().startswith("cd "):
            Cd(command)
        if command.lower().startswith("dir"):
            FileShowing(CurrentPaths)
        if command.lower().startswith("execute"):
            Execute(command)
        if command.lower().startswith("exit"):
            exit()
        command = ""

main()
