import tkinter as tk
from PIL import Image, ImageTk
from ExpenseManager import addEditExpense, addNewExpense, SearchExpense, addEditCategoryPayment, addNewCategoryPayment, \
    SearchCategoryPayment, tkcal


class ExpenseApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        # SearchCategoryPayment.SearchCategoryPaymentMain
        self.frames = {}
        for F in (ExpenseMain, tkcal.CalendarMain, addNewExpense.AddNewExpenseMain, SearchExpense.SearchExpenseMain,
                  addEditExpense.AddEditExpenseMain, addNewCategoryPayment.AddNewCategoryPaymentMain,
                  SearchCategoryPayment.SearchCategoryPaymentMain, addEditCategoryPayment.AddEditCategoryPaymentMain):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("ExpenseMain")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def get_page(self, page_class):
        return self.frames[page_class]


class ExpenseMain(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # screen_width = self.winfo_screenwidth()
        # screen_height = self.winfo_screenheight()

        img = Image.open("images/MainScreenImage.png")
        img = img.resize((1000, 800), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(img)
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        PrgLbl = tk.Label(self, text="מערכת לניהול הוצאות", fg="black", font=("Times New Rome", "48", "bold"),
                          bg="snow")
        PrgLbl.place(relx=0.5, rely=0.2, anchor="c")

        ExpensesBtn = tk.Button(self, text="הוצאות", bg="gray91", fg="black", font=("Times New Rome", "18", "bold"),
                                command="")
        ExpensesBtn.place(relx=0.82, rely=0.5, anchor="c")

        addEditExpenseBtn = tk.Button(self, text="הוסף/שנה הוצאה", font=("Times New Rome", "18", "bold"), bg="gray91",
                                      fg="black", command=lambda: controller.show_frame("AddEditExpenseMain"))
        addEditExpenseBtn.place(relx=0.63, rely=0.5, anchor="c")

        addEditCategoryPaymentBtn = tk.Button(self, text="הוסף/שנה קטגוריה או אמצעי תשלום", bg="gray91", fg="black",
                                              font=("Times New Rome", "18", "bold"), command=lambda: controller.
                                              show_frame("AddEditCategoryPaymentMain"))
        addEditCategoryPaymentBtn.place(relx=0.3, rely=0.5, anchor="c")


if __name__ == "__main__":
    root = ExpenseApp()
    root.geometry("1000x800")
    root.resizable(0, 0)
    root.mainloop()
