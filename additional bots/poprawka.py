from time import sleep
from tkinter import *

from keyboard import wait
from selenium.common.exceptions import NoSuchElementException, InvalidElementStateException, \
    StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys

from management.loggin_in import logging_in, driver

SEARCH_BY = 'sku'  # szukaj po: sku/name


def instrukcje(data):
    # driver.find_element_by_xpath('//a[@title="Kategorie"]').click()
    #
    # TV = False
    # Audio = False
    # Audio_sub = False
    # # Category
    # for i in range(1, len(driver.find_elements_by_xpath('//div[@id="product-categories"]/ul[1]/div[1]/li[1]/ul[1]/li'))+1):
    #     category = driver.find_element_by_xpath(f'//div[@id="product-categories"]/ul[1]/div[1]/li[1]/ul[1]/li[{i}]').text
    #     category = category[:category.find('(')-1]
    #     if 'TV i akcesoria RTV' == category:
    #         TV = driver.find_element_by_xpath(f'//div[@id="product-categories"]/ul[1]/div[1]/li[1]/ul[1]/li[{i}]//input').is_selected()
    #
    #     if 'Audio' == category:
    #         Audio = driver.find_element_by_xpath(f'//div[@id="product-categories"]/ul[1]/div[1]/li[1]/ul[1]/li[{i}]//input').is_selected()
    #         break
    #
    # # Audio subcategory
    # for i in range(1, len(driver.find_elements_by_xpath('//div[@id="product-categories"]/ul[1]/div[1]/li[1]/ul[1]/li[2]/ul[1]/*')) + 1):
    #     category = driver.find_element_by_xpath(f'//div[@id="product-categories"]/ul[1]/div[1]/li[1]/ul[1]/li[2]/ul[1]/*[{i}]').text
    #     category = category[:category.find('(') - 1]
    #     if 'Kino domowe' == category or 'Głośniki' == category or 'Stereo' == category or 'Słuchawki' == category or 'Audio przenośne' == category:
    #         Audio_sub = driver.find_element_by_xpath(f'//div[@id="product-categories"]/ul[1]/div[1]/li[1]/ul[1]/li[2]/ul[1]/*[{i}]//input').is_selected()
    #         if Audio_sub:
    #             break
    #
    # if not Audio and Audio_sub:
    #     for i in range(1, len(driver.find_elements_by_xpath('//div[@id="product-categories"]/ul[1]/div[1]/li[1]/ul[1]/li')) + 1):
    #         category = driver.find_element_by_xpath(f'//div[@id="product-categories"]/ul[1]/div[1]/li[1]/ul[1]/li[{i}]').text
    #         category = category[:category.find('(') - 1]
    #         if 'Audio' == category:
    #             try:
    #                 driver.find_element_by_xpath(f'//div[@id="product-categories"]/ul[1]/div[1]/li[1]/ul[1]/li[{i}]//input').click()
    #             except ElementClickInterceptedException:
    #                 sleep(3)
    #                 try:
    #                     driver.find_element_by_xpath(f'//div[@id="product-categories"]/ul[1]/div[1]/li[1]/ul[1]/li[{i}]//input').click()
    #                 except ElementClickInterceptedException:
    #                     print('Faliure: ElementClickInterceptedException')
    #                     undone.append(data)
    #             break
    # if TV:
    #     for i in range(1, len(driver.find_elements_by_xpath('//div[@id="product-categories"]/ul[1]/div[1]/li[1]/ul[1]/li')) + 1):
    #         category = driver.find_element_by_xpath(f'//div[@id="product-categories"]/ul[1]/div[1]/li[1]/ul[1]/li[{i}]').text
    #         category = category[:category.find('(') - 1]
    #         if 'TV i akcesoria RTV' == category:
    #             try:
    #                 driver.find_element_by_xpath(f'//div[@id="product-categories"]/ul[1]/div[1]/li[1]/ul[1]/li[{i}]//input').click()
    #             except ElementClickInterceptedException:
    #                 sleep(3)
    #                 try:
    #                     driver.find_element_by_xpath(f'//div[@id="product-categories"]/ul[1]/div[1]/li[1]/ul[1]/li[{i}]//input').click()
    #                 except ElementClickInterceptedException:
    #                     print('Faliure: ElementClickInterceptedException')
    #                     undone.append(data)
    #             break

    # driver.find_element_by_xpath('//select[@id="search_priority"]/option[text()="3"]').click()

    # link = 'https://matrixmedia.pl/' + driver.find_element_by_xpath('//input[@id="url_key"]').get_attribute('value') + '.html'
    # driver.switch_to.window(driver.window_handles[1])
    # driver.get(link)
    # driver.switch_to.window(driver.window_handles[0])

    # driver.find_element_by_xpath('//a[@title="Zestawy"]').click()
    #
    # for j in range(25):
    #     pyautogui.click(1791, 388)

    # name = driver.find_element_by_xpath('//input[@name="product[name]"]').get_attribute('value').replace('Watch 3',
    #                                                                                                      'Watch3')
    # driver.find_element_by_xpath('//input[@name="product[name]"]').clear()
    # driver.find_element_by_xpath('//input[@name="product[name]"]').send_keys(name)

    # driver.find_element_by_xpath('//textarea[@name="product[additional_description]"]').clear()
    # driver.find_element_by_xpath('//textarea[@name="product[additional_description]"]').send_keys('<h2 style="text-align: center; font-size: 17px;"><strong>Kup Galaxy A71, <span style="color: #b41f21;"><br />a Galaxy A21s otrzymasz w prezencie.</span> </strong></h2>')
    # driver.find_element_by_xpath('//input[@name="product[additional_description_to]"]').clear()
    # driver.find_element_by_xpath('//input[@name="product[additional_description_to]"]').send_keys('12.02.2021 16:30')

    # driver.find_element_by_xpath('//input[@name="product[search_keywords]"]').send_keys('etui case do s21')
    #
    # promo = '<p style="text-align: center;"><strong>Kup, <a href="https://my-samsung.com/pl/mysamsung/offers/#/UTUVG9W2FCVXV/" style="color: #b41f21;" target="_blank">wypełnij formularz</a>&nbsp;i odbierz słuchawki&nbsp;<a href="https://matrixmedia.pl/sluchawki-samsung-galaxy-buds-sm-r170n-czarne.html/" style="color: #b41f21;" target="_blank">Galaxy Buds+</a><br />Szczeg&oacute;ły w <a href="https://stg-images.samsung.com/is/content/samsung/p5/pl/regulamin_GW3_bundle.pdf" style="color: #b41f21;" target="_blank">regulaminie</a>.</strong></p>\n'
    #
    short = driver.find_element_by_xpath('//textarea[@name="product[short_description]"]').text
    if short.find('otrzymasz w prezencie!') != -1:
        short = short[short.find('</p>')+4:]
        driver.find_element_by_xpath('//textarea[@name="product[short_description]"]').clear()
        driver.find_element_by_xpath('//textarea[@name="product[short_description]"]').send_keys(
            short
        )

    # driver.find_element_by_xpath('//*').send_keys(Keys.HOME)
    # sleep(1)
    # driver.find_element_by_xpath('//a[@title="Naklejki"]').click()
    # try:
    #     print(
    #         driver.find_element_by_xpath('//input[@name="product[stickers_with_timeout]"]').get_attribute('value'))
    #     print(driver.find_element_by_xpath('//input[@name="product[sticker_time_to]"]').get_attribute('value'))
    #     print('=' * 8)
    #     driver.find_element_by_name('product[stickers_with_timeout]').clear()
    #     driver.find_element_by_name('product[stickers_with_timeout]').send_keys('303')
    #     driver.find_element_by_name('product[sticker_time_to]').clear()
    #     driver.find_element_by_name('product[sticker_time_to]').send_keys('12.02.2021 16:30')
    # except InvalidElementStateException:
    #     pass
    #
    # wait('Enter')

    # short = driver.find_element_by_xpath('//textarea[@name="product[short_description]"]').text
    # if short.find('</strong></p>') != -1:
    #     print(short)
    #     short = short[short.find('</strong></p>') + 13:]
    #     driver.find_element_by_xpath('//textarea[@name="product[short_description]"]').clear()
    #     driver.find_element_by_xpath('//textarea[@name="product[short_description]"]').send_keys(
    #         short
    #     )
    #     driver.find_element_by_xpath('//button[@title="Zapisz"]').click()
    # else:
    #     driver.find_element_by_xpath('//button[@title="Powrót"]').click()
    # wait('Enter')

    # driver.find_element_by_xpath('//*[@id="manufacturer"]/option[text()="Samsung"]').click()  # Zmień producenta

    # driver.find_element_by_xpath('//*[@id="price_negotiation_hide"]/option[text()="Tak"]').click()

    # driver.find_element_by_xpath('//*[@title="Porównywarki cenowe"]').click()
    # driver.find_element_by_xpath('//select[@name="product[export_ceneo]"]/option[2]').click()

    # driver.find_element_by_xpath('//*[@title="Matrix Media"]').click()
    # driver.find_element_by_xpath('//select[@name="product[pricecomparison_short_desc]"]/option[@value="329"]').click()


def go():
    i = 1
    for data in data_list:
        driver.implicitly_wait(8)
        driver.find_element_by_xpath(f'//input[@name="{SEARCH_BY}"]').clear()
        driver.find_element_by_xpath(f'//input[@name="{SEARCH_BY}"]').send_keys(data[0])
        driver.find_element_by_xpath('//button[@title="Szukaj"]').click()

        sleep(1)
        for j in range(1, len(driver.find_elements_by_xpath(f'//table[@id="productGrid_table"]/tbody/tr')) + 1):
            if driver.find_elements_by_xpath(f'//table[@id="productGrid_table"]/tbody/tr')[0].text == 'Nie znaleziono wpisów.':
                undone.append(data[0])
                break
            try:
                if driver.find_element_by_xpath(f'//table[@id="productGrid_table"]/tbody/tr[{j}]/td[7]').text == data[0]\
                        and driver.find_element_by_xpath(f'//table[@id="productGrid_table"]/tbody/tr[{j}]/td[10]').text == 'Katalog, wyszukiwanie':
                    driver.find_element_by_xpath(f'//table[@id="productGrid_table"]/tbody/tr[{j}]').click()
                    break
            except StaleElementReferenceException:
                sleep(1)
                if driver.find_element_by_xpath(f'//table[@id="productGrid_table"]/tbody/tr[{j}]/td[7]').text == data[0] \
                        and driver.find_element_by_xpath(f'//table[@id="productGrid_table"]/tbody/tr[{j}]/td[10]').text == 'Katalog, wyszukiwanie':
                    driver.find_element_by_xpath(f'//table[@id="productGrid_table"]/tbody/tr[{j}]').click()
                    break

        try:
            driver.implicitly_wait(3)
            driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/h3').get_attribute("innerText")
        except NoSuchElementException:
            undone.append(data[0])
            continue

        """ Początek instrukcji """
        print(f"-- {i} -- {data[0]} --")
        i += 1

        instrukcje(data[0])

        """ Koniec instrukcji """
        driver.find_element_by_xpath('//button[@title="Zapisz"]').click()
        try:
            driver.find_element_by_xpath('//button[@title="Dodaj produkt"]')
        except NoSuchElementException:
            driver.find_element_by_xpath('//button[@title="Powrót"]').click()
            undone.append(data[0])

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
    # driver.execute_script('''window.open("about:blank", "_blank");''')

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
