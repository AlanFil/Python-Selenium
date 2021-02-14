"""
This code sends user to logging_in() module to login py_bot to Magento system.
It displays basic GUI in tkinter where you can paste product's data and let
Python do it's magic in scraping and inserting data.
"""

from tkinter import *

from management.loggin_in import logging_in
from management.product_magic import product_magic

from GUI.attributes_sets_options import attributes_sets_options
from GUI.brands_options import brands_options

from globals import report_label, std_bg

product_list = []


def desc(option):
    print(product_list)
    for product in product_list:
        product_magic(report_label, product, option)
    product_list.clear()


if __name__ == '__main__':
    logging_in()
    global report_label

    root = Tk()
    root.title('Automatyzacja opisów')
    root.geometry('745x640')
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

    """ MENU """
    frame_menu = LabelFrame(view_frame, text='Menu', bg=std_bg)
    attr_button = Button(frame_menu, text="Zestawy atrybutów", width=16, bg='#525252', fg='#EEEEEE',
                         command=attributes_sets_options)
    attr_button.grid(row=0, column=0)
    brand_button = Button(frame_menu, text="Marki", width=16, bg='#525252', fg='#EEEEEE',
                          command=brands_options)
    brand_button.grid(row=0, column=1)
    frame_menu.grid(row=0, column=0)


    def add_to_list():
        if insert_product.get(1.0, END) != '':
            product_l = insert_product.get(1.0, END)
            product_l = product_l.split('\n')
            product_l.remove('')
            for product in product_l:
                product = product.split('\t')

                if len(product) == 6:
                    product.append('')
                # if len(product) != 7:
                #     report_label['text'] += f'Niewystraczająca liczba elementów (powinno być 6 lub 7)\n'
                #     return
                product_list.append(product)
                report_label['text'] += f'Dodaję "{product[1]}"...\n'

        elif insert_product_1.get() != '':
            product = [insert_product_1.get(), insert_product_2.get(), insert_product_3.get(), insert_product_4.get(),
                       insert_product_5.get(), insert_product_6.get(), insert_product_7.get()]
            insert_product_1.delete(0, END)
            insert_product_2.delete(0, END)
            insert_product_3.delete(0, END)
            insert_product_4.delete(0, END)
            insert_product_5.delete(0, END)
            insert_product_6.delete(0, END)
            insert_product_7.delete(0, END)
            product_list.append(product)
        else:
            report_label['text'] += "Uzupełnij najpierw dane produktu\n"
            return

        insert_product.delete(1.0, END)


    """ DODAWANIE PRODUKTÓW """
    frame_product = LabelFrame(view_frame, text='Dodawanie produktu', bg=std_bg)
    Label(frame_product, text="Wprowadź produkty ", bg=std_bg).grid(row=0, column=0)
    Label(frame_product, text="Wprowadź ręcznie ", bg=std_bg).grid(row=1, column=0)
    insert_product = Text(frame_product, width=75, height=5, bg='#525252', fg='#EEEEEE')
    insert_product.grid(row=0, column=1, columnspan=7)
    insert_product_1 = Entry(frame_product, width=10, bg='#525252', fg='#EEEEEE', justify=LEFT)
    insert_product_1.grid(row=1, column=1)
    insert_product_2 = Entry(frame_product, width=34, bg='#525252', fg='#EEEEEE', justify=LEFT)
    insert_product_2.grid(row=1, column=2)
    insert_product_3 = Entry(frame_product, width=13, bg='#525252', fg='#EEEEEE', justify=LEFT)
    insert_product_3.grid(row=1, column=3)
    insert_product_4 = Entry(frame_product, width=7, bg='#525252', fg='#EEEEEE', justify=LEFT)
    insert_product_4.grid(row=1, column=4)
    insert_product_5 = Entry(frame_product, width=10, bg='#525252', fg='#EEEEEE', justify=LEFT)
    insert_product_5.grid(row=1, column=5)
    insert_product_6 = Entry(frame_product, width=12, bg='#525252', fg='#EEEEEE', justify=LEFT)
    insert_product_6.grid(row=1, column=6)
    insert_product_7 = Entry(frame_product, width=10, bg='#525252', fg='#EEEEEE', justify=LEFT)
    insert_product_7.grid(row=1, column=7)
    add_to_list_button = Button(frame_product, text="Dodaj", width=16, bg='#525252', fg='#EEEEEE',
                                command=add_to_list)
    clean_list = Button(frame_product, text="Wyczyść", width=16, bg='#525252', fg='#EEEEEE',
                        command=lambda: product_list.clear())
    enter_product = Button(frame_product, text="Tylko dane", width=16, bg='#525252', fg='#EEEEEE',
                           command=lambda: desc('enter'))
    full_desc = Button(frame_product, text="Cały opis", width=16, bg='#525252', fg='#EEEEEE',
                       command=lambda: desc('full'))
    clean_list.grid(row=2, column=0, columnspan=1, sticky=W)
    add_to_list_button.grid(row=2, column=1, columnspan=2, sticky=W)
    enter_product.grid(row=2, column=3, columnspan=3, sticky=E)
    full_desc.grid(row=2, column=6, columnspan=2, sticky=E, padx=2)
    report_label = Label(frame_product, text='', width=100, height=250, justify=LEFT, anchor=NW)
    report_label.grid(row=3, column=0, columnspan=8)
    frame_product.grid(row=1, column=0)

    root.mainloop()
