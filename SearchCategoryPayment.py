import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
# -*- coding: utf-8 -*-


class SearchCategoryPaymentMain(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.table = []  # Table that show the filtering ans sorting results on screen
        self.var = tk.IntVar()  # Get the current selected radio button
        self.search_results = []  # The category/payment list after sorting
        self.var1 = tk.StringVar()  # Variable that holds the current selected category
        self.var2 = tk.StringVar()  # Variable that holds the current selected payment method

        self.selection = None  # Type of selection
        self.name = None  # Name of chosen type for display
        self.type = None  # Type - category or payment method
        self.current_type = None  # Current category or payment before editing

        self.sort_category = 0  # Sorting category ascending/descending
        self.sort_payment = 0  # Sorting payment method ascending/descending
        self.item_chosen = 0  # If a certain filter has been applied remember that filter when using other filters
        self.table_exist = 0  # while sorting don't alter data from local storage
        self.save_btn = None  # Save button to save changes to current row
        self.abort_btn = None  # Abort button to cancel any changes made by the user
        self.delete_btn = None  # Delete button to remove an expense from the array and file

        # Set background image
        img = Image.open("images/SearchExpense.png")
        img = img.resize((1000, 800), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(img)
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # ------------------------ Set and place labels and buttons ------------------------------------
        self.PrgLbl = tk.Label(self, text="חפש הוצאה", fg="black", font=("Times New Rome", "48", "bold"))
        self.PrgLbl.place(relx=0.5, rely=0.07, anchor="c")

        self.category = tk.Radiobutton(self, text="קטגוריה", font=("Times New Rome", "18", "bold"), variable=self.var,
                                       value=1, command=self.delete_table)
        self.category.place(relx=0.6, rely=0.35, anchor="c")
        self.category.select()

        self.payment = tk.Radiobutton(self, text="אמצעי תשלום", font=("Times New Rome", "18", "bold"),
                                      variable=self.var, value=2, command=self.delete_table)
        self.payment.place(relx=0.4, rely=0.35, anchor="c")

        self.ShowBtn = tk.Button(self, text="הצג", font=("Times New Rome", "18", "bold"), bg="gray91", fg="black",
                                 command=lambda: self.show_category_payment)
        self.ShowBtn.place(relx=0.65, rely=0.5, anchor="c")

        self.BackBtn = tk.Button(self, text="חזרה", font=("Times New Rome", "18", "bold"), bg="gray91", fg="black",
                                 command=lambda: controller.show_frame("AddEditCategoryPaymentMain"))
        self.BackBtn.place(relx=0.35, rely=0.5, anchor="c")

    def choose_sort(self, var):  # Choose what type to add: category or payment method
        if var == 1:
            self.category_sort()
        elif var == 2:
            self.payment_sort()

    def category_sort(self):  # Sorting categories ascending/descending
        self.table_exist = 1
        if self.sort_category == 0:  # Sorting categories ascending
            self.search_results.sort(key=lambda k: k['category_name'])
            self.show_category_payment()  # Show table result after sorting
            self.sort_category = 1
        elif self.sort_category == 1:  # Sorting categories descending
            self.search_results.sort(key=lambda k: k['category_name'], reverse=True)
            self.show_category_payment()  # Show table result after sorting
            self.sort_category = 0
        self.table_exist = 0

    def payment_sort(self):  # Sorting payment methods ascending/descending
        self.table_exist = 1
        if self.sort_payment == 0:  # Sorting payment methods ascending
            self.search_results.sort(key=lambda k: k['payment_name'])
            self.show_category_payment()  # Show table result after sorting
            self.sort_payment = 1
        elif self.sort_payment == 1:  # Sorting payment methods descending
            self.search_results.sort(key=lambda k: k['payment_name'], reverse=True)
            self.show_category_payment()  # Show table result after sorting
            self.sort_payment = 0
        self.table_exist = 0

    def show_category_payment(self):  # Show all expenses according to search results
        self.delete_table()
        if self.table_exist == 0:
            self.selection = self.var.get()
            if self.selection == 1:
                file = open("files/Categories.txt", "r")
                for line in file:
                    line = line.strip()
                    self.search_results.append(line)
                file.close()
                self.name = "קטגוריה"
                self.type = "category"
            elif self.selection == 2:
                file = open("files/PaymentMethods.txt", "r")
                for line in file:
                    line = line.strip()
                    self.search_results.append(line)
                file.close()
                self.name = "אמצעי תשלום"
                self.type = "payment"
            else:
                messagebox.showinfo("Error", "!אין פריטים בקטגוריה זו")
                return

        b = tk.Button(self, text=self.name, font=("Times New Rome", "12", "bold"), bg="gray91", fg="black",
                      command=lambda i=self.selection: self.choose_sort(self.selection))
        b.place(relx=0.86, rely=0.57, anchor="c")
        val = 0
        for item in range(len(self.search_results)):  # Get info from search results and insert to table
            rows = [val]
            cols = []
            e = tk.Entry(self, width="10", justify='center')
            e.insert(tk.END, self.search_results[item])
            e.configure(state='readonly', font=("Times New Rome", "14", "bold"))
            e.place(relx=0.8, rely=0.62+(item*0.05), anchor="c")
            cols.append(e)
            rows.append(cols)

            cols = []
            # Create an edit button for every row to change parameters in the row
            change_btn = tk.Button(self, text="שינוי", width="6", font=("Times New Rome", "10", "bold"), bg="gray91",
                                   fg="black", command=lambda i=val: self.edit_row(val))
            change_btn.place(relx=0.79, rely=0.62+(item*0.05), anchor="c")
            cols.append(change_btn)
            rows.append(cols)
            self.table.append(rows)
            val = val + 1

    def delete_table(self):
        if len(self.table) == 0:
            return
        for rows in self.table:
            for cols in rows:
                if not isinstance(cols, str):
                    cols[0].place_forget()
        self.table.clear()

    def edit_row(self, num):  # Make a certain row editable and add save, delete and abort buttons
        for rows in self.table:
            if rows[0] == num:
                for cols in rows:
                    if isinstance(cols, str):
                        continue
                    elif cols[0].winfo_class() == "Entry":
                        cols[0].configure(state='normal', font=("Times New Rome", "14", "bold"))
                        self.current_type = cols[0].get()
                    elif cols[0].winfo_class() == "Button":
                        cols[0].config(state="disabled")
                        y = cols[0].place_info()['rely']
                        self.save_btn = tk.Button(self, text="שמור", width="6", font=("Times New Rome", "10", "bold"),
                                                  bg="gray91", fg="black",
                                                  command=lambda i=num: self.save_changes(num))
                        self.save_btn.place(relx=0.72, rely=float(y), anchor="c")
                        self.delete_btn = tk.Button(self, text="מחק", width="6", font=("Times New Rome", "10", "bold"),
                                                    bg="gray91", fg="black",
                                                    command=lambda i: self.delete_expense)
                        self.delete_btn.place(relx=0.65, rely=float(y), anchor="c")
                        self.abort_btn = tk.Button(self, text="בטל", width="6", font=("Times New Rome", "10", "bold"),
                                                   bg="gray91", fg="black",
                                                   command=lambda i: self.abort_changes)
                        self.abort_btn.place(relx=0.58, rely=float(y), anchor="c")
            else:
                for cols in rows:  # disable other edit buttons - one edit at a time
                    if isinstance(cols, str):
                        continue
                    elif cols[0].winfo_class() == "Button":
                        cols[0].config(state="disabled")

    def save_changes(self, num):  # Get changes from edited row check for valid inputs and save to file and array
        my_type = None
        for rows in self.table:
            if rows[0] == num:
                for cols in rows:
                    if isinstance(cols, str):
                        continue
                    elif cols[0].winfo_class() == "Entry":
                        my_type = cols[0].get()
            break

        for item in self.search_results:
            if my_type == item:
                if self.type == "category":
                    messagebox.showinfo("Error", "!הקטגוריה הנוכחית כבר קיימת")
                elif self.type == "payment":
                    messagebox.showinfo("Error", "!אמצעי התשלום הנוכחי כבר קיים")
                return

        for item1 in self.search_results:
            if item1 == self.current_type:
                indx = self.search_results.index(item1)
                self.search_results[indx] = item1
            break

        if self.type == "category":
            file1 = open("files/Categories.txt", "w")  # Write all categories to file
            file1.seek(0)
            file1.truncate()
            file1.write('\n'.join(self.search_results))
            file1.close()
        elif self.type == "payment":
            file1 = open("files/PaymentMethods.txt", "w")  # Write all categories to file
            file1.seek(0)
            file1.truncate()
            file1.write('\n'.join(self.search_results))
            file1.close()

        self.show_category_payment()
        self.remove_buttons()

    def abort_changes(self):  # Abort any changes made by the user and restore the original expense
        self.show_category_payment()
        self.remove_buttons()

    def delete_expense(self):  # Delete the current expense from the file and the array
        for item1 in self.search_results:
            if item1 == self.current_type:
                indx = self.search_results.index(item1)
                del self.search_results[indx]
            break

        if self.type == "category":
            file1 = open("files/Categories.txt", "w")  # Write all categories to file
            file1.seek(0)
            file1.truncate()
            file1.write('\n'.join(self.search_results))
            file1.close()
        elif self.type == "payment":
            file1 = open("files/PaymentMethods.txt", "w")  # Write all categories to file
            file1.seek(0)
            file1.truncate()
            file1.write('\n'.join(self.search_results))
            file1.close()

        self.show_category_payment()
        self.remove_buttons()

    def remove_buttons(self):  # Remove the save, abort and delete buttons fro the row and enable all edit buttons
        for rows in self.table:
            for cols in rows:
                if isinstance(cols, str):
                    continue
                elif cols[0].winfo_class() == "Button":
                    if cols[0]['text'] == "שינוי":
                        cols[0].config(state="normal")
        self.save_btn.place_forget()
        self.save_btn = None
        self.abort_btn.place_forget()
        self.abort_btn = None
        self.delete_btn.place_forget()
        self.delete_btn = None
