from time import sleep
from tkinter import *
from selenium.common.exceptions import NoSuchElementException

from management.loggin_in import logging_in, driver

import pyautogui

set_name = ['Hua17', 'Hua18']
date_from = ''
date_to = '2021-02-14'
sorting_order = '1'  # required
eans_in_set = ['6901443375806', '6901443375790']
promo_price = ['124,99', '124,99']


def go():
    for data in data_list:
        driver.implicitly_wait(3)
        driver.find_element_by_xpath('//input[@name="sku"]').clear()
        driver.find_element_by_xpath('//input[@name="sku"]').send_keys(data[0])
        driver.find_element_by_xpath('//button[@title="Szukaj"]').click()
        try:
            x = driver.find_element_by_xpath('//*[@id="messages"]/ul//span').text
        except NoSuchElementException:
            x = ''
        if x == 'Produkt został zapisany.':
            sleep(2)
            pyautogui.click(300, 552)
        else:
            pyautogui.click(300, 502)
        try:
            driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/h3').get_attribute("innerText")
        except NoSuchElementException:
            undone.append(data[0])
            continue

        driver.find_element_by_xpath('//a[@title="Zestawy"]').click()

        for ean in eans_in_set:
            sleep(0.5)
            driver.find_element_by_xpath('//button[@title="Dodaj nowy zestaw"]').click()
            driver.find_element_by_xpath('//div[contains(@id, "bundlediscount_option")][1]//input[@class="input-text"]').send_keys(set_name[eans_in_set.index(ean)])
            driver.find_element_by_xpath('//div[contains(@id, "bundlediscount_option")][1]//input[contains(@class, "validate-date-range")][1]').send_keys(date_from)
            driver.find_element_by_xpath('//div[contains(@id, "bundlediscount_option")][1]//input[contains(@class, "validate-date-range")][2]').send_keys(date_to)
            driver.find_element_by_xpath('//div[contains(@id, "bundlediscount_option")][1]//input[contains(@name, "[sort_order]")]').send_keys(sorting_order)

            driver.find_element_by_xpath('//div[contains(@id, "bundlediscount_option")][1]//select[contains(@name, "[customer_groups]")]/option[1]').click()
            driver.find_element_by_xpath('//div[contains(@id, "bundlediscount_option")][1]//select[contains(@name, "[customer_groups]")]/option[2]').click()
            driver.find_element_by_xpath('//div[contains(@id, "bundlediscount_option")][1]//select[contains(@name, "[customer_groups]")]/option[3]').click()
            driver.find_element_by_xpath('//div[contains(@id, "bundlediscount_option")][1]//select[contains(@name, "[customer_groups]")]/option[4]').click()

            driver.find_element_by_xpath('//div[contains(@id, "bundlediscount_option")][1]//select[contains(@name, "[store_ids]")]/option[1]').click()
            driver.find_element_by_xpath('//div[contains(@id, "bundlediscount_option")][1]//select[contains(@name, "[store_ids]")]//option[contains(text(), "Default Store View")]').click()

            driver.find_element_by_xpath('//div[contains(@id, "bundlediscount_option")][1]//button[@title="Dodaj nowy produkt"]').click()
            driver.find_element_by_xpath('//div[contains(@id, "bundlediscount_option")][1]//input[@name="sku"]').send_keys(ean)
            driver.find_element_by_xpath('//div[contains(@id, "bundlediscount_option")][1]//button[@title="Szukaj"]').click()
            driver.find_element_by_xpath('//div[contains(@id, "bundlediscount_option")][1]//tr[@title="#"]').click()
            driver.find_element_by_xpath('//div[contains(@id, "bundlediscount_option")][1]//button[@title="Dodaj wybrane produkt(y) do opcji"]').click()

            driver.find_element_by_xpath('//div[contains(@id, "bundlediscount_option")][1]//table[@class="border"]//tr[1]//input[contains(@name, "[discount_price]")]').clear()
            driver.find_element_by_xpath('//div[contains(@id, "bundlediscount_option")][1]//table[@class="border"]//tr[1]//input[contains(@name, "[discount_price]")]').send_keys(promo_price[eans_in_set.index(ean)])

        driver.find_element_by_xpath('//button[@title="Zapisz"]').click()
        done.append(data[0])

    print(f'\n\nNiezrobione:')
    print('\n'.join(undone))
    done.clear()
    undone.clear()
    data_list.clear()


done = []
undone = []
data_list = []
if __name__ == '__main__':
    logging_in()

    root = Tk()
    root.title('URLs')
    root.geometry('745x640')
    std_bg = "#B4B4B4"
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


    def add_to_list():
        if insert_product.get(1.0, END) != '':
            product_l = insert_product.get(1.0, END)
            product_l = product_l.split('\n')
            product_l.remove('')
            product_l.remove('')
            for i in range(len(product_l)):
                product_l[i] = product_l[i].split('\t')
            for product in product_l:
                data_list.append(product)
                report_label['text'] += f'Dodaję "{product}"...\n'
                print(product)
        else:
            report_label['text'] += "Uzupełnij najpierw dane produktu\n"
            return
        insert_product.delete(1.0, END)


    """ DODAWANIE PRODUKTÓW """
    frame_product = LabelFrame(view_frame, text='Dodawanie produktu', bg=std_bg)
    Label(frame_product, text="Wprowadź produkty ", bg=std_bg).grid(row=0, column=0)
    insert_product = Text(frame_product, width=75, height=5, bg='#525252', fg='#EEEEEE')
    insert_product.grid(row=0, column=1, columnspan=7)
    add_to_list_button = Button(frame_product, text="Dodaj", width=16, bg='#525252', fg='#EEEEEE', command=add_to_list)
    go_button = Button(frame_product, text="Go!", width=16, bg='#525252', fg='#EEEEEE', command=go)

    add_to_list_button.grid(row=2, column=1, columnspan=2, sticky=W)
    go_button.grid(row=2, column=3, columnspan=3, sticky=E)
    report_label = Label(frame_product, text='', width=100, height=250, justify=LEFT, anchor=NW)
    report_label.grid(row=3, column=0, columnspan=8)
    frame_product.grid(row=1, column=0)

    root.mainloop()