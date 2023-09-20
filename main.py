import os
import subprocess

current_path = "C:/"
def FullCheck(input_path):
    """
    A check function that is very complex. It is the main core of the check system.
    :param input_path: The full path that we want to check.
    :return:First is a bool. It means if the file/folder exist or not in that path.
            Second is which file is not exist if it's fail.
            Third is a counter in that path, which is got fail.
            Fourth is where the method stopped or get done.
    """
    global current_path
    paths = input_path
    tmp_current_path = current_path
    result_diskcheck = DiskCheck(input_path)
    if result_diskcheck[0] and result_diskcheck[1] != "Undefined":
        tmp_current_path = result_diskcheck[1]
        paths = result_diskcheck[2]
    elif not result_diskcheck[0]:
        return False, paths[0:3], "Disk"
    pathsplitted = PathsCutter(paths)
    for path_item in pathsplitted:
        if path_item != "":
            results_foldercheck = FolderCheck(tmp_current_path, path_item)
            if not results_foldercheck[1]:
                return False, path_item, "Not disk"
            else:
                tmp_current_path = results_foldercheck[1]
    return True, tmp_current_path, "Not disk"

def FolderCheck(input_path, input_pathsplitted):
    """
    This is a core of the checking system. Here is decided going back or forward and is it a folder.
    :param input_path: The path that we want to check and format.
    :param input_pathsplitted: The next destination folder.
    :return: First is a bool that is it format or not. The second if yes the newly created output path
    """
    if input_pathsplitted == ".." and input_path[1:] != ":/":
        return True, FolderMoveBack(input_path)
    if input_pathsplitted != "" and input_pathsplitted != "..":
        result_folderforward = FolderMoveForward(input_path, input_pathsplitted)
        if result_folderforward[0]:
            return True, result_folderforward[1]
        else:
            return True, result_folderforward[1]
    return False, "Undefined"
def DiskCheck(input_path):
    """
    This function take care of that if the input path is absolute this is format it to be relative path.
    :param input_path: The path that we want to check and format.
    :return: First is a bool. This shows is it format the path.
             Second if yes it gives back the disk drive like C:/.
             Third is the relative path.
    """
    if input_path.__contains__(":/"):
        if os.path.exists(input_path[0:3]):
            return True, input_path[0:3], input_path[3:]
        else:
            return False, "Undefined", "Undefined"
    return True, "Undefined", "Undefined"

def FolderMoveBack(input_path):
    """
    This function is take care of the move folder back. It's split the path and from that list
    remove the last two. For example: inputpath = C:/dog/food/ and it gives back the C:/dog/.
    :param input_path: The path that we want to go back on it.
    :return: The newly created path.
    """
    pathsplitted = PathsCutter(input_path)
    pathsplitted.pop()
    pathsplitted.pop()
    output_current_paths = ""
    for i in range(len(pathsplitted)):
        output_current_paths += pathsplitted[i] + "/"
    return output_current_paths

def FolderMoveForward(input_current_path, input_path_find):
    """
    This function is take care of the path to move forward. It's check the folder or file is there
    if yes it goes on it.
    :param input_current_path: The parameter of the folder where we want to check.
    :param input_path_find: The parameter of the folder that in the inputpath we want to check for it.
    :return: It's a tuple that we get back. First is a bool that was it success or not.
             The second is the newly created path with simply the inputpath + / + inputpathfind.
             It only gives it back if the first one is true.
    """
    output_path = input_current_path
    for entry in os.scandir(output_path):
        if entry.is_dir() or entry.is_file():
            if input_path_find.lower() == entry.name.lower():
                if entry.is_file():
                    output_path += entry.name
                    return True, output_path
                else:
                    output_path += entry.name + "/"
                    return True, output_path
    return False, "Undefined"

def FileShowing(input_path):
    """
    This function core controll for the dir command.
    Not much command is here and it is not complex, so it is only one function.
    :param input_path: The path that we want to show the files in it.
    :return: There is no return data in it.
    """
    checkdirectory = os.scandir(input_path)
    for entry in checkdirectory:
        if entry.is_dir() or entry.is_file():
            print(entry.name)



def Cd(input_command):
    """
    This function core controll for the complex cd command.
    It would be very complicated if I would put everything to only one function.
    This provides functions calling and their data to set up properly.
    :param input_command: The command itself.
    :return: There is no return.
    """
    global current_path
    result_is_argument = IsArgument(input_command)
    if result_is_argument[0].startswith("/") or result_is_argument[0].startswith("\\"):
        path = result_is_argument[0][4:]
    else:
        path = result_is_argument[0][3:]
    result_check = FullCheck(path)
    if not result_is_argument[1] and not result_check[0]:
        print(f"Sorry but this disk or folder doesn't exist: {result_check[1]}")
    elif result_is_argument[1] and not result_check[0] and result_check[2] == "Not disk":
        MakeFolders(path)
    elif result_check[0]:
        current_path = result_check[1]
    return

def IsArgument(input_command):
    """
    This function if the command has arguments it returns it. For now it is a bitly simplier than it should.
    Not yet used that much and also needs some upgrades to work fine with every command.
    For now the CD uses only.
    :param input_command: The command itself. Like in cd or execute.
    :return: First is the new command without the argument.
             Second the bool for now only dedicated for "cd" command
             Third is for later use what argument is the command us
    """
    is_this_r = False
    argument_name = ""
    output_command = input_command
    if input_command[-3:] == " -r":
        is_this_r = True
        output_command = input_command[:-3]
        argument_name += "r"
    return output_command, is_this_r, argument_name

def PathsCutter(input_path):
    """
    It's a simply path splitter. It is necessary to get the paths into a List and return it.
    :param input_path: The path that we want to split.
    :return: The splitted path list.
    """
    if input_path.__contains__("/"):
        output_paths = input_path.split("/")
    else:
        output_paths = input_path.split("\\")
    return output_paths

def MakeFolders(input_path):
    """
    It is for now a folder maker function. For now it is a helper function for the cd [folder/folders] -r command.
    Later it will have more functions.
    We can give it any path that is possible, and it makes it. For example:
    The "dog" folder is avaliable in C:/ volume, but you give it as C:/dog/foods/fruits/.
    It will make a foods folder in the dog folder and in foods it create a fruits folder too.
    :param input_path: The path that we want to make folder on it.
    :return: There is no return.
    """
    global current_path
    splitted_path = PathsCutter(input_path)
    found_one_missing = False
    for Folder in splitted_path:
        if Folder != "":
            if not found_one_missing:
                result_check = FullCheck(current_path + Folder)
                if not result_check[0]:
                   found_one_missing = True
            if found_one_missing:
                current_path += Folder + "/"
                os.mkdir(current_path)
            else:
                current_path += Folder + "/"

def Execute(input_command):
    """
    It is an execute program for the execute command. It split the command, check is the file is avaliable, is
    the absolute or relative path(if we give to the command) is avaliable and the file is exist.
    It uses for this the Check function, which return that is the file/folder is avaliable and if yes which one etc.
    :param input_command: The command itself.
    :return: There is no return.
    """
    splitted_command = input_command.split(" ")
    result_check = FullCheck(splitted_command[1])
    if splitted_command[1].__contains__("/") or splitted_command[1].__contains__("\\"):
        if result_check[0]:
            subprocess.run(["start", result_check[1]], shell=True, check=True)
        elif not result_check[0]:
            print(f"Sorry but this file or folder doesn't exist: {result_check[1]}")
    elif result_check[0]:
        subprocess.run(["start", current_path + splitted_command[1]], shell=True, check=True)
    else:
        print(f"Sorry but this file or folder doesn't exist: {result_check[1]}")

def main():
    """
    It is the Main Function. The function, that provides connection between user and program.
    It gets the command and forward it to the functions.
    """
    global current_path
    command = ""
    while command.lower() != "exit":
        command = input(current_path)
        if command.lower().startswith("cd "):
            Cd(command)
        if command.lower().startswith("dir"):
            FileShowing(current_path)
        if command.lower().startswith("execute"):
            Execute(command)
        if command.lower().startswith("exit"):
            exit()
        command = ""

main()
