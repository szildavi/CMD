import tkinter as tk

"""
Initialize the important variable and objects
"""
window = tk.Tk()
text_box = tk.Text(window, fg="white", bg="black", state="disabled")
entry = tk.Entry(window, fg="white", bg="black", font="Consolas")
key = ""
is_keydown = False


def GUIstart():
    """
    This function is the GUI start. It's initialize the window.
    :return:
    """
    window.title("CMD prompt")
    window.geometry("800x400")
    entry.place(x = 0,y=370, width=800, height=30)
    text_box.place(x = 0, y=0, width=800, height=370)
    window.bind("<Key>", Keypress)
    window.mainloop()


def GUIout(input_text):
    """
    It is the prompt output. This is where the out print is happens.
    :param input_text: The text that we want to print.
    :return:
    """
    text_box.config(state="normal")
    text_box.insert(tk.END,input_text + f"\n")
    text_box.config(state="disabled")
    text_box.yview("end")

def Keypress(event):
    """
    This is the key press method to store the key we press.
    :param event: The key in string.
    :return:
    """
    global key
    key = event.keysym

def Send():
    """
    It is the output for the main.py.
    :return: The output string. These are the command we give to the main.py
    """
    global is_keydown
    if key == "Return":
        is_keydown = True
        return entry.get()

