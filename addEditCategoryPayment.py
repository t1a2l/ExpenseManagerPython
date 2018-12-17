import tkinter as tk
from PIL import Image, ImageTk


class AddEditCategoryPaymentMain(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        img = Image.open("images/CategoryPaymentMainScreenImage.png")
        img = img.resize((1000, 800), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(img)
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.PrgLbl = tk.Label(self, text="שינוי/הוספה \n של קטגוריה/אמצעי תשלום", font=("Times New Rome", "48", "bold")
                               , fg="black", bg="white")
        self.PrgLbl.place(relx=0.5, rely=0.15, anchor="c")

        self.ExpensesBtn = tk.Button(self, text="חפש קטגוריה/אמצעי תשלום קיים", font=("Times New Rome", "18", "bold"),
                                     bg="gray91", fg="black", command=lambda: controller.show_frame(
                "SearchCategoryPaymentMain"))
        self.ExpensesBtn.place(relx=0.72, rely=0.5, anchor="c")

        self.addEditExpenseBtn = tk.Button(self, text="הוסף קטגוריה/אמצעי תשלום חדש", bg="gray91", fg="black", font=(
                                            "Times New Rome", "18", "bold"), command=lambda: controller.show_frame(
            "AddNewCategoryPaymentMain"))
        self.addEditExpenseBtn.place(relx=0.33, rely=0.5, anchor="c")

        self.addEditCategoryPaymentBtn = tk.Button(self, text="חזרה", font=("Times New Rome", "18", "bold"), bg="gray91"
                                                   , fg="black", command=lambda: controller.show_frame("ExpenseMain"))
        self.addEditCategoryPaymentBtn.place(relx=0.2, rely=0.8, anchor="c")
