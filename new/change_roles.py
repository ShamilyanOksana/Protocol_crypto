from tkinter import *
from random import *


def start(_p, _g):
    global root
    global p
    p = _p
    global g
    g = _g
    root = Tk()
    root.title("Поменятся ролями")
    root.geometry('800x600')
    geometry_x = (root.winfo_screenwidth() - root.winfo_reqwidth()) // 3.5
    geometry_y = (root.winfo_screenheight() - root.winfo_reqheight()) // 3.5
    root.wm_geometry("+%d+%d" % (geometry_x, geometry_y))

    m = Menu(root)
    root.config(menu=m)
    help_menu = Menu(m)
    m.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="Help")
    help_menu.add_command(label="About")

    p_label = Label(root, text='p = %d' % p, font=14)
    p_label.place(x=450, y=5)

    g_label = Label(root, text='g = %d' % g, font=14)
    g_label.place(x=550, y=5)

    turn = Label(root, fg='blue', text='ХОД ПОЛЬЗОВАТЕЛЯ:')
    turn.place(x=5, y=5)

    comment = Label(root, fg='green',
                    text='Выберите случайное число х из элементов предложенных ниже и вычислите  y = (g^x) mod p')
    comment.place(x=5, y=30)

    global Z
    Z = []
    f_p = p - 1
    for l in range(1, f_p):
        if (g ** l) % p == 1:
            break
        else:
            Z.append((g ** l) % p)
    print(Z)

    comment = Label(root, fg='green', text='Мультипликативная группа: '+str(Z))
    comment.place(x=5, y=50)

    comment = Label(root, bg='orange', text='Пользователь:')
    comment.place(x=5, y=95)

    comment = Label(root, text='x = ')
    comment.place(x=100, y=80)
    global enter_x
    enter_x = Entry(root)
    enter_x.place(x=130, y=80)

    comment = Label(root, text='y = ')
    comment.place(x=100, y=110)
    global enter_y
    enter_y = Entry(root)
    enter_y.place(x=130, y=110)
    global ok_button
    ok_button = Button(root, text='Продолжить', command=check_x_y)
    ok_button.place(x=280, y=105)
    root.mainloop()


def check_x_y():
    global root
    global enter_x
    global enter_y
    global Z
    global p
    global g
    global ok_button
    x = enter_x.get()
    y = enter_y.get()
    if x == "" or y == "":
        error_label = Label(root, text='Данные введены неверно', fg='red')
        error_label.place(x=380, y=105)
    elif (not x.isdigit()) or (not y.isdigit()):
        error_label = Label(root, text='Данные введены неверно', fg='red')
        error_label.place(x=380, y=105)
    elif (int(x) not in Z) or (int(y) != (g**(int(x))) % p):
        error_label = Label(root, text='Данные введены неверно', fg='red')
        error_label.place(x=380, y=105)
    else:
        error_label = Label(root, text='Данные введены верно      ', fg='green')
        error_label.place(x=380, y=105)
        ok_button.destroy()
        next_turn()


def next_turn():
    global Z
    global enter_y

    turn = Label(root, fg='blue', text='ХОД КОМПЬЮТЕРА:')
    turn.place(x=5, y=140)

    comment = Label(root, text='Компьютер выбирает два числа - k и b', fg='green')
    comment.place(x=5, y=160)
    comment = Label(root, text='Значение  k  выбирается из мультипликативной группы, значение  b  равно либо 0, либо 1', fg='green')
    comment.place(x=5, y=180)
    comment = Label(root, text='И с помощью выбранных значений считает значение r = ((y^b) * (g^k)) mod p и передает его пользователю', fg='green')
    comment.place(x=5, y=200)
    global k
    global b
    k = Z[randint(0, len(Z)-1)]
    b = randint(0, 1)
    y = int(enter_y.get())
    print('k = ', k)
    print('b = ', b)
    r = ((y**b) * (g**k)) % p
    comment = Label(root, bg='yellow', text='Компьютер:')
    comment.place(x=5, y=220)

    comment = Label(root, text='r = %d' % r)
    comment.place(x=100, y=220)

    turn = Label(root, fg='blue', text='ХОД ПОЛЬЗОВАТЕЛЯ:')
    turn.place(x=5, y=250)

    comment = Label(root, text='Пользователь выбирает случайный бит  с,  значение которого равно либо 0, либо 1', fg='green')
    comment.place(x=5, y=270)

    comment = Label(root, bg='orange', text='Пользователь:')
    comment.place(x=5, y=300)
    comment = Label(root, text='c = ')
    comment.place(x=100, y=300)
    global enter_c
    enter_c = Entry(root)
    enter_c.place(x=130, y=300)
    global ok_button
    ok_button = Button(root, text='Продолжить', command=check_c)
    ok_button.place(x=280, y=295)

def check_c():
    global enter_c
    global ok_button
    c = enter_c.get()
    if c == "":
        error_label = Label(root, text='Данные введены неверно', fg='red')
        error_label.place(x=380, y=295)
    elif not(c.isdigit()):
        error_label = Label(root, text='Данные введены неверно', fg='red')
        error_label.place(x=380, y=295)
    elif c == "0" or c == "1":
        error_label = Label(root, text='Данные введены верно   ', fg='green')
        error_label.place(x=380, y=295)
        ok_button.destroy()
        get_k_b()


def get_k_b():
    global k
    global b
    turn = Label(root, fg='blue', text='ХОД КОМПЬЮТЕРА:')
    turn.place(x=5, y=325)

    comment = Label(root, text='Компьютер передает Пользователю значения k и b, выбранные для подсчета r', fg='green')
    comment.place(x=5, y=345)

    comment = Label(root, bg='yellow', text='Компьютер:')
    comment.place(x=5, y=385)

    comment = Label(root, text='k = %d' % k)
    comment.place(x=100, y=370)

    comment=Label(root, text='b = %d' % b)
    comment.place(x=100, y=400)

    count_d()


def count_d():
    global b
    global enter_c
    c = int(enter_c.get())
    d = b ^ c
    name_result = Label(root, bg='lightgreen', text='Результат выполнения протокола: ')
    name_result.place(x=0, y=450)
    result_lable = Label(root, fg='red', text=str(d))
    result_lable.place(x=250, y=450)

    close_button = Button(root, text='Закрыть', command=close)
    close_button.place(x=230, y=570)


def close():
    root.destroy()
