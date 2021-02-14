import os
import shutil

import mysql.connector

from management.insert_data import insert_data
from management.loggin_in import driver
from sites.amica import amica
from sites.blaupunk import blaupunkt
from sites.bosch import bosch
from sites.electrolux import electrolux
from sites.electrolux_xlsx import electrolux_file
from sites.samsung import samsung
from sites.beko import beko
from sites.samsung_imgs import samsung_imgs
from sites.sony_one import sony_one


def brand_check(name):
    db = mysql.connector.connect(host="localhost", user="root", database="test")
    cursor = db.cursor()

    cursor.execute("SELECT * FROM brands")
    db_results = cursor.fetchall()

    results = []
    for i in range(len(db_results)):
        results.append(list(db_results[i]))
        for j in range(len(results[i])):
            if results[i][j] is None:
                results[i][j] = ''

    br = 'nie wykryto'
    for res in results:
        if res[1].lower() in name.lower():
            br = res[1]

    return br


def product_magic(raport_lab, product, option):
    from globals import file_path

    brand = brand_check(product[1])

    descriptions = None
    model = product[1][product[1].lower().find(brand.lower()) + len(brand) + 1:]
    replaces = (')', '(', ' ', '.', '-', '+', '"')
    polish = ('ą', 'ć', 'ę', 'ł', 'ń', 'ó', 'ś', 'ż', 'ź')
    neutral = ('a', 'c', 'e', 'l', 'n', 'o', 's', 'z', 'z')
    for replace in replaces:
        model = model.replace(replace, '')
    for i in range(len(polish)):
        model = model.replace(polish[i], neutral[i])

    if option == 'full':

        # Jeżeli istniały jakieś dane w tym pliku, to usuń je (dla porządku)
        try:
            shutil.rmtree(file_path)
        except FileNotFoundError:
            pass

        # Utwórz brakujące foldery
        os.mkdir(file_path)
        os.mkdir(f'{file_path}/{model}')
        os.mkdir(f'{file_path}/{model}/obrazki_produktu')
        os.mkdir(f'{file_path}/{model}/obrazki_opisu')

        if brand == 'Amica':
            driver.execute_script('''window.open("about:blank", "_blank");''')
            driver.switch_to.window(driver.window_handles[1])

            descriptions = amica(raport_lab, product, model)

            driver.execute_script("window.close('');")
            driver.switch_to.window(driver.window_handles[0])
        elif brand == 'Blaupunkt':
            descriptions = blaupunkt(model, product[6])
        elif brand == 'Samsung':
            if product[6].startswith('http'):
                # wymagany model i link do opisu technicznego na stronie Samsunga
                descriptions = samsung(model, product[6])
                samsung_imgs(product[6])
        elif brand == 'Beko':
            if product[6].startswith('http'):
                descriptions = beko(raport_lab, product, model)
        elif brand == 'Bosch':
            print('Bosch')
            if product[6].startswith('http'):
                driver.execute_script('''window.open("about:blank", "_blank");''')
                driver.switch_to.window(driver.window_handles[1])

                descriptions = bosch(raport_lab, product[6], model)

                driver.execute_script("window.close('');")
                driver.switch_to.window(driver.window_handles[0])
        elif brand == 'Electrolux' and 'file' in product[6]:
            descriptions = electrolux_file(product, model)
        elif brand == 'Electrolux':
            if product[6].startswith('http'):
                driver.execute_script('''window.open("about:blank", "_blank");''')
                driver.switch_to.window(driver.window_handles[1])

                descriptions = electrolux(raport_lab, product, model)

                driver.execute_script("window.close('');")
                driver.switch_to.window(driver.window_handles[0])
        elif product[6] == "sony_one.xml":
            descriptions = sony_one()

        if descriptions == -1:
            return

    insert_data(raport_lab, product, model, descriptions, brand)
    return
