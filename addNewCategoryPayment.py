import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class AddNewCategoryPaymentMain(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        var = tk.IntVar()

        # Set background image
        img = Image.open("images/NewCategoryPaymentImage.png")
        img = img.resize((1000, 800), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(img)
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.PrgLbl = tk.Label(self, text="הוספת קטגוריה \n או אמצעי תשלום חדש", font=("Times New Rome", "48", "bold"),
                               fg="black", bg="snow")
        self.PrgLbl.place(relx=0.5, rely=0.2, anchor="c")

        self.category = tk.Radiobutton(self, text="קטגוריה", font=("Times New Rome", "18", "bold"), variable=var,
                                       value=1)
        self.category.place(relx=0.6, rely=0.35, anchor="c")
        self.category.select()

        self.payment = tk.Radiobutton(self, text="אמצעי תשלום", font=("Times New Rome", "18", "bold"), variable=var,
                                      value=2)
        self.payment.place(relx=0.4, rely=0.35, anchor="c")

        self.InputCategoryPayment = tk.Entry(self, width="30", font=("Times New Rome", "18", "bold"))
        self.InputCategoryPayment.place(relx=0.5, rely=0.42, anchor="c")

        self.AddNewCategoryPaymentButton = tk.Button(self, text="הוסף קטגוריה/אמצעי תשלום", bg="gray91", fg="black",
                                                     font=("Times New Rome", "18", "bold"),
                                                     command=lambda: self.choose_type(var))
        self.AddNewCategoryPaymentButton.place(relx=0.62, rely=0.5, anchor="c")

        self.BackBtn = tk.Button(self, text="חזרה", font=("Times New Rome", "18", "bold"), bg="gray91", fg="black",
                                 command=lambda: controller.show_frame("AddEditCategoryPaymentMain"))
        self.BackBtn.place(relx=0.3, rely=0.5, anchor="c")

    def choose_type(self, var):  # Choose what type to add: category or payment method
        selection = var.get()
        if selection == 1:
            self.save_new_category()
        elif selection == 2:
            self.save_new_payment()
        
    def save_new_category(self):  # Save new category
        category_arr = []
        file = open("files/Categories.txt", "r")  # Get categories from file
        for line in file:
            line = line.strip()
            category_arr.append(line)
        file.close()
        new_category = self.InputCategoryPayment.get()  # Get new category from textbox
        if new_category == "":
            messagebox.showinfo("Error", "נא הזן קטגוריה!")
            return
        for i in category_arr:  # Check if the category exist already
            if new_category == i:
                messagebox.showinfo("Error", "הקטגוריה הנוכחית כבר קיימת!")
                return
        category_arr.append(new_category)  # Add new category to the category list
        file1 = open("files/Categories.txt", "w")  # Write all categories to file
        file1.seek(0)
        file1.truncate()
        file1.write('\n'.join(category_arr))
        file1.close()
        self.clear_text_data()  # Clear input field
        messagebox.showinfo("Success", "הקטגוריה נוספה בהצלחה!")

    def save_new_payment(self):  # Save new category
        payment_arr = []
        file = open("files/PaymentMethods.txt", "r")  # Get payment methods from file
        for line in file:
            line = line.strip()
            payment_arr.append(line)
        file.close()
        new_payment = self.InputCategoryPayment.get()  # Get new category from textbox
        if new_payment == "":
            messagebox.showinfo("Error", "נא הזן אמצעי תשלום!")
            return
        for i in payment_arr:  # Check if the category exist already
            if new_payment == i:
                messagebox.showinfo("Error", "אמצעי התשלום הנוכחי כבר קיים!")
                return
        payment_arr.append(new_payment)  # Add new category to the category list
        file1 = open("files/PaymentMethods.txt", "w")  # Write all categories to file
        file1.seek(0)
        file1.truncate()
        file1.write('\n'.join(payment_arr))
        file1.close()
        self.clear_text_data()  # Clear input field
        messagebox.showinfo("Success", "אמצעי התשלום נוסף בהצלחה!")

    def clear_text_data(self):  # Clear input field
        self.InputCategoryPayment.delete('0', tk.END)
