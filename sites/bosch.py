import os
from time import sleep

import cv2
import requests
from PIL import Image
from selenium.common.exceptions import NoSuchElementException

from globals import file_path
from management.ImgRefractor import prod_img
from management.loggin_in import driver


def bosch(report_lab, page_address, model):

    driver.get(page_address)
    sleep(3)  # po wczytaniu strona jest przez krótką chwilę zakryta przez inne okno
    driver.implicitly_wait(3)

    """ OBRAZKI PRODUKTU """
    i = 1
    first = ''
    while True:
        try:
            img = driver.find_element_by_xpath(f'//div[@class="slick-track"]/*[{i}]//picture/img').get_attribute(
                'src').replace('/600x337', '/1200x675')
            print(img)

            if i == 1:
                first = img
            else:
                if first == img:
                    break

            prod_img(f'{file_path}/{model}', img, i+1)

            i += 1
        except NoSuchElementException:
            break

    """OPIS KRÓTKI"""
    try:
        shorts = driver.find_element_by_xpath('//div[contains(@class, "morecontent")]//ul').text.split('\n')
        for i in range(len(shorts)):
            shorts[i] = '<li>' + shorts[i][:shorts[i].find(':')] + '</li>'
        short = '<ul>' + ''.join(shorts) + '</ul>'
    except NoSuchElementException:
        short = ''
        print('NoSuchElementException. Brak opisu krótkiego')

    """OPIS GRAFICZNY"""
    desc = ''
    i = 1
    while True:
        print(f'g_desc: {i}')
        try:
            text = driver.find_element_by_xpath(f'//*[@id="section-highlights"]/*[{i}]').text
            try:
                while True:
                    img = driver.find_element_by_xpath(
                        f'//*[@id="section-highlights"]/*[{i}]//picture//img').get_attribute(
                        "src")
                    driver.find_element_by_xpath(
                        f'//*[@id="section-highlights"]/*[{i}]//picture//img').location_once_scrolled_into_view
                    if i == 2:
                        sleep(2)
                        img = driver.find_element_by_xpath(
                            f'//*[@id="section-highlights"]/*[{i}]//picture//img').get_attribute("src")
                    else:
                        pass

                    if 'Feature_Icons' in img:
                        try:
                            img = driver.find_element_by_xpath(
                                f'//*[@id="section-highlights"]/*[{i}]//div[contains(@class, "mediagallery-slide")][2]//picture//img').get_attribute(
                                "src")
                        except NoSuchElementException:
                            pass
                    replacements = ['/600x337', '/600x']
                    for replacement in replacements:
                        img = img.replace(replacement, '')

                    res = requests.get(img)
                    with open(f'{file_path}/{model}/obrazki_opisu/{i}.jpg', 'wb') as file_format:
                        file_format.write(res.content)

                    im = Image.open(f'{file_path}/{model}/obrazki_opisu/{i}.jpg')
                    width, height = im.size
                    if width > 480:
                        ratio = width / 480
                        new_width = round(width / ratio)
                        new_height = round(height / ratio)
                        im = im.resize((new_width, new_height))
                        try:
                            im.save(f'{file_path}/{model}/obrazki_opisu/{i}.jpg')
                        except OSError:
                            im = im.convert('RGB')
                            im.save(f'{file_path}/{model}/obrazki_opisu/{i}.jpg')
                    break
            except NoSuchElementException:
                pass

            i += 1

            if text == '':
                continue

            replacements = ['Poprzednie', 'Następne', '1/2', '2/2', '1/3', '2/3', '3/3', 'Dowiedz się więcej',
                            '  Powrót',
                            'Dalej']
            for replacement in replacements:
                text = text.replace(replacement, '')

            text = text.split('\n')
            text = [e for e in text if e]

            direction = 'left' if i % 2 == 0 else 'right'  # tekst po lewej/prawej stronie względem zdjęcia
            if len(text) == 1:
                print('jeden')
                desc += f'<div><h1 class="important-header" style="text-align: center;">{text[0]}</h1></div>'
            elif len(text) == 2:
                print('dwa')
                desc += f"""<div class="two-col-asymmetrically"><div class="{direction}-side"><h2 class="important-header">
                            {text[0]}</h2>
                            <p style="font-size: large;">{text[1]}</p></div>
                            <img alt="" src="https://matrixmedia.pl/media/wysiwyg/Bosch/{model}/{i}.jpg" /></div>
                        """
            elif len(text) == 3:
                print('trzy')
                desc += f"""<div class="two-col-asymmetrically"><div class="{direction}-side"><h2 class="important-header">
                        {text[0]}</h2>
                        <p style="font-size: large;">{text[1]}
                        <br/><br/>
                        <small>{text[2]}</small></p></div>
                        <img alt="" src="https://matrixmedia.pl/media/wysiwyg/Bosch/{model}/{i}.jpg" /></div>
                    """
            else:
                print(f'\n------\n{text}\n------\n')

        except NoSuchElementException:
            break
    desc = '<div class="product-description-section">' + desc + '</div>'

    """OPIS TECHNICZNY"""
    driver.get(page_address + '#/Tabs=section-technicalspecs/')
    driver.find_element_by_xpath('//div[@id="tech-data"]//span[contains(text(), "Specyfikacja techniczna")]').click()

    # znajdź który div zawiera informacje techniczne
    i = 1
    while True:
        if 'specyfikacja techniczna' in driver.find_element_by_xpath(f'//div[@id="tech-data"]/*[{i}]').text.lower():
            break
        else:
            i += 1

    # zbierz dane techniczne
    j = 1
    tech = []
    driver.implicitly_wait(0.5)
    while True:
        try:
            driver.find_element_by_xpath(f'//div[@id="tech-data"]/*[{i}]/section/div[{j}]/a').click()
            sleep(0.5)
            category_name = driver.find_element_by_xpath(f'//div[@id="tech-data"]/*[{i}]/section/div[{j}]/a').text
            tech.append(f'<tr class="specs_category"><td colspan="2">{category_name}</td></tr>')
        except NoSuchElementException:
            break

        k = 1
        while True:
            try:
                name = driver.find_element_by_xpath(f'//div[@id="tech-data"]/*[{i}]/section/div[{j}]//tr[{k}]/th').text
                value = driver.find_element_by_xpath(f'//div[@id="tech-data"]/*[{i}]/section/div[{j}]//tr[{k}]/td').text
                if value == '':
                    icon = driver.find_element_by_xpath(
                        f'//div[@id="tech-data"]/*[{i}]/section/div[{j}]//tr[{k}]/td').get_attribute('class')
                    value = 'Tak' if icon.lower() == 'checked' else 'Nie'
                tech.append(f'<tr><td class="c_left">{name}</td><td class="c_left">{value}</td></tr>')
                k += 1
            except NoSuchElementException:
                break
        j += 1

    tech = ['<table id="plan_b" class="data-table"><tbody>'] + tech + ['</tbody></table>']
    tech = ''.join(tech)

    return [desc, short, tech]
