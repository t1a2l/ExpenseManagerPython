import calendar as ca
import datetime as dt


try:
    import Tkinter
    import tkfont
except ImportError:  # py3k
    import tkinter as tkinter
    import tkinter.font as tkfont

import tkinter.ttk as ttk


class CalendarMain(tkinter.Frame):

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        self.newWindow = None
        self.calendar = None

    def create_inner(self):
        return CalendarMain.Calendar(self)

    @staticmethod
    def get_calendar(locale, fwday):
        # instantiate proper calendar class
        if locale is None:
            return ca.TextCalendar(fwday)
        else:
            return ca.LocaleTextCalendar(fwday, locale)

    def select_date(self):
        import sys
        self.calendar = self.controller.get_page('AddNewExpenseMain')

        root = tkinter.Toplevel(self.controller)
        root.title('Ttk Calendar')
        root.resizable(0, 0)

        ttkcal = self.Calendar(root, firstweekday=ca.SUNDAY)
        # self.calendar.NewDate.insert(ttkcal.selected_date, tkinter.END)

        ttkcal.pack(expand=1, fill='both')

        if 'win' not in sys.platform:
            style = ttk.Style()
            style.theme_use('clam')

        root.mainloop()

    class Calendar(ttk.Frame):

        timedelta = dt.timedelta
        datetime = dt.datetime

        def __init__(self, master, **kw):
            self.master = master
            """
            WIDGET-SPECIFIC OPTIONS
                locale, firstweekday, year, month, selectbackground,
                selectforeground
            """
            # remove custom options from kw before initializing ttk.Frame
            self.fwday = kw.pop('firstweekday', ca.MONDAY)
            year = kw.pop('year', self.datetime.now().year)
            month = kw.pop('month', self.datetime.now().month)
            self.locale = kw.pop('locale', None)
            self.sel_bg = kw.pop('selectbackground', '#ecffc4')
            self.sel_fg = kw.pop('selectforeground', '#05640e')
            self.ismonth = 0
            self._cal = None
            self._items = None
            self._date = self.datetime(year, month, 1)
            self._selection = None  # no date selected
            self.hframe = None
            self.headerbtn = None
            self.lbtn = None
            self.rbtn = None
            self._canvas = None
            self._items = []
            self.item_range = 6
            ttk.Frame.__init__(self, master, **kw)
            self.kw = kw
            self.init_calendar()
            self.selected_date = None

        def init_calendar(self):

            self.__place_widgets()      # pack/grid used widgets

            if self.ismonth == 0:
                self._cal = CalendarMain.get_calendar(self.locale, self.fwday)
                self.__config_calendar()  # adjust calendar columns and setup tags
                # store items ids, used for insertion later
                self._items = [self._calendar.insert('', 'end', values='') for _ in range(6)]
            elif self.ismonth == 1:
                self._cal = [['Jan', 'Feb', 'Mar', 'Apr'], ['May', 'Jun', 'Jul', 'Aug'], ['Sep', 'Oct', 'Nov', 'Dec']]
                self.__config_calendar()  # adjust calendar columns and setup tags
                self._items = [self._calendar.insert('', 'end', values='') for _ in range(4)]
            else:
                return

            self.__setup_styles()  # creates custom styles
            # configure a canvas, and proper bindings, for selecting dates

            self.__setup_selection(self.sel_bg, self.sel_fg)

            # insert dates in the currently empty calendar
            self._build_calendar()

        def __setitem__(self, item, value):
            if item in ('year', 'month'):
                raise AttributeError("attribute '%s' is not writeable" % item)
            elif item == 'selectbackground':
                self._canvas['background'] = value
            elif item == 'selectforeground':
                self._canvas.itemconfigure(self._canvas, item=value)
            else:
                ttk.Frame.__setitem__(self, item, value)

        def __getitem__(self, item):
            if item in ('year', 'month'):
                return getattr(self._date, item)
            elif item == 'selectbackground':
                return self._canvas['background']
            elif item == 'selectforeground':
                return self._canvas.itemcget(self._canvas, 'fill')
            else:
                r = ttk.tclobjs_to_py({item: ttk.Frame.__getitem__(self, item)})
                return r[item]

        def __setup_styles(self):
            # custom ttk styles
            style = ttk.Style(self.master)

            def arrow_layout(mydir): return [('Button.focus', {'children': [('Button.%sarrow' % mydir, None)]})]

            style.layout('L.TButton', arrow_layout('left'))
            style.layout('R.TButton', arrow_layout('right'))

        def __place_widgets(self):
            # header frame and its widgets
            if self.headerbtn is not None:
                self.headerbtn.grid_remove()
                self.lbtn.grid_remove()
                self.rbtn.grid_remove()
                self.hframe.pack_forget()
            self.hframe = ttk.Frame(self)
            self.lbtn = ttk.Button(self.hframe, style='L.TButton', command=self._prev_month)
            self.rbtn = ttk.Button(self.hframe, style='R.TButton', command=self._next_month)
            self.headerbtn = ttk.Button(self.hframe, text="", command="")
            # the calendar
            self._calendar = ttk.Treeview(self, show='', selectmode='none', height=7)

            # pack the widgets
            self.hframe.pack(in_=self, side='top', pady=4, anchor='center')
            self.lbtn.grid(in_=self.hframe)
            self.headerbtn.grid(in_=self.hframe, column=1, row=0, padx=12)
            self.rbtn.grid(in_=self.hframe, column=2, row=0)
            self._calendar.pack(in_=self, expand=1, fill='both', side='bottom')

        # def _header_pressed(self):
        #     i = 1
        #     # for item in self._calendar.get_children():
        #     #     self._calendar.delete(item)
        #     # ttk.Frame.destroy(self)
        #     # ttk.Frame.__init__(self, None, **self.kw)
        #     # self._items = []
        #     # self._cal = None
        #     #
        #     # if self.ismonth == 0:
        #     #     self.ismonth = 1
        #     #     self.init_calendar()
        #     # elif self.ismonth == 1:
        #     #     self.ismonth = 0
        #     #     self.init_calendar()

        def __config_calendar(self):  # Show calendar header - weekdays or none
            if self.ismonth == 0:
                cols = self._cal.formatweekheader(3).split()
                self._calendar['columns'] = cols
                self._calendar.tag_configure('header', background='grey90')
                self._calendar.insert('', 'end', values=cols, tag='header')
                # for i in self._calendar.get_children():
                # adjust its columns width
                font = tkfont.Font()
                maxwidth = max(font.measure(col) for col in cols)
                for col in cols:
                    self._calendar.column(col, width=maxwidth, minwidth=maxwidth, anchor='e')
            else:
                cols = ['Sun', 'Mon', 'Tue', 'Wed']
                self._calendar['columns'] = cols
                self._calendar.tag_configure('header', background='grey90')
                self._calendar.insert('', 'end', values="", tag='header')
                font = tkfont.Font()
                maxwidth = max(font.measure(col) for col in cols)
                for col in cols:
                    self._calendar.column(col, width=maxwidth, minwidth=maxwidth, anchor='c')

        def __setup_selection(self, sel_bg, sel_fg):
            self._font = tkfont.Font()
            self._canvas = canvas = tkinter.Canvas(self._calendar, background=sel_bg, borderwidth=0,
                                                   highlightthickness=0)
            canvas.text = canvas.create_text(0, 0, fill=sel_fg, anchor='w')

            canvas.bind('<ButtonPress-1>', lambda evt: canvas.place_forget())
            self._calendar.bind('<Configure>', lambda evt: canvas.place_forget())
            self._calendar.bind('<ButtonPress-1>', self._pressed)

        def _build_calendar(self):
            year = self._date.year
            if self.ismonth == 1:
                self.headerbtn['text'] = self._date.year
                for indx, item in enumerate(self._items):
                    monthrow = self._cal[indx] if indx < len(self._cal) else []
                    fmt_month = [month if month else '' for month in monthrow]
                    self._calendar.item(item, values=fmt_month)
            else:
                month = self._date.month
                cal = self._cal.monthdayscalendar(year, month)
                header = self._cal.formatmonthname(year, month, 0)
                self.headerbtn['text'] = header.title()
                for indx, item in enumerate(self._items):
                    week = cal[indx] if indx < len(cal) else []
                    fmt_week = [('%02d' % day) if day else '' for day in week]
                    self._calendar.item(item, values=fmt_week)

        def _show_selection(self, text, bbox):
            """Configure canvas for a new selection."""

            x, y, width, height = bbox
            self._canvas.delete("all")
            textw = self._font.measure(text)
            canvas = self._canvas
            my_text = canvas.create_text(x, y)
            canvas.configure(width=width, height=height)
            canvas.coords(my_text, width - textw, height / 2 - 1)
            canvas.itemconfigure(my_text, text=text)
            canvas.place(in_=self._calendar, x=x, y=y)
            self.selected_date = text + "/" + str(self._date.month) + "/" + str(self._date.year)

        def _pressed(self, evt):
            """Clicked somewhere in the calendar."""
            x, y, widget = evt.x, evt.y, evt.widget
            item = widget.identify_row(y)
            column = widget.identify_column(x)

            if (not column or not item) in self._items:
                # clicked in the weekdays row or just outside the columns
                return

            item_values = widget.item(item)['values']
            if not len(item_values):  # row is empty for this month
                return

            text = item_values[int(column[1]) - 1]
            if not text:  # date is empty
                return

            bbox = widget.bbox(item, column)
            if not bbox:  # calendar not visible yet
                return

            if not isinstance(text, str):
                # update and then show selection
                text = '%02d' % text
                self._selection = (text, item, column)
                self._show_selection(text, bbox)

        def _prev_month(self):
            if self.ismonth == 1:
                """Updated calendar to show the previous month."""
                self._canvas.place_forget()

                self._date = self._date - self.timedelta(days=1)
                self._date = self.datetime(self._date.year, self._date.month, 1)
            else:
                """Updated calendar to show the previous month."""
                self._canvas.place_forget()

                self._date = self._date - self.timedelta(days=1)
                self._date = self.datetime(self._date.year, self._date.month, 1)
            self._build_calendar()  # reconstuct calendar

        def _next_month(self):
            """Update calendar to show the next month."""
            self._canvas.place_forget()

            year, month = self._date.year, self._date.month
            self._date = self._date + self.timedelta(
                days=ca.monthrange(year, month)[1] + 1)
            self._date = self.datetime(self._date.year, self._date.month, 1)
            self._build_calendar()  # reconstruct calendar

        # Properties

        @property
        def selection(self):
            """Return a datetime representing the current selected date."""
            if not self._selection:
                return None

            year, month = self._date.year, self._date.month
            return self.datetime(year, month, int(self._selection[0]))
