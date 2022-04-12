import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
import os
from drawing_checker import KornitPart
import tkinter.messagebox
import threading
import xlsxwriter

pop_path = f"{os.getcwd()}\\poppler"


## Choices class definition
class choices():
    def __init__(self, master):
        self.master = master
        self.path = 'placeholder'
        self.files = []


## Functions definitions

# When you change radio buttons
def radio_change(folder_files):
    if folder_files.get() == 'folder':
        files_widget.config(state='disabled')
        files_button.config(state='disabled')
        folder_widget.config(state='normal')
        folder_button.config(state='normal')
    else:
        files_button.config(state='normal')
        folder_widget.config(state='disabled')
        folder_button.config(state='disabled')


def browse_folder():
    directory = filedialog.askdirectory()
    if directory != '':
        folder_entry.set(directory)


def browse_files():
    files = filedialog.askopenfilenames(parent=root, title='Choose files', filetypes=[
        ('all files', '*'),
        ('Acrobat reader files', '.pdf'),
        ('x_t files', '.x_t'),
        ('New excel files', '.xlsx'),
        ('Old excel files', '.xls'), ])
    files_list = list(files)
    files_list_text = ["{}{}".format(i, "\n") for i in files_list]
    try:
        # Try and split for path and file name
        choice.path = os.path.split(files_list[0])[0]
    except:
        pass
    else:
        choice.files = [os.path.split(i)[1] for i in files_list]
        if files != '':
            # Show file names + path in files log (make log disabled so user can't change input)
            files_widget.config(state='normal')
            files_widget.delete(1.0, tk.END)
            files_widget.insert(1.0, ''.join(files_list_text))
            files_widget.config(state='disabled')


def creating_thread(folder_or_files):
    # Use threading for action
    t1 = threading.Thread(target=run_ECOrganizer(folder_or_files))
    t1.start()


#  Run the program
def run_ECOrganizer(folder_or_files):
    run_but.config(state='disabled')
    cancel_but.config(state='normal')
    export_but.config(state='disabled')
    # Delete log and set progress bar value to 0
    log.delete(1.0, tk.END)
    pb['value'] = 0
    global stop
    # Stop = 1 - cancel button pressed, stop = 0 - cancel button wasn't pressed
    stop = 0
    try:
        # If the user chose a folder
        if folder_or_files.get() == 'folder':
            choice.path = folder_entry.get()
            choice.files = os.listdir(choice.path)
        else:
            os.listdir(choice.path)
    except:
        # In case file list is incorrect (weird files, changed directory name manually...)
        tkinter.messagebox.showinfo("Error", "Error importing files list.\nPlease check information.")
    else:
        os.chdir(choice.path)
        global part_list
        part_list = []
        counter = -1
        for i, file in enumerate(choice.files):
            # If cancel button was pressed
            if stop == 1:
                log.insert(tk.END, "Process Canceled")
                break
            # check if file is a pdf and if it has the proper name
            if file[-4:] == ".pdf" and file[len(file) - 20:len(file) - 7] != "":
                counter += 1
                # Create a KornitPart object that holds all the information of the part
                part_list.append(KornitPart(file, pop_path, choice.files, log, balloons_check.get()))
                if dir_drawing_num_check.get() == 1:
                    part_list[counter].compare_drawing_numbers(log)
                if dir_rev_check.get() == 1:
                    part_list[counter].compare_revs(log)
                if signatures_check.get() == 1:
                    part_list[counter].check_signatures(log)
                if date_check.get() == 1:
                    part_list[counter].check_date(log)
                if pn_check.get() == 1:
                    part_list[counter].check_pn(log)
            # If got to the end change process bar % to 100
            if i + 1 != len(choice.files):
                pb['value'] += round(float(100 / len(choice.files)), 2)
            else:
                pb['value'] = 100
            value_label['text'] = f"{round(pb['value'], 2)}%"
            root.update()

        export_but.config(state='normal')
        run_but.config(state='normal')
        cancel_but.config(state='disabled')
        pass


def cancel():
    # print(stop)
    global stop
    stop = 1
    run_but.config(state='normal')
    cancel_but.config(state='disabled')


def export_to_excel():
    global part_list
    files = [('Excel file', '*.xlsx')]
    path = filedialog.asksaveasfile(mode='w', defaultextension=files, filetypes=files)
    if path is None:  # asksaveasfile return `None` if dialog closed with "cancel".
        return
    workbook = xlsxwriter.Workbook(path.name)
    sheet = workbook.add_worksheet(name="Warnings")
    bold = workbook.add_format({'bold': True})
    sheet.write(0, 0, "Part number", bold)
    sheet.write(0, 1, "Drawing number", bold)
    sheet.write(0, 2, "Warning", bold)
    row = 1
    for part in part_list:
        if len(part.issues) != 0:
            for issue in part.issues:
                # Write the warnings for each item (write part_number and drawing number)
                sheet.write(row, 0, part.part_number)
                sheet.write(row, 1, part.dir_drawing_number)
                sheet.write(row, 2, issue)
                row += 1
    sheet.set_column(0, 0, 13)
    sheet.set_column(1, 1, 15.14)
    sheet.set_column(2, 2, 40)
    workbook.close()
    tkinter.messagebox.showinfo("Export to excel", "Log exported to excel")


## Help window
def help_window():
    help_win = tk.Toplevel(root)
    help_win.title("Help")
    help_win.geometry("1500x920")
    help_win.resizable(False, False)
    help_win.iconbitmap(os.getcwd() + "\\poppler\\icon.ico")
    regular_font = ("Helvetica", 12)
    # Focus on help window
    help_win.focus()
    # Create a grid
    help_win.columnconfigure(0, weight=1)
    help_win.columnconfigure(1, weight=1)

    tk.Label(help_win,
             text="This app allows the user to perform basic checks on drawings for ECOs.\n\n"
                  "The app can perform the following checks:\n\n\n\n\n "
                  "Directory vs PDF revision - \n "
                  "Checks for the revision of the item in"
                  " the explorer directory and compares it with the revision in the PDF", font=regular_font,
             justify=tk.LEFT, anchor="w") \
        .grid(row=0, column=0, sticky=tk.W)

    # Show image of revisions comparing
    rev_photo = tk.PhotoImage(file='./poppler/rev_comp.png')
    rev_photo_label = tk.Label(help_win, image=rev_photo, padx=10, pady=10)
    rev_photo_label.image = rev_photo
    rev_photo_label.grid(row=1, column=0, sticky=tk.W)

    tk.Label(help_win,
             text="\nDirectory vs PDF drawing number -\n"
                  "Checks for the drawing number of the item in"
                  " the explorer directory and compares it with the drawing\n number in the PDF", font=regular_font,
             justify=tk.LEFT, anchor="w") \
        .grid(row=0, column=1, sticky=tk.SW)

    # Show image of drawing number comparing
    rev_photo = tk.PhotoImage(file='./poppler/drawing_number_comp.png')
    rev_photo_label = tk.Label(help_win, image=rev_photo, padx=10, pady=10)
    rev_photo_label.image = rev_photo
    rev_photo_label.grid(row=1, column=1, sticky=tk.W)

    tk.Label(help_win,
             text="\nSignatures -\n"
                  "Checks for all 3 signatures in the drawing in all pages, if "
                  "a signature is missing it raises a warning\n and on what page", font=regular_font,
             justify=tk.LEFT, anchor="w") \
        .grid(row=2, column=0, sticky=tk.W)

    # Show image of signatures check
    rev_photo = tk.PhotoImage(file='./poppler/signs_check.png')
    rev_photo_label = tk.Label(help_win, image=rev_photo, padx=10, pady=10)
    rev_photo_label.image = rev_photo
    rev_photo_label.grid(row=3, column=0, sticky=tk.W)

    tk.Label(help_win,
             text="\nSignatures date -\n"
                  "Checks for signature date on any signature or any page, and raises a warning if no date is present",
             font=regular_font,
             justify=tk.LEFT, anchor="w") \
        .grid(row=4, column=0, sticky=tk.W)

    # Show image of date check
    rev_photo = tk.PhotoImage(file='./poppler/date_check.png')
    rev_photo_label = tk.Label(help_win, image=rev_photo, padx=10, pady=10)
    rev_photo_label.image = rev_photo
    rev_photo_label.grid(row=5, column=0, sticky=tk.NW)

    tk.Label(help_win,
             text="\nKornit P/N -\n"
                  "Checks if the item has the correct form of a Kornit P/N."
                  " Raises a warning if P/N is wrong format / doesn't exist.", font=regular_font,
             justify=tk.LEFT, anchor="w") \
        .grid(row=2, column=1, sticky=tk.SW)

    # Show image of part number check
    rev_photo = tk.PhotoImage(file='./poppler/pn_check.png')
    rev_photo_label = tk.Label(help_win, image=rev_photo, padx=10, pady=10)
    rev_photo_label.image = rev_photo
    rev_photo_label.grid(row=3, column=1, sticky=tk.W)

    tk.Label(help_win,
             text="\nBalloons -\n"
                  "Scans the drawing and check for all present balloons."
                  " Raises a warning if a balloon is missing", font=regular_font,
             justify=tk.LEFT, anchor="w") \
        .grid(row=4, column=1, sticky=tk.SW)

    # Show image of balloons check
    rev_photo = tk.PhotoImage(file='./poppler/baloons_check.png')
    rev_photo_label = tk.Label(help_win, image=rev_photo, padx=10, pady=10)
    rev_photo_label.image = rev_photo
    rev_photo_label.grid(row=5, column=1, sticky=tk.W)

    tk.Label(help_win,
             text="For any questions or comments please contact me at mdan1000@gmail.com \n", font=regular_font,
             justify=tk.LEFT, anchor="w") \
        .grid(row=100, column=0, sticky=tk.W)

    help_exit_but = ttk.Button(help_win, text="Exit", command=lambda: help_win.destroy())
    help_exit_but.grid(row=100, column=1, ipadx=20, ipady=10, pady=10)


## Initializing window

root = tk.Tk()
root.geometry('700x860')
root.resizable(False, False)
root.title('ECOrganizer')
# Set icon
root.iconbitmap(os.getcwd() + "\\poppler\\icon.ico")
# Initialize settings
choice = choices(root)
title_font = ("Helvetica", 16)
regular_font = ("Helvetica", 12)
# Create a grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
global part_list
part_list = []
## First label
ttk.Label(
    root,
    text='Choose either to import files or a folder:',
    font=title_font).grid(row=0, column=0, sticky=tk.W)

## import part

# Tuple of tuples for choosing import type radio buttons
import_type = (('Import folder', 'folder'),
               ('Import files', 'files'))
folder_or_files = tk.StringVar()

# Import folder
folder_radio = ttk.Radiobutton(
    root,
    text=import_type[0][0],
    value=import_type[0][1],
    variable=folder_or_files,
    command=lambda: radio_change(folder_or_files)
)
folder_radio.grid(row=1, column=0, sticky=tk.W, padx=10)
folder_or_files.set('folder')
folder_button = ttk.Button(
    root,
    text="Browse",
    command=browse_folder,
)
folder_button.grid(row=1, column=0, sticky=tk.W, padx=120)

folder_entry = tk.StringVar()
folder_entry.set(os.getcwd())
folder_widget = ttk.Entry(
    root,
    font=regular_font, textvariable=folder_entry, background='white')
folder_widget.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5, ipadx=280, columnspan=5)

# Import files
files_radio = ttk.Radiobutton(
    root,
    text=import_type[1][0],
    value=import_type[1][1],
    variable=folder_or_files,
    command=lambda: radio_change(folder_or_files)
)
files_radio.grid(row=3, column=0, sticky=tk.W, padx=10)

files_button = ttk.Button(
    root,
    text="Browse",
    state='disabled',
    command=browse_files
)
files_button.grid(row=3, column=0, sticky=tk.W, padx=120)
files_widget = ScrolledText(root, width=135, height=13, state='disabled')
files_widget.grid(row=4, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)

## Checks section

ttk.Label(root,
          text='Choose checks to do:',
          font=title_font).grid(row=5, column=0, sticky=tk.W, pady=5, padx=5)

# Checkboxes for each possible check
dir_rev_check = tk.IntVar()
dir_rev_check.set(1)
ttk.Checkbutton(root,
                text='Directory vs PDF revision',
                variable=dir_rev_check,
                ).grid(row=6, column=0, sticky=tk.W, pady=5, padx=5)

dir_drawing_num_check = tk.IntVar()
dir_drawing_num_check.set(1)
ttk.Checkbutton(root,
                text='Directory drawing number vs PDF',
                variable=dir_drawing_num_check,
                ).grid(row=6, column=1, sticky=tk.W, pady=5, padx=5)

balloons_check = tk.IntVar()
balloons_check.set(1)
ttk.Checkbutton(root,
                text='Balloons',
                variable=balloons_check,
                ).grid(row=7, column=0, sticky=tk.W, pady=5, padx=5)

signatures_check = tk.IntVar()
signatures_check.set(1)
ttk.Checkbutton(root,
                text='Signatures',
                variable=signatures_check,
                ).grid(row=7, column=1, sticky=tk.W, pady=5, padx=5)

date_check = tk.IntVar()
date_check.set(1)
ttk.Checkbutton(root,
                text='Signatures date',
                variable=date_check,
                ).grid(row=8, column=0, sticky=tk.W, pady=5, padx=5)

pn_check = tk.IntVar()
pn_check.set(1)
ttk.Checkbutton(root,
                text='Kornit P/N check',
                variable=pn_check,
                ).grid(row=8, column=1, sticky=tk.W, pady=5, padx=5)

## Run and cancel buttons

run_but = ttk.Button(root, text="Run", command=lambda: creating_thread(folder_or_files))
run_but.grid(row=10, column=1, columnspan=1, ipady=10, ipadx=20, pady=20, padx=10, sticky=tk.W)

cancel_but = ttk.Button(root, text="Cancel", command=cancel, state='disabled')
cancel_but.grid(row=10, column=1, columnspan=1, ipady=10, ipadx=20, pady=20, padx=10, sticky=tk.E)

## Log

log = ScrolledText(root, width=77, height=10)
log.grid(row=11, column=0, columnspan=2, padx=10, sticky=tk.W)

## Progress bar

pb = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='determinate',
    length=480
)
pb.grid(row=12, column=0, columnspan=2, padx=10, pady=20, sticky=tk.W)

# Value for progress bar
value_label = tk.Label(root, text="0%")
value_label.grid(row=12, column=1, padx=80, columnspan=2, sticky=tk.W)

# Export to excel button
export_but = ttk.Button(root, text="Export to excel", state='disabled', command=export_to_excel)
export_but.grid(row=12, column=1, sticky=tk.E, padx=20, ipady=3)

## Bottom buttons

help_but = ttk.Button(root, text="Help", command=help_window)
help_but.grid(row=13, column=0, ipadx=20, ipady=10)

exit_but = ttk.Button(root, text="Exit", command=lambda: root.quit())
exit_but.grid(row=13, column=1, ipadx=20, ipady=10)

## Developed by me!

tk.Label(root, text="Developed by Daniel Marom").grid(row=14, column=1, sticky=tk.SE, pady=20)

root.mainloop()
