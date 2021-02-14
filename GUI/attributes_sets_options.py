from tkinter import *

import mysql.connector

from globals import std_bg


def attributes_sets_options():
    db = mysql.connector.connect(host="localhost", user="root", database="test")
    cursor = db.cursor()

    cursor.execute("SELECT * FROM attributes_sets")
    db_results = cursor.fetchall()

    results = []
    for i in range(len(db_results)):
        results.append(list(db_results[i]))
        for j in range(len(results[i])):
            if results[i][j] is None:
                results[i][j] = ''

    # Sortowanie wyników dla lepszego odbioru użytkownika
    results = sorted(results, key=lambda x: x[1])

    root = Tk()
    root.title('Automatyzacja opisów')
    root.geometry('570x550')
    root.configure(bg=std_bg)

    # Nie rozumiem tego kodu, ale on dodaje suwak
    main_frame = Frame(root, bg=std_bg)
    main_frame.pack(fill=BOTH, expand=1)
    canvas = Canvas(main_frame, bg=std_bg)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview, bg=std_bg)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set, bg=std_bg)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    view_frame = Frame(canvas, bg=std_bg)
    canvas.create_window((0, 0), window=view_frame, anchor='nw')

    """ NAZWY KOLUMN """

    frame_cols = LabelFrame(view_frame, text="Nazwy kolumn")
    frame_cols.configure(bg=std_bg)
    Label(frame_cols, width=17, bg='#525252', fg='#EEEEEE', justify=LEFT, text="Nazwa").grid(row=0, column=0,
                                                                                             pady=2)
    Label(frame_cols, width=17, bg='#525252', fg='#EEEEEE', justify=LEFT, text="Zestaw1").grid(row=0, column=1,
                                                                                               pady=2)
    Label(frame_cols, width=17, bg='#525252', fg='#EEEEEE', justify=LEFT, text="Waga").grid(row=0, column=2,
                                                                                            pady=2)
    Label(frame_cols, width=17, bg='#525252', fg='#EEEEEE', justify=LEFT, text="Zestaw2").grid(row=0, column=3,
                                                                                               pady=2)
    Label(frame_cols, width=4, bg='#525252', fg='#EEEEEE', justify=LEFT, text="Usuń").grid(row=0, column=4, pady=2)
    frame_cols.grid(row=1, column=0)

    """ DANE Z BAZY DANYCH """

    def change_data():
        changes = []
        for i in range(len(res_label)):
            query_SET = ''
            if res_label[i][0].get() != results[i][1]:
                query_SET += f'Name="{res_label[i][0].get()}", '
            if res_label[i][1].get() != results[i][2]:
                query_SET += f'Set1="{res_label[i][1].get()}", '

            if res_label[i][2].get() == '':
                if results[i][3] == '':
                    pass
                else:
                    query_SET += f'Weight=NULL, '
            else:
                try:
                    weight = int(res_label[i][2].get())
                    if weight != results[i][3]:
                        query_SET += f'Weight={weight}, '
                except ValueError:
                    error['text'] = 'Waga musi być liczbą'
                    return

            if res_label[i][3].get() != results[i][4]:
                query_SET += f'Set2="{res_label[i][3].get()}", '

            if query_SET != '':
                changes.append([results[i][0], query_SET])

        for change in changes:
            cursor.execute(f"""
                        UPDATE attributes_sets 
                        SET {change[1][:-2]}
                        WHERE ID={change[0]}
                    """)
            db.commit()
        root.destroy()
        attributes_sets_options()

    def remove():
        for i in range(len(var)):
            if var[i].get() == 1:
                cursor.execute(f"""
                            DELETE FROM attributes_sets
                            WHERE ID={results[i][0]};
                """)
        db.commit()
        root.destroy()
        attributes_sets_options()

    frame_data = LabelFrame(view_frame, text="Dane")
    frame_data.configure(bg=std_bg)
    res_label = []
    var = []
    for i in range(len(results)):
        var.append(IntVar())
        res_label.append([
            Entry(frame_data, width=20, bg='#525252', fg='#EEEEEE', justify=LEFT),
            Entry(frame_data, width=20, bg='#525252', fg='#EEEEEE', justify=LEFT),
            Entry(frame_data, width=20, bg='#525252', fg='#EEEEEE', justify=LEFT),
            Entry(frame_data, width=20, bg='#525252', fg='#EEEEEE', justify=LEFT),
            Checkbutton(frame_data, width=1, bg=std_bg, variable=var[i], onvalue=1)
        ])

    for i in range(len(res_label)):
        res_label[i][0].insert(0, results[i][1])
        res_label[i][1].insert(0, results[i][2])
        res_label[i][2].insert(0, results[i][3])
        res_label[i][3].insert(0, results[i][4])
        res_label[i][0].grid(row=i, column=0, pady=2)
        res_label[i][1].grid(row=i, column=1, pady=2)
        res_label[i][2].grid(row=i, column=2, pady=2)
        res_label[i][3].grid(row=i, column=3, pady=2)
        res_label[i][4].grid(row=i, column=4, pady=2)

    change_button = Button(frame_data, text="Zmień", width=16, bg='#525252', fg='#EEEEEE', command=change_data)
    change_button.grid(row=len(res_label) + 1, column=3)
    remove_button = Button(frame_data, text="Usuń", width=4, bg='#525252', fg='#EEEEEE', command=remove)
    remove_button.grid(row=len(res_label) + 1, column=4)
    frame_data.grid(row=2, column=0)

    """ DODAWANIE NOWEJ POZYCJI """

    def add_new():
        if not e_name.get():
            error['text'] = 'Nazwa musi być podana'
            return
        elif not e_set1.get():
            error['text'] = 'Pierwszy zestaw musi być podany'
            return
        if e_weight.get() != '':
            try:
                weight = int(e_weight.get())
            except ValueError:
                error['text'] = 'Waga musi być liczbą'
                return
        else:
            weight = "NULL"

        error['text'] = ''
        cursor.execute(f"""
            INSERT INTO attributes_sets (Name, Set1, Weight, Set2)
            VALUES ('{e_name.get()}', '{e_set1.get()}', {weight}, '{e_set2.get()}');
        """)
        db.commit()
        e_name.delete(0, END)
        e_set1.delete(0, END)
        e_weight.delete(0, END)
        e_set2.delete(0, END)
        root.destroy()
        attributes_sets_options()

    frame_new = LabelFrame(view_frame, text="Dodaj nowe")
    frame_new.configure(bg=std_bg)
    e_name = Entry(frame_new, width=20, bg='#525252', fg='#EEEEEE', justify=LEFT)
    e_set1 = Entry(frame_new, width=20, bg='#525252', fg='#EEEEEE', justify=LEFT)
    e_weight = Entry(frame_new, width=20, bg='#525252', fg='#EEEEEE', justify=LEFT)
    e_set2 = Entry(frame_new, width=20, bg='#525252', fg='#EEEEEE', justify=LEFT)
    e_name.grid(row=0, column=0)
    e_set1.grid(row=0, column=1)
    e_weight.grid(row=0, column=2)
    e_set2.grid(row=0, column=3)
    add_button = Button(frame_new, text="Dodaj", width=16, bg='#525252', fg='#EEEEEE', command=add_new)
    add_button.grid(row=1, column=3)
    error = Label(view_frame, text='', bg=std_bg, fg='red')
    frame_new.grid(row=0, column=0, pady=20)
    error.grid(row=3, column=0)

    exit_button = Button(view_frame, text="Wyjdź", width=16, bg='#525252', fg='#EEEEEE', command=root.destroy)
    exit_button.grid(row=5, column=0)
    root.mainloop()
