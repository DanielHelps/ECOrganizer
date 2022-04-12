import tkinter as tk

# Check how many files with the format of XXX-XX-XX-XXX (X is a digit)
# there are in the folder
def check_occurrences(drawing_number, file_list, log, kornit_pn):
    number_of_files = sum(drawing_number in file for file in file_list)
    if number_of_files < 2:
        log.insert(tk.END,f"{drawing_number}: Not enough files in directory!\n")
        log.yview(tk.END)
        kornit_pn.issues.append("Not enough files in directory!")
    elif number_of_files > 3:
        log.insert(tk.END,f"{drawing_number}: Too many files in directory!\n")
        log.yview(tk.END)
        kornit_pn.issues.append("Too many files in directory!")

# Get the drawing number from directory
def get_dir_drawing_number(path):
    return path[len(path)-20:len(path)-7]


# Get the revision from directory
def get_dir_rev(path):
    return path[len(path) - 6:len(path) - 4]


# Check whether revisions of drawing, model and BOM are the same (in directory)
def check_revs(name, file_list):
    rev = None
    for current_file in file_list:
        if name == current_file[:13] and rev is None:
            rev = current_file[14:16]
        elif name == current_file[:13] and rev != current_file[14:16]:
            print(f"{name} revisions do not match")
