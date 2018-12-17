import tkinter as tk
from tkinter import messagebox
import csv
from PIL import Image, ImageTk


class AddNewExpenseMain(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.calendar = self.controller.get_page('CalendarMain')

        self.category_arr = ["בחר"]  # The category drop down list
        self.payment_arr = ["בחר"]  # The payment methods drop down list
        self.var1 = tk.StringVar()  # Variable that holds the current selected category
        self.var2 = tk.StringVar()  # Variable that holds the current selected payment method

        # Set background image
        img = Image.open("images/addNewExpense.png")
        img = img.resize((1000, 800), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(img)
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # ------------------------ Set and place labels and buttons ------------------------------------
        self.PrgLbl = tk.Label(self, text="הוסף הוצאה חדשה", fg="black", font=("Times New Rome", "48", "bold"),
                               bg="snow")
        self.PrgLbl.place(relx=0.5, rely=0.1, anchor="c")

        self.MyDate = tk.Label(self, text=":הכנס תאריך", fg="black", bg="snow", font=("Times New Rome", "18", "bold"))
        self.MyDate.place(relx=0.67, rely=0.2, anchor="c")

        self.NewDate = tk.Entry(self, width="30")
        self.NewDate.place(relx=0.5, rely=0.2, anchor="c")
        self.ChooseDateBtn = tk.Button(self, text="בחר תאריך", font=("Times New Rome", "12", "bold"), bg="gray91",
                                       fg="black", command=self.calendar.select_date)
        self.ChooseDateBtn.place(relx=0.3, rely=0.2, anchor="c")

        self.MyCategory = tk.Label(self, text=":בחר קטגוריה", fg="black", font=("Times New Rome", "18", "bold"),
                                   bg="snow")
        self.MyCategory.place(relx=0.75, rely=0.27, anchor="c")

        self.InputCategory = tk.OptionMenu(self, self.var1, *self.category_arr)
        self.InputCategory.place(relx=0.59, rely=0.27, anchor="c")

        self.MyPayment = tk.Label(self, text=":בחר אמצעי תשלום", fg="black", font=("Times New Rome", "18", "bold"),
                                  bg="snow")
        self.MyPayment.place(relx=0.4, rely=0.27, anchor="c")

        self.InputPayment = tk.OptionMenu(self, self.var2, *self.payment_arr)
        self.InputPayment.place(relx=0.26, rely=0.27, anchor="c")

        self.MyTransaction = tk.Label(self, text=":הכנס סכום עסקה", fg="black", font=("Times New Rome", "18", "bold"),
                                      bg="snow")
        self.MyTransaction.place(relx=0.7, rely=0.34, anchor="c")

        self.NewTransaction = tk.Entry(self, width="30")
        self.NewTransaction.place(relx=0.5, rely=0.34, anchor="c")

        self.MyComments = tk.Label(self, text=":הערות", fg="black", font=("Times New Rome", "18", "bold"), bg="snow")
        self.MyComments.place(relx=0.64, rely=0.41, anchor="c")

        self.NewComments = tk.Entry(self, width="30")
        self.NewComments.place(relx=0.5, rely=0.41, anchor="c")

        self.AddNewExpenseBtn = tk.Button(self, text="הוסף הוצאה", font=("Times New Rome", "18", "bold"), bg="gray91",
                                          fg="black", command=self.save_expense)
        self.AddNewExpenseBtn.place(relx=0.7, rely=0.5, anchor="c")

        self.BackBtn = tk.Button(self, text="חזרה", font=("Times New Rome", "18", "bold"), bg="gray91", fg="black",
                                 command=lambda: controller.show_frame("AddEditExpenseMain"))
        self.BackBtn.place(relx=0.4, rely=0.5, anchor="c")

    def save_expense(self):  # Save the new expense to file
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
        if expenses_arr is None:  # If local storage is empty
            items_count = 0  # Set first item to number 0
            expenses_arr = []
        else:  # If local storage is not empty
            items_count = len(expenses_arr)  # Get the max number of items from local storage
            items_count = items_count + 1  # Set the new item to be 1+ of current number of items

        date = self.NewDate.get()  # Get date value from input
        category_name = self.var1.get()  # Get category name from input
        payment_name = self.var2.get()  # get payment method name from input
        transaction = self.NewTransaction.get()  # get transaction sum value from input
        comments = self.NewComments.get()  # get comment value from input
        if comments.find('"'):  # Set to empty if comment is undefined
            comments = ""
        if date == "" or category_name == "בחר" or payment_name == "בחר" or transaction == "":
            # Only comments can be empty
            messagebox.showinfo("Error", "!רק שדה הערות יכול להשאר ריק")
            return
        if transaction.isalpha():
            messagebox.showinfo("Error", "!זה לא מספר חוקי")
            return
        if float(transaction) <= 0:  # Transaction sum value must be greater then zero
            messagebox.showinfo("Error", "!סכום עסקה חייב להיות חיובי")
            return
        items_count = str(items_count)
        expense = {"number": items_count, "date": date, "category_name": category_name, "payment_name": payment_name,
                   "transaction": transaction, "comments": comments}
        # Create a new expense dictionary and add the expense properties to the dictionary
        expenses_arr.append(expense)  # Save the expense dictionary in the expenses array
        file1 = open("files/Expenses.csv", "w")
        file1.seek(0)
        file1.truncate()
        writer = csv.writer(file1, dialect='comma')
        for dic in expenses_arr:
            temp_list = list(dic.values())
            writer.writerow(temp_list)
        file1.close()
        self.clear_text_data()  # Clear all input fields
        messagebox.showinfo("Success", "ההוצאה נוספה בהצלחה!")

    def clear_text_data(self):  # Clear all input fields
        self.NewDate.delete('0', tk.END)
        self.var1.set("בחר")
        self.var2.set("בחר")
        self.NewTransaction.delete('0', tk.END)
        self.NewComments.delete('0', tk.END)
