from tkinter import *
from random import *
from change_roles import start as change_roles

def main_page():
    global mainroot
    mainroot = Tk()

    m = Menu(mainroot)
    mainroot.configure(menu=m)
    help_menu = Menu(m)
    m.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="Help", command=help)

    mainroot.title("Главное меню")
    mainroot.geometry('250x100')
    geometry_x = (mainroot.winfo_screenwidth() - mainroot.winfo_reqwidth()) // 3.5
    geometry_y = (mainroot.winfo_screenheight() - mainroot.winfo_reqheight()) // 3.5
    mainroot.wm_geometry("+%d+%d" % (geometry_x, geometry_y))


    text = Label(mainroot, text="Выберете один из вариантов")
    text.pack()
    first = Button(mainroot, text='Построение мультипликативной группы', command=start1, width=200)
    first.pack()
    second = Button(mainroot, text='Без подмены бита', command=start2, width=200)
    second.pack()
    third = Button(mainroot, text='C подменой бита', command=start3, width=200)
    third.pack()
    mainroot.mainloop()


def start1():
    mainroot.destroy()
    global ind
    ind = 1
    start()


def start2():
    mainroot.destroy()
    global ind
    ind = 2
    start()


def start3():
    mainroot.destroy()
    global ind
    ind = 3
    start()


def start():
    global root
    root = Tk()
    if ind == 1:
        root.title("Построение мультипликативной группы")
    elif ind == 2:
        root.title("Без подмены бита")
    elif ind == 3:
        root.title("С подменой бита")
    root.geometry('350x200')
    geometry_x = (root.winfo_screenwidth() - root.winfo_reqwidth()) // 3.5
    geometry_y = (root.winfo_screenheight() - root.winfo_reqheight()) // 3.5
    root.wm_geometry("+%d+%d" % (geometry_x, geometry_y))
    m = Menu(root)
    root.config(menu=m)
    help_menu = Menu(m)
    m.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="Help", command=help)

    text_label = Label(root, text='Выберете простое число p,\n значение которого не превышает 100')
    text_label.grid(row=1, column=0)
    global p_text
    p_text = Entry(root)
    p_text.grid(row=1, column=1)
    space = Label(root, text='          \n           ')
    space.grid(row=2, column=0)
    text_label = Label(root, text='Выберете порождающий элемент\n мультипликативной группы g')
    text_label.grid(row=3, column=0)
    global g_text
    g_text = Entry(root)
    g_text.grid(row=3, column=1)

    ok_button = Button(root, text='Далее', command=check_p_g)
    ok_button.place(x=250, y=150)
    ok_button.bind("<1>")

    root.mainloop()


def check_p_g():
    arr = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
           47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    global root
    global p_text
    global g_text
    global p
    global g
    p = p_text.get()
    g = g_text.get()
    error_label = Label(root)
    error_label.destroy()
    if p == "" or g == "":
        error_label = Label(root, text='Не все поля заполнены!', fg='red')
        error_label.grid(row=5, column=0)
    elif not p.isdigit() or not g.isdigit():
        error_label = Label(root, text='Данные введены не верно!', fg='red')
        error_label.grid(row=5, column=0)
    elif (int(p) not in arr) or ((int(g)**(int(p)-1)) % int(p) != 1):
        error_label = Label(root, text='Данные введены не верно!', fg='red')
        error_label.grid(row=5, column=0)
    else:
        p = int(p)
        g = int(g)
        root.destroy()
        global ind
        if ind == 1:
            count()
        elif ind == 2 or ind == 3:
            create_Z_x_y()


def count():
    global root
    global p
    global g

    root = Tk()
    root.title("Построение мультипликативной группы")
    root.geometry('400x200')
    geometry_x = (root.winfo_screenwidth() - root.winfo_reqwidth()) // 3.5
    geometry_y = (root.winfo_screenheight() - root.winfo_reqheight()) // 3.5
    root.wm_geometry("+%d+%d" % (geometry_x, geometry_y))
    m = Menu(root)
    root.config(menu=m)
    help_menu = Menu(m)
    m.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="Help", command=help)

    p_text = Label(root, text='p = %s' % p, font=14)
    p_text.grid(row=0, column=0)

    g_text = Label(root, text='g = %s' % g, font=14)
    g_text.grid(row=0, column=1)

    g_text = Label(root)
    g_text.grid(row=0, column=2)

    enter_text = Label(root, text='Поочередно введите \nподсчитанные элементы \n мулитипликативной группы')
    enter_text.grid(row=2, column=0)
    global input_z
    global arr_z
    arr_z = []
    input_z = ''
    global text_area
    text_area = Entry(root)
    text_area.grid(row=2, column=1)
    ok_button = Button(root, text='Ввести значение', command=find)
    ok_button.grid(row=2, column=2)
    ok_button.bind("<1>")

    output_label = Label(root, text='Введенные значения:')
    output_label.grid(row=3, column=0)

    root.mainloop()


def find():
    global input_z
    global arr_z
    a = text_area.get()
    if a.isdigit():
        arr_z.append(int(a))
        input_z += a + '   '
        output_label = Label(root, text=input_z)
        output_label.place(x=5, y=100)
        next_button = Button(root, text='Завершить ввод', command=check_arr)
        next_button.place(x=10, y=150)
    text_area.delete(0, END)


def check_arr():
    global arr_z
    same = 0

    Z = []
    f_p = p - 1
    for l in range(1, f_p):
        if (g ** l) % p == 1:
            break
        else:
            Z.append((g ** l) % p)

    global root1
    root1 = Tk()
    root1.title("")
    root1.geometry('200x100')
    geometry_x = (root1.winfo_screenwidth() - root1.winfo_reqwidth()) // 3.5
    geometry_y = (root1.winfo_screenheight() - root1.winfo_reqheight()) // 3.5
    root1.wm_geometry("+%d+%d" % (geometry_x, geometry_y))

    m = Menu(root1)
    root1.config(menu=m)
    help_menu = Menu(m)
    m.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="Help", command=help)

    for i in range(len(arr_z)):
        if arr_z[i] in Z:
            same += 1
    if same == len(Z):
        next_label = Label(root1, text='Все верно!')
        next_label.pack()
        yes_button = Button(root1, text='Перейти в меню', command=go_to_main)
        yes_button.pack()
    else:
        next_label = Label(root1, text='Неверно!\nНачать заново?')
        next_label.pack()
        yes_button = Button(root1, text='Да', command=go_to_start)
        yes_button.pack()
        no_button = Button(root1, text='Нет', command=go_to_main)
        no_button.pack()


def go_to_start():
    root.destroy()
    if ind == 1:
        root1.destroy()
    start()


def go_to_main():

    if ind == 1:
        root.destroy()
        root1.destroy()
    if ind == 2 or ind == 3:
        root2.destroy()
    main_page()


def create_Z_x_y():
    global Z
    Z = []
    f_p = p - 1
    for l in range(1, f_p):
        if (g ** l) % p == 1:
            break
        else:
            Z.append((g ** l) % p)
    print(Z)

    index = randint(0, len(Z)-1)

    x = Z[index]
    global y
    y = (g ** x) % p


    global root2
    root2 = Tk()
    if ind == 2:
        root2.title("Без подмены бита")
    elif ind == 3:
        root2.title("С подменой бита")
    root2.geometry('800x600')
    geometry_x = (root2.winfo_screenwidth() - root2.winfo_reqwidth()) // 3.5
    geometry_y = (root2.winfo_screenheight() - root2.winfo_reqheight()) // 3.5
    root2.wm_geometry("+%d+%d" % (geometry_x, geometry_y))

    m = Menu(root2)
    root2.config(menu=m)
    help_menu = Menu(m)
    m.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="Help", command=help)

    p_label = Label(root2, text='p = %d' %p, font=14)
    p_label.place(x=450, y=5)

    g_label = Label(root2, text='g = %d' %g, font=14)
    g_label.place(x=550, y=5)

    turn = Label(root2, fg='blue', text='ХОД КОМПЬЮТЕРА:')
    turn.place(x=0, y=0)

    comment = Label(root2, fg='green',
                    text='Компьютер выбирает случайное число х и вычисляет       y = (g**x) mod p')
    comment.place(x=0, y=20)

    name_A = Label(root2, bg='yellow', text='Компьютер:')
    name_A.place(x=0, y=40)
    output_lable = Label(root2, text='y = ' + str(y))
    output_lable.place(x=100, y=40)

    turn = Label(root2, fg='blue', text='ХОД ПОЛЬЗОВАТЕЛЯ:')
    turn.place(x=0, y=80)
    comment = Label(root2, fg='green',
                    text="Для подсчета значения переменной r требуется ввести два значения - k и b. r = ((y**b) * (g**k)) mod p")
    comment.place(x=0, y=100)
    comment = Label(root2, fg='green',
                    text="ВЫБОР ЭЛЕМЕНТА k\n")
    comment.place(x=0, y=120)
    comment = Label(root2, fg='green',
                    text="Выберите любой элемент из предложенных ниже и запишите его в текстовое поле:")
    comment.place(x=0, y=140)

    comment = Label(root2, fg='green', text='Мультипликативная группа: '+str(Z))
    comment.place(x=0, y=160)

    global print_k
    print_k = Entry(root2)
    print_k.place(x=10, y=185)

    comment = Label(root2, fg='green', text='ВЫБОР ЭЛЕМЕНТА b')
    comment.place(x=0, y=205)

    comment = Label(root2, fg='green', text='Выберите чило либо 0, либо 1 и запишите его в текставое поле:')
    comment.place(x=0, y=225)

    global print_b
    print_b = Entry(root2)
    print_b.place(x=10, y=245)

    global ok_button
    ok_button = Button(root2, text='Продолжить', command=check_k_b)
    ok_button.place(x=240, y=245)
    ok_button.bind("<1>")


def check_k_b():
    global root2
    global print_k
    global print_b
    global Z
    b = print_b.get()
    k = print_k.get()
    if b == "" or k == "":
        error_label = Label(root2, text="Данные введены неверно", fg="red")
        error_label.place(x=350, y=245)
    elif not b.isdigit() or not k.isdigit():
        error_label = Label(root2, text="Данные введены неверно", fg="red")
        error_label.place(x=350, y=245)
    elif int(k) not in Z or (int(b) != 0 and int(b) != 1):
        error_label = Label(root2, text="Данные введены неверно", fg="red")
        error_label.place(x=350, y=245)

    else:
        error_label = Label(root2, text="Значение  k  и  b  подобраны верно", fg="green")
        error_label.place(x=350, y=245)
        count_r()


def count_r():
    global ok_button
    ok_button.destroy()

    name_B = Label(root2, bg='orange', text='Пользователь:')
    name_B.place(x=0, y=275)
    global print_r
    print_r = Label(root2, text='r = ')
    print_r.place(x=100, y=275)

    global enter_r
    enter_r = Entry(root2)
    enter_r.place(x=150, y=275)

    k = int(print_k.get())
    b = int(print_b.get())
    r = ((y ** b) * (g ** k)) % p
    print('r=', r)

    global Z
    for i in Z:
        for j in range(0, 2):
            if r == (y**j * g**i) % p and i != k and j != b:
                print('k=', i)
                print('b=', j)

    ok_button = Button(root2, text='Продолжить', command=check_r)
    ok_button.place(x=300, y=270)
    ok_button.bind("<1>")


def check_r():
    global enter_r
    global ok_button
    global print_r
    global r
    k = int(print_k.get())
    b = int(print_b.get())
    r = ((y ** b) * (g ** k)) % p
    if enter_r.get() == "":
        error_label = Label(root2, text="Данные введены неверно", fg="red")
        error_label.place(x=385, y=270)
    elif not enter_r.get().isdigit():
        error_label = Label(root2, text="Данные введены неверно", fg="red")
        error_label.place(x=385, y=270)
    elif int(enter_r.get()) == r:
        error_label = Label(root2, text='Значение  r  подобрано верно  ', fg='green')
        error_label.place(x=385, y=270)
        ok_button.destroy()
        next_turn()
    else:
        error_label = Label(root2, text='Данные введены неверно', fg='red')
        error_label.place(x=385, y=270)


def next_turn():

    k = int(print_k.get())
    b = int(print_b.get())

    turn = Label(root2, fg='blue', text='ХОД КОМПЬЮТЕРА:')
    turn.place(x=0, y=310)

    comment = Label(root2, fg='green', text='Компьютер случайно выбирает либо 0,либо 1')
    comment.place(x=0, y=330)
    global c
    c = randint(0, 1)
    name_A = Label(root2, bg='yellow', text='Компьютер: ')
    name_A.place(x=0, y=350)

    print_c = Label(root2, text='c = ' + str(c))
    print_c.place(x=100, y=350)

    turn = Label(root2, fg='blue', text='ХОД ПОЛЬЗОВАТЕЛЯ:')
    turn.place(x=0, y=390)
    global ind
    if ind == 2:
        comment = Label(root2, fg='green',
                        text='Компьютер выполняет проверку подлинности переданных ему занчений')
        comment.place(x=0, y=410)

        name_B = Label(root2, bg='orange', text='Пользователь: ')
        name_B.place(x=0, y=430)

        give_k = Label(root2, text='k = ' + str(k))
        give_k.place(x=100, y=430)
        give_b = Label(root2, text='b = ' + str(b))
        give_b.place(x=150, y=430)
        count_d()
    elif ind == 3:
        comment = Label(root2, fg='green',
                        text='Подберите такие значения k2 и b2, что \n'
                             'r2 = r1 = ((y**b)*(g**k)) mod p')
        comment.place(x=0, y=410)
        give_k = Label(root2, text='k = ')
        give_k.place(x=0, y=450)
        global k_entry
        k_entry = Entry(root2)
        k_entry.place(x=100, y=450)
        give_b = Label(root2, text='b = ')
        give_b.place(x=0, y=480)
        global b_entry
        b_entry = Entry(root2)
        b_entry.place(x=100, y=480)
        global ok_button
        ok_button = Button(root2, text='Продолжить', command=count_r2)
        ok_button.place(x=300, y=480)


def count_r2():
    global k_entry
    global b_entry
    global r
    global ok_button
    global Z
    b = b_entry.get()
    k = k_entry.get()

    if b == "" or k == "":
        error_label = Label(root2, text="Данные введены неверно", fg="red")
        error_label.place(x=385, y=480)
    elif not b.isdigit() or not k.isdigit():
        error_label = Label(root2, text="Данные введены неверно", fg="red")
        error_label.place(x=385, y=480)
    elif int(k) not in Z or (int(b) != 0 and int(b) != 1):
        error_label = Label(root2, text="Данные введены неверно", fg="red")
        error_label.place(x=385, y=480)
    else:
        if r == (y**int(b) * g**int(k)) % p:
            error_label = Label(root2, text='Значение  k2  и  b2  подобраны верно    ', fg='green')
            error_label.place(x=385, y=480)
            ok_button.destroy()
            count_d()
        else:
            error_label = Label(root2, text='Значение k2 и b2 подобраны неверно', fg='red')
            error_label.place(x=385, y=480)


def count_d():
    global c
    if ind == 2:
        global print_b
        b = int(print_b.get())
        d = b ^ c
    if ind == 3:
        global b_entry
        b = int(b_entry.get())
        d = b ^ c
    name_result = Label(root2, bg='lightgreen', text='Результат выполнения протокола: ')
    name_result.place(x=0, y=510)
    result_label = Label(root2, fg='red', text=str(d))
    result_label.place(x=250, y=510)

    roles_button = Button(root2, text='Поменять роли', command=go_to_change_roles)
    roles_button.place(x=100, y=570)

    close_button = Button(root2, text='Закрыть', command=go_to_main)
    close_button.place(x=230, y=570)


def go_to_change_roles():
    change_roles(p, g)


def help():
    help_root = Tk()
    help_root.title('Help')
    help_root.geometry('550x600')
    geometry_x = (help_root.winfo_screenwidth() - help_root.winfo_reqwidth()) // 2.5
    geometry_y = (help_root.winfo_screenheight() - help_root.winfo_reqheight()) // 6.5
    help_root.wm_geometry("+%d+%d" % (geometry_x, geometry_y))

    scrollbar = Scrollbar(help_root)

    frame = Canvas(help_root, height='600', width='500', yscrollcommand=scrollbar.set)

    scrollbar.config(command=frame.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    main_frame = Frame(help_root, width=500, height=600)
    frame.pack(side="left", fill="both", expand=True)
    frame.create_window(0, 0, window=main_frame, anchor='nw')



    title_label = Label(main_frame, text='Протокол подбрасывания монеты по телефону', font=24, justify='center')
    title_label.grid(row=1, column=1)

    general_help = Label(main_frame, text='О протоколе:', font=18, justify='left')
    general_help.grid(row=2, column=1, sticky=W)
    general_help = Label(main_frame, text="\nИз всех криптографических протоколов данного типа, пожалуй, наиболее наглядным, \n"
                                       " и к тому же достаточно простым, является протокол подбрасывания монеты.\n\n"
                                       "Предположим, что двум участникам, Алисе и Бобу, необходимо бросить жребий.\n"
                                       "В случае, когда они оба физически находятся в одном и том же месте,\n"
                                       "задачу можно решить с помощью обычной процедуры подбрасывания монеты.\n\n"
                                       "Если же Алиса и Боб удалены друг от друга и могут общаться лишь по каналу связи,\n"
                                       "то задача о жребии, на первый взгляд, кажется неразрешимой. В самом деле, если,\n"
                                       "следуя обычной процедуре подбрасывания монеты, первый ход делает Алиса, которая\n"
                                       "выбирает один из возможных вариантов - ``орел'' или ``решка'', то Боб всегда может о\n"
                                       "бъявить тот исход, который ему выгоден.\n\n"
                                       "Легко понять, что задача о жребии решается очень просто, если существует надежный\n"
                                       "агент - третья сторона, которая пользуется полным доверием и Алисы, и Боба, и\n"
                                       "которая имеет конфиденциальные (закрытые) каналы связи с обоими участниками.\n"
                                       "В этом случае Боб и Алиса выбирают случайные биты b и c соответственно и посылают\n"
                                       "их в тайне друг от друга агенту. Последний ждет, пока не поступят оба бита,\n"
                                       "и после этого публикует b, c и d=b^c - исход подбрасывания монеты.\n\n"
                                       "(^ - знак операции \"ислючающее или\")",
                         justify='left')
    general_help.grid(row=3, column=1, sticky=W)
    general_help = Label(main_frame, text='Разновидности протокола: ', font=18, justify='left')
    general_help.grid(row=4, column=1, sticky=W)
    general_help = Label(main_frame, text='\n1. Протокол Блюма-Микалли;\n'
                                         '2. Протокол подбрасывания монеты \n'
                                         '(на основе проблемы дискретного логарифмирования);\n'
                                         '3.Протокол подбрасывания монеты для получения \n'
                                         'общего случайного бита (на основе проблемы дискретного \n'
                                         'логарифмирования).\n\n'
                                         'В данном программном комплексе рассматривается третий тип протокола', justify='left')
    general_help.grid(row=5, column=1, sticky=W)
    general_help = Label(main_frame, text='Алгоритм работы протокола: ', font=18, justify='left')
    general_help.grid(row=6, column=1, sticky=W)
    general_help = Label(main_frame, text='\nПараметры протокола: p – большое простое число,\n'
                                         ' g - порождающий элемент мультипликативной группы Z\n\n.'
                                         'П1: выбирает случайное x из Z, вычисляет y=(g**x)mod p.\n'
                                         'П1 -> П2: y\n'
                                         'П2: выбирает случайные b={0,1}, k из Z, вычисляет r=((y**b)*(g**k)) mod p\n'
                                         'П2 -> П1: r\n'
                                         'П1 -> П2: случайный c={0,1}\n'
                                         'П2 -> П1: b, k\n'
                                         'П1: проверяет r=((y**b)*(g**k)) mod p. Если результат проверки положительный, \n'
                                         '   то результатом выполнения протокола будет бит d=b^c.',
                         justify='left')
    general_help.grid(row=7, column=1, sticky=W)
    general_help = Label(main_frame, text="Алгоритм построения мультипликативной группы:", font=18, justify='left')
    general_help.grid(row=8, column=1, sticky=W)
    general_help = Label(main_frame, text='1. Выбрать простое число p\n'
                                          '2. Выбрать порождающий элемент мультипликативной группы g, такой что, g**(p-1) mod p = 1\n'
                                          '3. Обозначить диапазон переменной l от 1 до p-1\n'
                                          '4. Найти значение выражения g**l mod p для каждого значения l из выбраного диапазона,\n'
                                          'при этом учитывать, что  g**l mod p != 1 \n'
                                          'Полученные значение и есть элементы мультипликативной группы', justify='left')
    general_help.grid(row=9, column=1, sticky=W)
    general_help = Label(main_frame, text='ПРИМЕЧАНИЕ:', font=18, justify='left')
    general_help.grid(row=10, column=1, sticky=W)
    general_help = Label(main_frame, text='** - знак операции "возведение в степень"\n'
                                          '^ - знак операции "исключающее или"\n'
                                          '!= - знак неравенства', fg='darkgreen', justify='left')
    general_help.grid(row=11, column=1, sticky=W)

    help_root.update()
    frame.config(scrollregion=frame.bbox("all"))

main_page()