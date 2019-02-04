import tkinter as tk
from tkinter import *
top = tk.Tk()
top.title("JAVA Similarity Checker")
top.geometry("500x500")     #   sets sixe of the window
# Code to add widgets will go here...

# sets background properties
back = tk.Frame(top, bg='white')
back.pack(fill=BOTH,expand=1)



L1 = Label(back, bg="grey", text="Enter Source Files Directory")
L1.pack( side = LEFT,ipadx="10")

E1 = Entry(back, bd =5)
E1.pack(side = RIGHT)

close = tk.Button(back, text='Quit', bg='black', bd="0", fg='red',command=lambda:quit() ).pack()

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
