import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import csv


class AddEditExpenseMain(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.populate_new = self.controller.get_page('AddNewExpenseMain')
        self.populate_search = self.controller.get_page('SearchExpenseMain')

        # Set background image
        img = Image.open("images/addEditExpense.png")
        img = img.resize((1000, 800), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(img)
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # ------------------------ Set and place labels and buttons ------------------------------------
        self.PrgLbl = tk.Label(self, text="שינוי/הוספה של הוצאות", fg="black", font=("Times New Rome", "48", "bold"))
        self.PrgLbl.place(relx=0.48, rely=0.195, anchor="c")

        self.SearchExpense = tk.Button(self, text="חפש הוצאה קיימת", font=("Times New Rome", "18", "bold"), bg="gray91",
                                       fg="black", command=self.search_expense)
        self.SearchExpense.place(relx=0.62, rely=0.5, anchor="c")

        self.AddNewExpense = tk.Button(self, text="הוסף הוצאה חדשה", font=("Times New Rome", "18", "bold"), bg="gray91",
                                       fg="black", command=self.new_expense)
        self.AddNewExpense.place(relx=0.33, rely=0.5, anchor="c")

        self.BackBtn = tk.Button(self, text="חזרה", font=("Times New Rome", "18", "bold"), bg="gray91", fg="black",
                                 command=lambda: controller.show_frame("ExpenseMain"))
        self.BackBtn.place(relx=0.2, rely=0.8, anchor="c")

    def new_expense(self):  # Check available categories and payment methods before entering to new expense page
        answer_category = self.category_check_populate(1)
        answer_payment = self.payment_check_populate(1)
        if answer_category == 0 or answer_payment == 0:
            messagebox.showinfo("Error", "!גש להוספת אמצעי תשלום חדש/קטגוריה חדשה ולאחר מכן חזור למסך זה")
        else:
            self.controller.show_frame("AddNewExpenseMain")

    def category_check_populate(self, bit):  # Populate and check the category drop down list
        category_arr = ["בחר"]
        file = open("files/Categories.txt", "r")
        for line in file:
            line = line.strip()
            category_arr.append(line)
        file.close()
        if len(category_arr) == 1:
            return 0
        else:
            if bit == 1:
                self.populate_new.InputCategory['menu'].delete(0, 'end')
                self.populate_new.var1.set(category_arr[0])
                for category in category_arr:
                    self.populate_new.InputCategory['menu'].add_command(label=category,
                                                                        command=tk._setit(self.populate_new.var1,
                                                                                          category))
            else:
                self.populate_search.InputCategory['menu'].delete(0, 'end')
                self.populate_search.var1.set(category_arr[0])
                for category in category_arr:
                    self.populate_search.InputCategory['menu'].add_command(label=category,
                                                                           command=tk._setit(self.populate_search.var1,
                                                                                             category))
            return 1

    def payment_check_populate(self, bit):  # Populate and check the payment drop down list
        payment_arr = ["בחר"]
        file = open("files/PaymentMethods.txt", "r")  # Get payment methods from file
        for line in file:
            line = line.strip()
            payment_arr.append(line)
        file.close()
        if len(payment_arr) == 1:
            return 0
        else:
            if bit == 1:
                self.populate_new.InputPayment['menu'].delete(0, 'end')
                self.populate_new.var2.set(payment_arr[0])
                for payment in payment_arr:
                    self.populate_new.InputPayment['menu'].add_command(label=payment,
                                                                       command=tk._setit(self.populate_new.var2,
                                                                                         payment))
            else:
                self.populate_search.InputPayment['menu'].delete(0, 'end')
                self.populate_search.var2.set(payment_arr[0])
                for payment in payment_arr:
                    self.populate_search.InputPayment['menu'].add_command(label=payment,
                                                                          command=tk._setit(self.populate_search.var2,
                                                                                            payment))
            return 1

    def search_expense(self):  # Check available categories and payment methods before entering to search expenses page
        answer_category = self.category_check_populate(0)
        answer_payment = self.payment_check_populate(0)
        if answer_category == 0 or answer_payment == 0:
            messagebox.showinfo("Error", "!גש להוספת אמצעי תשלום חדש/קטגוריה חדשה ולאחר מכן חזור למסך זה")
        else:
            answer = self.expenses_check()
            if answer == 0:
                messagebox.showinfo("Error", "אין הוצאות כלל נא הוסף הוצאה חדשה במסך המתאים!")
            else:
                self.controller.show_frame("SearchExpenseMain")

    def expenses_check(self):  # Populate the expenses arr list in the search expenses page
        expenses_arr = []
        csv.register_dialect('comma', delimiter=',')
        file = open("files/Expenses.csv", "r")
        reader = csv.reader(file, dialect='comma')
        for row in reader:  # Get expenses data from file
            if row:
                dict1 = {'number': row[0], 'date': row[1], 'category_name': row[2], 'payment_name': row[3],
                         'transaction': row[4], 'comments': row[5]}
                expenses_arr.append(dict1)
        file.close()
        if len(expenses_arr) == 0:  # If local storage is empty
            return 0
        else:
            self.populate_search.expenses_arr = expenses_arr
            return 1
