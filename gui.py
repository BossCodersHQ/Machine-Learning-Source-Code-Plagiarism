import tkinter as tk
from tkinter import *
from tkinter import filedialog, Menu, font

import tkinter.ttk as ttk

window_width = 500
window_height = 500
top = Tk()
top.title("JAVA Similarity Checker")
temp = str(window_width) + "x" + str(window_height)
# top.geometry("500x500")  # sets size of the window
top.columnconfigure(0, weight=1)  # weight of 1 ensures the application resizes


# Code to add widgets will go here...
def sourcefile_dir_cb(var):
    # messagebox.showinfo("Hello Python", "Hello World")
    dirr = filedialog.askdirectory()
    var.set(dirr)
    print(dirr)


menu = Menu(top)
item_instructions = Menu(menu)
item_instructions.add_command(label='Instructions')

menu.add_cascade(label='Help', menu=item_instructions)

top.config(menu=menu)
# directory = filedialog.askdirectory()
# print(directory)

# sets background properties
back = Frame(top, padx=50)
back.grid(row=0)
# -------------------------Styles & Fonts---------------------------#

font_title = font.Font(family="Times New Roman", size=25, weight=font.BOLD)
font_info = font.Font(family="Times New Roman", size=10,  slant=font.ITALIC)
font_normal = font.Font(family="Helvetica", size=10)

# ------------------------Variables -------------------------------#
directory = StringVar()
method_selection = IntVar()
# --------------------End of Variables ----------------------------#

# Row 0 - Title
ROW0 = Frame(back)
ROW0.grid(row=0, pady=10)
label = Label(ROW0, text="JAVA\nSimilarity Checker", font=font_title, justify=CENTER)
label.grid(row=0)

# Row 1 - Software Information
ROW1 = Frame(back)
ROW1.grid(row=1, pady=8)

info_text = """
This is a program designed to test the limits of similarity software. 
Im in the field bottles on spill diamonds just be shining.
"""
label = Label(ROW1, text=info_text, font=font_info, justify=CENTER)
label.grid(row=0)

# Row 2 - Enter Source File
ROW2 = Frame(back)
ROW2.grid(row=2, pady=5)

label = Label(ROW2, text="Enter Source Files Directory:", font=font_normal)
button = Button(ROW2, text="Open", padx=10, command=lambda: sourcefile_dir_cb(directory))
entry = Entry(ROW2, textvariable=directory, width=20)

label.grid(row=0, column=0)
button.grid(row=0, column=1, padx=5)
entry.grid(row=0, column=2)

# Row 3 - Enter method
ROW3 = Frame(back)
ROW3.grid(row=3, pady=5)

label = Label(ROW3, text="Enter the analysing method:", font=font_normal)
RADIO1 = Radiobutton(ROW3, text="Quick", value=1, variable=method_selection)
RADIO2 = Radiobutton(ROW3, text="Best", value=2, variable=method_selection)

label.grid(row=0, column=0)
RADIO1.grid(row=0, column=1)
RADIO2.grid(row=0, column=2)

# Row 4 - Enter number of Attributes
ROW4 = Frame(back)
ROW4.grid(row=4, pady=5)

label = Label(ROW4, text="Enter the number of attributes:", font=font_normal)
combo = ttk.Combobox(ROW4)
combo['values'] = (10, 20, 30)
combo.current(0)

label.grid(row=0, column=0)
combo.grid(row=0, column=1)

# Row 5 - Start Button
ROW5 = Frame(back)
ROW5.grid(row=5, pady=10)

button = Button(ROW5, text="Start", bg="#67D80E", fg="#fff")

button.grid(row=0, ipadx=10, ipady=10)




# ROW1 = Frame(back)
# ROW1.pack(fill=X)
# B1 = Button(ROW1, text="Enter Source Files Directory", command=lambda: sourcefile_dir_cb(directory))
# B1.pack(side=LEFT, ipadx="10")
#
# E1 = Entry(ROW1, textvariable=directory)
# E1.pack(side=LEFT, fill=X, expand=True)
#
#
# close = Button(back, text='Quit', command=lambda: quit())
# close.pack()
top.mainloop()

# import tkinter as tk
#
# root = tk.Tk()
# # root.attributes('-alpha', 1.0) #For icon
# # root.lower()
# root.iconify()
# window = tk.Toplevel(root)
# window.geometry("100x100") #Whatever size
# window.overrideredirect(1) #Remove border
# #window.attributes('-topmost', 1)
# #Whatever buttons, etc
# close = tk.Button(window, text = "Close Window", command = lambda: root.destroy())
# close.pack(fill = tk.BOTH, expand = 1)
# window.mainloop()
