import pdf_processor
import pdf_parser_old
import eco_directory_checker
import re
import tkinter as tk

# KornitPart class is created for each part
class KornitPart:
    def __init__(self, path, pop_path, file_list, log, balloon_check):
        self.issues = []
        self.dir_drawing_number = eco_directory_checker.get_dir_drawing_number(path)
        if self.dir_drawing_number != "":
            self.part_number, self.rev, self.drawing_number, self.signatures, self.date = pdf_processor.get_info(path, pop_path, log, balloon_check, self.dir_drawing_number, self.issues)
            self.dir_rev = eco_directory_checker.get_dir_rev(path)
            eco_directory_checker.check_occurrences(self.dir_drawing_number, file_list, log, self)
        # log.insert(tk.END, f"Kornit P/N: {self.part_number}\n")
        # log.insert(tk.END, f"Drawing number from PDF: {self.drawing_number}\n")
        # log.insert(tk.END,f"Revision from PDF: {self.rev}\n")
        # eco_directory_checker.check_occurrences(self.dir_drawing_number, file_list, self.part_number)

        # log.insert(tk.END,f"Drawing number from file name: {self.dir_drawing_number}\n")
        # log.insert(tk.END,f"Revision from file name: {self.dir_rev}\n")

    #Check P/N in PDF
    def check_pn(self, log):
        if self.part_number is None:
            log.insert(tk.END, f"{self.dir_drawing_number}: Missing correct P/N in PDF\n")
            log.yview(tk.END)
            self.issues.append('Missing correct P/N in PDF')

    # Comparing between directory and PDF revisions
    def compare_revs(self, log):
        if self.rev != self.dir_rev:
            log.insert(tk.END, f"{self.dir_drawing_number}: PDF revision and directory revision are not the same!\n")
            log.yview(tk.END)
            self.issues.append('PDF revision and directory revision are not the same!')

    # Comparing between directory and PDF drawing numbers
    def compare_drawing_numbers(self, log):
        if self.drawing_number != self.dir_drawing_number:
            log.insert(tk.END, f"{self.dir_drawing_number}: PDF drawing number and directory drawing number are not the same!\n")
            log.yview(tk.END)
            self.issues.append('PDF drawing number and directory drawing number are not the same!')

    # Checking that there are 3 signatures each page and alerting if there are missing signatures
    # Includes number of missing signatures and page number
    def check_signatures(self, log):
        for page_num, page_signatures in enumerate(self.signatures):
            if page_signatures == 2:
                log.insert(tk.END, f"{self.dir_drawing_number}: There is 1 signature missing in page {page_num + 1}\n")
                log.yview(tk.END)
                self.issues.append(f'There is 1 signature missing in page {page_num + 1}')
            elif page_signatures < 2:
                log.insert(tk.END, f"{self.dir_drawing_number}: There are {3 - page_signatures} signatures missing in page {page_num + 1}\n")
                log.yview(tk.END)
                self.issues.append(f"There are {3 - page_signatures} signatures missing in page {page_num + 1}")

    # Checking if there is a date next to signatures
    def check_date(self, log):
        if self.date is False:
            log.insert(tk.END, f"{self.dir_drawing_number}: Missing signature date\n")
            log.yview(tk.END)
            self.issues.append('Missing signature date')