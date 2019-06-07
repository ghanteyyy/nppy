from __future__ import division  # If python is 2.x

try:  # Python 3
    from tkinter import *

except (ImportError, ModuleNotFoundError):  # Python 2
    from Tkinter import *


def show_scrollbar():
    '''show scrollbar when text is more than the text area'''

    if history_area.cget('height') < int(history_area.index('end-1c').split('.')[0]):
        scrollbar.grid(column=1, row=0, sticky=N + S)
        history_area.config(yscrollcommand=scrollbar.set)
        root.after(100, hide_scrollbar)

    else:
        root.after(100, show_scrollbar)


def hide_scrollbar():
    '''hide scrollbar when text is less than the text area'''

    if history_area.cget('height') >= int(history_area.index('end-1c').split('.')[0]):
        scrollbar.grid_forget()
        history_area.config(yscrollcommand=None)
        root.after(100, show_scrollbar)

    else:
        root.after(100, hide_scrollbar)


def clear_history():
    '''Clear calculation history'''

    history_area.config(state=NORMAL)
    history_area.delete('1.0', 'end')
    history_area.insert('end', 'There\'s no history yet.')
    history_area.config(state=DISABLED)


def remove_decimal(result):
    '''Remove '.0' if result are 14.0, 99.0, 45.0'''

    global split

    split = result.partition('.')

    if split[-1] == '0':
        return True

    else:
        return False


def history(value=None):
    '''Display previous calculations'''

    history_area.config(state=NORMAL)

    get = history_area.get('1.0', 'end-1c')

    if len(get) == 0:
        history_area.insert('end', 'There\'s no history yet.')
        history_area.config(state=DISABLED)

    else:
        if get == 'There\'s no history yet.':
            history_area.delete('1.0', 'end')
            history_area.insert('end', value)
            history_area.config(state=DISABLED)

        else:
            history_area.insert('end', value)
            history_area.config(state=DISABLED)


def keyaction(event):
    '''Check if the input key is between 0123456789+-*./% c '''

    if text_area.get() == 'Invalid Input':
        var.set('')

    if event.char in '0123456789+-*./%':
        val = text_area.get() + event.char
        var.set(val)

    if event.char is 'c':
        var.set('')

    if event.char is 'h':
        clear_history()


def equals_to(event=None):
    '''Calculate the given equation'''

    value = text_area.get().lstrip('0').replace('%', '/100')

    try:
        calc = str(eval(value))

        if remove_decimal(calc):
            hist = '{} = {}\n'.format(text_area.get().lstrip('0'), split[0])
            var.set(split[0])
            history(hist)

        else:
            hist = '{} = {}\n'.format(text_area.get().lstrip('0'), calc)
            var.set(calc)
            history(hist)

    except ZeroDivisionError:
        var.set('Cannot divide by ZERO')

    except SyntaxError:
        var.set('Invalid Input')


def set_value(value):
    '''Display entered value'''

    if text_area.get() == 'Invalid Input':
        var.set('')

    val = text_area.get() + value
    var.set(val)


def main():
    global root, var, text_area, history_area, scrollbar

    root = Tk()
    root.withdraw()
    root.after(0, root.deiconify)
    root.title('Calculator')
    root.iconbitmap('icon.ico')
    root.resizable(0, 0)

    # pos_x and pos_y are calculated such that the window is at the center of the screen
    pos_x = int(root.winfo_screenwidth() / 2) - int(342 / 2)
    pos_y = int(root.winfo_screenheight() / 2) - int(263 / 2)

    root.geometry('550x263+{}+{}'.format(pos_x, pos_y))

    var = StringVar()
    text_frame = Frame(root)
    text_area = Entry(text_frame, textvariable=var, borderwidth=1, width=21, bg='silver', font=("Arial", 20), cursor='arrow', justify=RIGHT)
    text_area.configure(state='disabled', disabledbackground='white', disabledforeground='black')
    text_area.grid(row=0, column=0, columnspan=5)
    text_frame.place(x=10, y=10)

    # Buttons
    buttons_frame = Frame(root)
    nine_button = Button(buttons_frame, text='9', width=10, height=2, bg='grey', fg='black', activebackground='grey', relief='groove', command=lambda: set_value('9'))
    eight_button = Button(buttons_frame, text='8', width=10, height=2, bg='grey', fg='black', activebackground='grey', relief='groove', command=lambda: set_value('8'))
    seven_button = Button(buttons_frame, text='7', width=10, height=2, bg='grey', fg='black', activebackground='grey', relief='groove', command=lambda: set_value('7'))
    six_button = Button(buttons_frame, text='6', width=10, height=2, bg='grey', fg='black', activebackground='grey', relief='groove', command=lambda: set_value('6'))
    five_button = Button(buttons_frame, text='5', width=10, height=2, bg='grey', fg='black', activebackground='grey', relief='groove', command=lambda: set_value('5'))
    four_button = Button(buttons_frame, text='4', width=10, height=2, bg='grey', fg='black', activebackground='grey', relief='groove', command=lambda: set_value('4'))
    three_button = Button(buttons_frame, text='3', width=10, height=2, bg='grey', fg='black', activebackground='grey', relief='groove', command=lambda: set_value('3'))
    two_button = Button(buttons_frame, text='2', width=10, height=2, bg='grey', fg='black', activebackground='grey', relief='groove', command=lambda: set_value('2'))
    one_button = Button(buttons_frame, text='1', width=10, height=2, bg='grey', fg='black', activebackground='grey', relief='groove', command=lambda: set_value('1'))
    zero_button = Button(buttons_frame, text='0', width=10, height=2, bg='grey', fg='black', activebackground='grey', relief='groove', command=lambda: set_value('0'))
    del_button = Button(buttons_frame, text='DEL', width=10, height=2, bg='grey', fg='black', activebackground='grey', relief='groove', command=lambda: var.set(text_area.get()[:-1]))
    ac_button = Button(buttons_frame, text='AC', width=10, height=2, bg='grey', fg='black', activebackground='grey', relief='groove', command=lambda: var.set(''))
    multiply_button = Button(buttons_frame, text='*', width=10, height=2, bg='grey', fg='black', activebackground='grey', relief='groove', command=lambda: set_value('*'))
    divide_button = Button(buttons_frame, text='/', width=10, height=2, bg='grey', fg='black', activebackground='grey', relief='groove', command=lambda: set_value('/'))
    plus_button = Button(buttons_frame, text='+', width=10, height=2, bg='grey', fg='black', activebackground='grey', relief='groove', command=lambda: set_value('+'))
    minus_button = Button(buttons_frame, text='-', width=10, height=2, bg='grey', fg='black', activebackground='grey', relief='groove', command=lambda: set_value('-'))
    percent_button = Button(buttons_frame, text='%', width=10, height=2, bg='grey', fg='black', activebackground='grey', relief='groove', command=lambda: set_value('%'))
    point_button = Button(buttons_frame, text='.', width=10, height=2, bg='grey', fg='black', activebackground='grey', relief='groove', command=lambda: set_value('.'))
    equal_button = Button(buttons_frame, text='=', width=10, height=2, bg='grey', fg='black', activebackground='grey', relief='groove', padx=41, command=lambda: equals_to())
    buttons_frame.place(x=10, y=50)

    history_label_frame = Frame()
    history_label = Label(history_label_frame, text='History', font=('Courier', 15), bg='grey')
    history_label.grid(row=0, column=0)
    history_label_frame.place(x=335, y=-1)

    history_frame = Frame(root)
    history_area = Text(history_frame, width=25, height=13, borderwidth=0, cursor='arrow', bg='grey')
    history_area.grid(row=0, column=0)
    history_frame.place(x=332, y=35)

    # Attaching scrollbar to the text area
    scrollbar = Scrollbar(history_frame, orient="vertical", command=history_area.yview, cursor='arrow')
    history_area['yscrollcommand'] = scrollbar.set

    zero_button.grid(row=4, column=2)
    point_button.grid(row=4, column=1)
    nine_button.grid(row=1, column=3)
    eight_button.grid(row=1, column=2)
    seven_button.grid(row=1, column=1)
    six_button.grid(row=2, column=3)
    five_button.grid(row=2, column=2)
    four_button.grid(row=2, column=1)
    three_button.grid(row=3, column=3)
    two_button.grid(row=3, column=2)
    one_button.grid(row=3, column=1)
    divide_button.grid(row=0, column=4)
    multiply_button.grid(row=1, column=4)
    minus_button.grid(row=2, column=4)
    plus_button.grid(row=3, column=4)
    percent_button.grid(row=0, column=3)
    del_button.grid(row=0, column=2)
    ac_button.grid(row=0, column=1)
    equal_button.grid(row=4, column=3, columnspan=2)

    clear_history_frame = Frame(root)
    clear_history_button = Button(clear_history_frame, text='CLEAR', bg='grey', activebackground='grey', fg='black', relief='groove', command=clear_history)
    clear_history_button.grid(row=0, column=0)
    clear_history_frame.place(x=500, y=5)

    # Binding keys
    root.bind('<Key>', lambda evt: keyaction(evt))
    root.bind('<Return>', equals_to)
    root.bind('<BackSpace>', lambda e: var.set(text_area.get()[:-1]))

    history()  # Calling history function
    show_scrollbar()

    root.config(bg='grey')
    history_area.config(state=DISABLED)
    root.mainloop()


if __name__ == '__main__':
    main()
