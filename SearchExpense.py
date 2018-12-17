import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
import csv
# -*- coding: utf-8 -*-


class SearchExpenseMain(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.table = []  # Table that show the filtering ans sorting results on screen
        self.expenses_arr = []  # The expenses list
        self.search_results = []  # The expenses list after sorting and filtering

        self.category_arr = ["בחר"]  # The category drop down list
        self.payment_arr = ["בחר"]  # The payment methods drop down list
        self.var1 = tk.StringVar()  # Variable that holds the current selected category
        self.var2 = tk.StringVar()  # Variable that holds the current selected payment method

        self.sort_date = 0  # Sorting date ascending/descending
        self.sort_category = 0  # Sorting category ascending/descending
        self.sort_payment = 0  # Sorting payment method ascending/descending
        self.sort_transaction = 0  # Sorting transaction ascending/descending
        self.item_chosen = 0  # If a certain filter has been applied remember that filter when using other filters
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

        self.DateSearch = tk.Label(self, text=":חפש לפי תאריכים", fg="black", font=("Times New Rome", "18", "bold"))
        self.DateSearch.place(relx=0.5, rely=0.15, anchor="c")

        self.DateStart = tk.Label(self, text=":מתאריך", fg="black", font=("Times New Rome", "18", "bold"))
        self.DateStart.place(relx=0.82, rely=0.2, anchor="c")

        self.InputDateStart = tk.Entry(self, width="30")
        self.InputDateStart.place(relx=0.67, rely=0.2, anchor="c")

        self.DateEnd = tk.Label(self, text=":עד תאריך", fg="black", font=("Times New Rome", "18", "bold"))
        self.DateEnd.place(relx=0.48, rely=0.2, anchor="c")

        self.InputDateEnd = tk.Entry(self, width="30")
        self.InputDateEnd.place(relx=0.33, rely=0.2, anchor="c")

        self.ChooseCategory = tk.Label(self, text=":חפש לפי קטגוריה", fg="black", font=("Times New Rome", "18", "bold"))
        self.ChooseCategory.place(relx=0.58, rely=0.27, anchor="c")

        self.InputCategory = tk.OptionMenu(self, self.var1, *self.category_arr)
        self.InputCategory.place(relx=0.44, rely=0.27, anchor="c")

        self.PaymentOptions = tk.Label(self, text=":חפש לפי סוג תשלום", font=("Times New Rome", "18", "bold"),
                                       fg="black")
        self.PaymentOptions.place(relx=0.58, rely=0.34, anchor="c")

        self.InputPayment = tk.OptionMenu(self, self.var2, *self.payment_arr)
        self.InputPayment.place(relx=0.43, rely=0.34, anchor="c")

        self.TransactionSum = tk.Label(self, text=":חפש לפי סכום עסקה", font=("Times New Rome", "18", "bold"),
                                       fg="black")
        self.TransactionSum.place(relx=0.62, rely=0.41, anchor="c")

        self.InputTransactionSum = tk.Entry(self, width="30")
        self.InputTransactionSum.place(relx=0.4, rely=0.41, anchor="c")

        self.SearchBtn = tk.Button(self, text="חפש", font=("Times New Rome", "18", "bold"), bg="gray91",
                                   fg="black", command=self.search)
        self.SearchBtn.place(relx=0.65, rely=0.5, anchor="c")

        self.CleanBtn = tk.Button(self, text="נקה שדות", font=("Times New Rome", "18", "bold"), bg="gray91",
                                  fg="black", command=self.clear_text_data)
        self.CleanBtn.place(relx=0.5, rely=0.5, anchor="c")

        self.BackBtn = tk.Button(self, text="חזרה", font=("Times New Rome", "18", "bold"), bg="gray91", fg="black",
                                 command=lambda: controller.show_frame("AddEditExpenseMain"))
        self.BackBtn.place(relx=0.35, rely=0.5, anchor="c")

    def choose_sort(self, var):  # Choose the sorting type according to button pressing
        if var == 0:
            self.date_sort()
        elif var == 1:
            self.category_sort()
        elif var == 2:
            self.payment_sort()
        elif var == 3:
            self.transaction_sort()

    def date_sort(self):  # Sorting dates ascending/descending
        if self.sort_date == 0:  # Sorting dates ascending
            self.search_results.sort(key=lambda k: datetime.strptime(k['date'], '%d/%m/%y'))
            self.show_expense(self.search_results)  # Show table result after sorting
            self.sort_date = 1
        elif self.sort_date == 1:  # Sorting dates descending
            self.search_results.sort(key=lambda k: datetime.strptime(k['date'], '%d/%m/%y'), reverse=True)
            self.show_expense(self.search_results)  # Show table result after sorting
            self.sort_date = 0

    def category_sort(self):  # Sorting categories ascending/descending
        if self.sort_category == 0:  # Sorting categories ascending
            self.search_results.sort(key=lambda k: k['category_name'])
            self.show_expense(self.search_results)  # Show table result after sorting
            self.sort_category = 1
        elif self.sort_category == 1:  # Sorting categories descending
            self.search_results.sort(key=lambda k: k['category_name'], reverse=True)
            self.show_expense(self.search_results)  # Show table result after sorting
            self.sort_category = 0

    def payment_sort(self):  # Sorting payment methods ascending/descending
        if self.sort_payment == 0:  # Sorting payment methods ascending
            self.search_results.sort(key=lambda k: k['payment_name'])
            self.show_expense(self.search_results)  # Show table result after sorting
            self.sort_payment = 1
        elif self.sort_payment == 1:  # Sorting payment methods descending
            self.search_results.sort(key=lambda k: k['payment_name'], reverse=True)
            self.show_expense(self.search_results)  # Show table result after sorting
            self.sort_payment = 0

    def transaction_sort(self):  # Sorting transactions ascending/descending
        if self.sort_transaction == 0:  # Sorting transactions ascending
            self.search_results.sort(key=lambda k: float(k['transaction']))
            self.show_expense(self.search_results)  # Show table result after sorting
            self.sort_transaction = 1
        elif self.sort_transaction == 1:  # Sorting transactions descending
            self.search_results.sort(key=lambda k: float(k['transaction']), reverse=True)
            self.show_expense(self.search_results)  # Show table result after sorting
            self.sort_transaction = 0

    def search(self):  # Search button - search for expenses according to certain filters
        start = self.InputDateStart.get()
        end = self.InputDateEnd.get()
        category = self.var1.get()
        payment = self.var2.get()
        transaction = self.InputTransactionSum.get()

        if start != "" and end == "":  # Only start date was entered
            messagebox.showinfo("Error", "נא הכנס תאריך יעד!")
            return
        elif start == "" and end != "":  # Only end date was entered
            messagebox.showinfo("Error", "נא הכנס תאריך התחלה!")
            return
        elif start != "" and end != "":  # Filter according to given dates
            start = datetime.strptime(start, '%d/%m/%Y')
            end = datetime.strptime(end, '%d/%m/%Y')
            if self.item_chosen == 0:  # If table haven't been filtered
                self.search_results = list(filter(lambda d: start < datetime.strptime(d['date'], '%d/%m/%Y') < end,
                                                  self.expenses_arr))
                self.show_expense(self.search_results)
                self.item_chosen = 1
            else:  # If table have been filtered before
                self.search_results = list(filter(lambda d: start < datetime.strptime(d['date'], '%d/%m/%Y') < end,
                                                  self.search_results))
                self.show_expense(self.search_results)

        if category != "בחר":  # Filter according to a certain category - if one was chosen
            if self.item_chosen == 0:  # If table haven't been filtered
                self.search_results = list(filter(lambda d: d['category_name'] == category, self.expenses_arr))
                self.show_expense(self.search_results)
                self.item_chosen = 1
            else:  # If table have been filtered
                self.search_results = list(filter(lambda d: d['category_name'] == category, self.search_results))
                self.show_expense(self.search_results)

        if payment != "בחר":  # Filter according to a certain payment method - if one was chosen
            if self.item_chosen == 0:  # If table haven't been filtered
                self.search_results = list(filter(lambda d: d['payment_name'] == payment, self.expenses_arr))
                self.show_expense(self.search_results)
                self.item_chosen = 1
            else:  # If table have been filtered
                self.search_results = list(filter(lambda d: d['payment_name'] == payment, self.search_results))
                self.show_expense(self.search_results)

        if transaction != "":  # Filter according to a certain transaction sum - if one was chosen
            if self.item_chosen == 0:  # If table haven't been filtered
                self.search_results = list(filter(lambda d: float(d['transaction']) == float(transaction),
                                                  self.expenses_arr))
                self.show_expense(self.search_results)
                self.item_chosen = 1
            else:  # If table have been filtered
                self.search_results = list(filter(lambda d: float(d['transaction']) == float(transaction),
                                                  self.search_results))
                self.show_expense(self.search_results)
        self.item_chosen = 0

    def show_expense(self, local_expense_arr):  # Show all expenses according to search results
        if local_expense_arr is None:
            return
        if self.item_chosen == 1:
            self.delete_table()
        temp_arr = []
        button_arr = ["תאריך", "קטגוריה", "אמצעי תשלום", "סכום עסקה", "הערות"]
        for x in range(4):  # Set the sorting buttons
            b = tk.Button(self, text=button_arr[x], font=("Times New Rome", "12", "bold"), bg="gray91", fg="black",
                          command=lambda i=x: self.choose_sort(x))
            b.place(relx=0.86 - (x * 0.12), rely=0.57, anchor="c")

        # Set comments label
        lbl = tk.Label(self, text=button_arr[4], fg="black", font=("Times New Rome", "12", "bold"))
        lbl.place(relx=0.38, rely=0.57, anchor="c")

        for item in range(len(local_expense_arr)):  # Get info from search results and insert to table
            dic = local_expense_arr[item]
            num = dic['number']
            temp_arr.append(dic['date'])
            temp_arr.append(dic['category_name'])
            temp_arr.append(dic['payment_name'])
            temp_arr.append(dic['transaction'])
            temp_arr.append(dic['comments'])

            rows = [num]
            for j in range(5):  # Add an expenses to the table
                cols = []
                e = tk.Entry(self, width="10", justify='center')
                e.insert(tk.END, temp_arr[j])
                e.configure(state='readonly', font=("Times New Rome", "14", "bold"))
                e.place(relx=0.86-(j*0.12), rely=0.62+(item*0.05), anchor="c")
                cols.append(e)
                rows.append(cols)

            cols = []
            # Create an edit button for every row to change parameters in the row
            change_btn = tk.Button(self, text="שינוי", width="6", font=("Times New Rome", "10", "bold"), bg="gray91",
                                   fg="black", command=lambda i=num: self.edit_row(num))
            change_btn.place(relx=0.28, rely=0.62+(item*0.05), anchor="c")
            cols.append(change_btn)
            rows.append(cols)
            self.table.append(rows)
            temp_arr = []

        if len(local_expense_arr) == 0 and self.item_chosen == 0:
            # If there are no results after filtering, show - "no results found"
            messagebox.showinfo("Error", "לא נמצאו תוצאות!")

    def delete_table(self):
        for rows in self.table:
            for cols in rows:
                if not isinstance(cols, str):
                    cols[0].place_forget()
        self.table.clear()

    def clear_text_data(self):  # Clear all input fields
        self.InputDateStart.delete('0', tk.END)
        self.InputDateEnd.delete('0', tk.END)
        self.var1.set("בחר")
        self.var2.set("בחר")
        self.InputTransactionSum.delete('0', tk.END)

    def edit_row(self, num):  # Make a certain row editable and add save, delete and abort buttons
        for rows in self.table:
            if rows[0] == num:
                for cols in rows:
                    if isinstance(cols, str):
                        continue
                    elif cols[0].winfo_class() == "Entry":
                        cols[0].configure(state='normal', font=("Times New Rome", "14", "bold"))
                    elif cols[0].winfo_class() == "Button":
                        cols[0].config(state="disabled")
                        y = cols[0].place_info()['rely']
                        self.save_btn = tk.Button(self, text="שמור", width="6", font=("Times New Rome", "10", "bold"),
                                                  bg="gray91", fg="black",
                                                  command=lambda i=num: self.save_changes(num))
                        self.save_btn.place(relx=0.21, rely=float(y), anchor="c")
                        self.delete_btn = tk.Button(self, text="מחק", width="6", font=("Times New Rome", "10", "bold"),
                                                    bg="gray91", fg="black",
                                                    command=lambda i=num: self.delete_expense(num))
                        self.delete_btn.place(relx=0.14, rely=float(y), anchor="c")
                        self.abort_btn = tk.Button(self, text="בטל", width="6", font=("Times New Rome", "10", "bold"),
                                                   bg="gray91", fg="black",
                                                   command=lambda i=num: self.abort_changes(num))
                        self.abort_btn.place(relx=0.07, rely=float(y), anchor="c")
            else:
                for cols in rows:  # disable other edit buttons - one edit at a time
                    if isinstance(cols, str):
                        continue
                    elif cols[0].winfo_class() == "Button":
                        cols[0].config(state="disabled")

    def save_changes(self, num):  # Get changes from edited row check for valid inputs and save to file and array
        temp_list = []
        for rows in self.table:
            if rows[0] == num:
                for cols in rows:
                    if isinstance(cols, str):
                        temp_list.append(cols)
                    elif cols[0].winfo_class() == "Entry":
                        temp_list.append(cols[0].get())
            break

        if temp_list[2] not in self.category_arr:
            messagebox.showinfo("Error", "!הקטגוריה לא קיימת")
            return
        if temp_list[3] not in self.payment_arr:
            messagebox.showinfo("Error", "!שיטת התשלום לא קיימת")
            return

        if temp_list[4].isalpha():
            messagebox.showinfo("Error", "!זה לא סכום עסקה חוקי")
            return
        if float(temp_list[4]) <= 0:
            messagebox.showinfo("Error", "!סכום העסקה חייב להיות חיובי")
            return

        dict1 = {'number': temp_list[0], 'date': temp_list[1], 'category_name': temp_list[2],
                 'payment_name': temp_list[3], 'transaction': temp_list[4], 'comments': temp_list[5]}

        expenses = self.get_expenses()
        for item1 in expenses:
            if item1['number'] == num:
                indx = self.expenses_arr.index(item1)
                expenses[indx] = dict1
            break

        file1 = open("files/Expenses.csv", "w")
        file1.seek(0)
        file1.truncate()
        writer = csv.writer(file1, dialect='comma')
        for dic in expenses:
            my_list = list(dic.values())
            writer.writerow(my_list)
        file1.close()

        for item2 in self.expenses_arr:
            if item2['number'] == num:
                indx = self.expenses_arr.index(item2)
                self.expenses_arr[indx] = dict1
            break

        self.show_expense(self.expenses_arr)
        self.remove_buttons()

    def abort_changes(self, num):  # Abort any changes made by the user and restore the original expense
        dict1 = None
        expenses = self.get_expenses()
        for item1 in expenses:
            if item1['number'] == num:
                dict1 = {'number': item1['number'], 'date': item1['date'], 'category_name': item1['category_name'],
                         'payment_name': item1['payment_name'], 'transaction': item1['transaction'],
                         'comments': item1['comments']}
                break

        for item2 in self.expenses_arr:
            if item2['number'] == num:
                indx = self.expenses_arr.index(item2)
                self.expenses_arr[indx] = dict1
                break
        self.show_expense(self.search_results)
        self.remove_buttons()

    def delete_expense(self, num):  # Delete the current expense from the file and the array
        expenses = self.get_expenses()
        for item1 in expenses:
            if item1['number'] == num:
                indx = self.expenses_arr.index(item1)
                del expenses[indx]
            break

        file1 = open("files/Expenses.csv", "w")
        file1.seek(0)
        file1.truncate()
        writer = csv.writer(file1, dialect='comma')
        for dic in expenses:
            my_list = list(dic.values())
            writer.writerow(my_list)
        file1.close()

        for item2 in self.expenses_arr:
            if item2['number'] == num:
                indx = self.expenses_arr.index(item2)
                del self.expenses_arr[indx]
            break

        for item2 in self.search_results:
            if item2['number'] == num:
                indx = self.search_results.index(item2)
                del self.search_results[indx]
            break
        self.show_expense(self.search_results)
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

    @staticmethod
    def get_expenses():  # Get expenses from the expenses file
        expenses_arr = []
        csv.register_dialect('comma', delimiter=',')
        file = open("files/Expenses.csv", "r")
        reader = csv.reader(file, dialect='comma')
        for row in reader:  # Get expenses data from file
            if row:
                dict1 = {'number': row[0], 'date': row[1], 'category_name': row[2], 'payment_name': row[3],
                         'transaction': row[4], 'comments': row[5]}
                expenses_arr.append(dict1)
        return expenses_arr
