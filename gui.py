import tkinter as tk
from tkinter import filedialog, Menu, font, messagebox, scrolledtext
import tkinter.ttk as ttk
from GST import main as gst
from quickGST import main as quick_gst
from machine_learning import main as ml
import threading
import util

STOPFLAG = False    # Used inconjunctin with threading to allow methods to be stopped


class Fonts:
    def __init__(self):
        self.title = font.Font(family="Times New Roman", size=25, weight=font.BOLD)
        self.info = font.Font(family="Times New Roman", size=10, slant=font.ITALIC)
        self.normal = tk.font.Font(family="Helvetica", size=10)


def get_directory(var):
    directory = filedialog.askdirectory()
    var.set(directory)


def set_stop_flag():
    util.STOPFLAG = True


class Main(tk.Frame):
    def __init__(self, parent, fonts):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.background = tk.Frame(self.parent, padx=50)
        self.background.grid(row=0)
        self.fonts = fonts

        # -----------------Creating variables-------------------#
        self.source_dir = tk.StringVar()
        self.results_dir = tk.StringVar()
        self.method_selection = tk.IntVar()
        self.combo = None
        self.output_box = None

        # Setting Layout rules
        self.create_title().grid(row=0, columnspan=2, pady=10)
        self.software_info().grid(row=1, columnspan=2, pady=8)
        self.source_files_entry().grid(row=2, columnspan=2, pady=5)
        self.results_files_entry().grid(row=3, columnspan=2, pady=5)
        self.method_entry().grid(row=4, columnspan=2, pady=5)
        attributes_entry = self.attributes_entry()
        attributes_entry.grid(row=5, columnspan=2, pady=5)
        attributes_entry.grid_remove()
        log_box, self.output_box = self.log_box()
        log_box.grid(row=6, column=0, ipady=10, pady=10, rowspan=3)
        self.clear_button().grid(row=6, column=1, sticky="S")
        self.stop_button().grid(row=7, column=1, sticky="N")
        self.start_button().grid(row=8, column=1, pady=10, stick="N")

    def create_title(self):
        title = tk.Frame(self.background)

        label = tk.Label(title, text="JAVA\nSimilarity Checker", font=self.fonts.title, justify=tk.CENTER)
        label.grid(row=0)
        return title

    def software_info(self):
        row = tk.Frame(self.background)

        info_text = """
        This is a program designed to test the limits of similarity software.
        Im in the field bottles on spill diamonds just be shining.
        """
        label = tk.Label(row, text=info_text, font=self.fonts.info, justify=tk.CENTER)
        label.grid(row=0)
        return row

    def source_files_entry(self):
        row = tk.Frame(self.background)

        label = tk.Label(row, text="Enter Source Files Directory:", font=self.fonts.normal)
        button = tk.Button(row, text="Open", padx=10, command=lambda: get_directory(self.source_dir))
        entry = tk.Entry(row, textvariable=self.source_dir, width=20)

        label.grid(row=0, column=0)
        button.grid(row=0, column=1, padx=5)
        entry.grid(row=0, column=2)

        return row

    def results_files_entry(self):
        row = tk.Frame(self.background)

        label = tk.Label(row, text="Enter Directory For Results Folder:", font=self.fonts.normal)
        button = tk.Button(row, text="Open", padx=10, command=lambda: get_directory(self.results_dir))
        entry = tk.Entry(row, textvariable=self.results_dir, width=20)

        label.grid(row=0, column=0)
        button.grid(row=0, column=1, padx=5)
        entry.grid(row=0, column=2)

        return row

    def method_entry(self):
        row = tk.Frame(self.background)

        label = tk.Label(row, text="Enter the Analysis method:", font=self.fonts.normal)
        radio1 = tk.Radiobutton(row, text="ML(quick)", value=1, variable=self.method_selection)
        radio2 = tk.Radiobutton(row, text="Improved GST + AST(quick)", value=2, variable=self.method_selection)
        radio3 = tk.Radiobutton(row, text="Normal GST(slow)", value=3, variable=self.method_selection)

        label.grid(row=0, column=0, rowspan=2)
        radio1.grid(row=0, column=1, sticky="W")
        radio2.grid(row=0, column=2, sticky="W")
        radio3.grid(row=1, column=1, columnspan=2, sticky="W")

        return row

    def attributes_entry(self):
        row = tk.Frame(self.background)

        label = tk.Label(row, text="Enter the number of attributes:", font=self.fonts.normal)
        combo = ttk.Combobox(row)
        combo['values'] = (10, 20, 30)
        combo.current(0)
        self.combo = combo  # allows combo boc to be accessed from outside this method

        label.grid(row=0, column=0)
        combo.grid(row=0, column=1)

        return row

    def start_button(self):
        row = tk.Frame(self.background)
        button = tk.Button(row, text="Start", bg="#67D80E", fg="#fff", command=lambda: self.main())
        button.grid(row=0, ipadx=10, ipady=20)
        return row

    def stop_button(self):
        row = tk.Frame(self.background)
        button = tk.Button(row, text="Stop", bg="#e82600", fg="#fff", command=lambda: set_stop_flag())
        button.grid(row=0, ipadx=10, ipady=10)
        return row

    def clear_button(self):
        row = tk.Frame(self.background)
        button = tk.Button(row, text="Clear", bg="#e5e5e5", fg="#000000", command=lambda: self.clear_log_box())
        button.grid(row=0, ipadx=10, ipady=5)
        return row

    def log_box(self):
        row = tk.Frame(self.background)
        txt = scrolledtext.ScrolledText(row, width=40, height=10)
        txt.grid(row=0, ipadx=10, ipady=10)
        return row, txt

    def clear_log_box(self):
        self.output_box.delete(1.0, tk.END)

    def main(self):
        source_directory = self.source_dir.get()
        results_directory = self.results_dir.get()
        method_choice = self.method_selection.get()
        num_attributes = self.combo.get()
        # print(source_directory)
        # print(method_choice)
        # print(num_attributes)

        if source_directory == "":
            messagebox.showerror("Error", "No Source directory has been entered")
        elif results_directory == "":
            messagebox.showerror("Error", "No Results directory has been entered")
        elif method_choice == 0:
            messagebox.showerror("Error", "No Method has been chosen")
        else:
            if method_choice == 3:
                self.output_box.insert(tk.INSERT, "Greedy String Tiling(Slowest):\n")
                thread = threading.Thread(target=gst, args=(source_directory, results_directory, self.output_box))
                thread.daemon = True  # Daemonize thread
                thread.start()

            if method_choice == 2:
                self.output_box.insert(tk.INSERT, "Improved Greedy String Tiling(Quick):\n")
                thread = threading.Thread(target=quick_gst, args=(source_directory, results_directory, self.output_box))
                thread.daemon = True  # Daemonize thread
                thread.start()

            if method_choice == 1:
                self.output_box.insert(tk.INSERT, "Attribute Counting using Machine Learning(Quick):\n")
                thread = threading.Thread(target=ml, args=(source_directory, results_directory, self.output_box))
                thread.daemon = True  # Daemonize thread
                thread.start()


class Menu(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.menu = tk.Menu(parent)
        self.parent = parent

        file_menu = tk.Menu(self.menu)
        file_menu.add_command(label="New Window")
        help_menu = tk.Menu(self.menu)
        help_menu.add_command(label='Instructions')

        self.menu.add_cascade(label='File', menu=file_menu)
        self.menu.add_cascade(label='Help', menu=help_menu)
        parent.config(menu=self.menu)


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent    # the parent acts as a master controller
        self.parent.title("JAVA Similarity Checker")
        self.parent.columnconfigure(0, weight=1)  # weight of 1 ensures the application resizes

        fonts = Fonts()
        menu = Menu(self.parent)

        self.background = Main(self.parent, fonts)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()


# window_width = 500
# window_height = 500
# root = Tk()
# root.title("JAVA Similarity Checker")
# temp = str(window_width) + "x" + str(window_height)
# # top.geometry("500x500")  # sets size of the window
# root.columnconfigure(0, weight=1)  # weight of 1 ensures the application resizes
#
# menu = Menu(root)
# item_instructions = Menu(menu)
# item_instructions.add_command(label='Instructions')
#
# menu.add_cascade(label='Help', menu=item_instructions)
#
# root.config(menu=menu)
# # directory = filedialog.askdirectory()
# # print(directory)
#
# # sets background properties
# back = Frame(root, padx=50)
# back.grid(row=0)
# # -------------------------Styles & Fonts---------------------------#
#
# font_title = font.Font(family="Times New Roman", size=25, weight=font.BOLD)
# font_info = font.Font(family="Times New Roman", size=10,  slant=font.ITALIC)
# font_normal = font.Font(family="Helvetica", size=10)
#
# # ------------------------Variables -------------------------------#
# directory = StringVar()
# method_selection = IntVar()
# # --------------------End of Variables ----------------------------#
#
# # Row 0 - Title
# ROW0 = Frame(back)
# ROW0.grid(row=0, pady=10)
# label = Label(ROW0, text="JAVA\nSimilarity Checker", font=font_title, justify=CENTER)
# label.grid(row=0)
#
# # Row 1 - Software Information
# ROW1 = Frame(back)
# ROW1.grid(row=1, pady=8)
#
# info_text = """
# This is a program designed to test the limits of similarity software.
# Im in the field bottles on spill diamonds just be shining.
# """
# label = Label(ROW1, text=info_text, font=font_info, justify=CENTER)
# label.grid(row=0)
#
# # Row 2 - Enter Source File
# ROW2 = Frame(back)
# ROW2.grid(row=2, pady=5)
#
# label = Label(ROW2, text="Enter Source Files Directory:", font=font_normal)
# button = Button(ROW2, text="Open", padx=10, command=lambda: sourcefile_dir_cb(directory))
# entry = Entry(ROW2, textvariable=directory, width=20)
#
# label.grid(row=0, column=0)
# button.grid(row=0, column=1, padx=5)
# entry.grid(row=0, column=2)
#
# # Row 3 - Enter method
# ROW3 = Frame(back)
# ROW3.grid(row=3, pady=5)
#
# label = Label(ROW3, text="Enter the analysing method:", font=font_normal)
# RADIO1 = Radiobutton(ROW3, text="Quick", value=1, variable=method_selection)
# RADIO2 = Radiobutton(ROW3, text="Best", value=2, variable=method_selection)
#
# label.grid(row=0, column=0)
# RADIO1.grid(row=0, column=1)
# RADIO2.grid(row=0, column=2)
#
# # Row 4 - Enter number of Attributes
# ROW4 = Frame(back)
# ROW4.grid(row=4, pady=5)
#
# label = Label(ROW4, text="Enter the number of attributes:", font=font_normal)
# combo = ttk.Combobox(ROW4)
# combo['values'] = (10, 20, 30)
# combo.current(0)
#
# label.grid(row=0, column=0)
# combo.grid(row=0, column=1)
#
# # Row 5 - Start Button
# ROW5 = Frame(back)
# ROW5.grid(row=5, pady=10)
#
# button = Button(ROW5, text="Start", bg="#67D80E", fg="#fff")
#
# button.grid(row=0, ipadx=10, ipady=10)
#
#
#
#
# # ROW1 = Frame(back)
# # ROW1.pack(fill=X)
# # B1 = Button(ROW1, text="Enter Source Files Directory", command=lambda: sourcefile_dir_cb(directory))
# # B1.pack(side=LEFT, ipadx="10")
# #
# # E1 = Entry(ROW1, textvariable=directory)
# # E1.pack(side=LEFT, fill=X, expand=True)
# #
# #
# # close = Button(back, text='Quit', command=lambda: quit())
# # close.pack()
# root.mainloop()
#
# # import tkinter as tk
# #
# # root = tk.Tk()
# # # root.attributes('-alpha', 1.0) #For icon
# # # root.lower()
# # root.iconify()
# # window = tk.Toplevel(root)
# # window.geometry("100x100") #Whatever size
# # window.overrideredirect(1) #Remove border
# # #window.attributes('-topmost', 1)
# # #Whatever buttons, etc
# # close = tk.Button(window, text = "Close Window", command = lambda: root.destroy())
# # close.pack(fill = tk.BOTH, expand = 1)
# # window.mainloop()
