from time import sleep

import requests
from PIL import Image
from scrapy import Selector
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys

from management.loggin_in import driver


def amica(report_label, product, model):
    from globals import file_path

    if product[7].startswith('http'):
        page_address = product[7]
        driver.get(product[7])
        html = requests.get(product[7]).content
        sel = Selector(text=html)
    else:
        search = product[1][product[1].lower().find('amica') + len('amica') + 1:]
        amica_link = f'https://www.amica.pl/szukaj/{search}'
        driver.get(amica_link)
        html = requests.get(amica_link).content
        sel = Selector(text=html)

        # Znajdź model na stronie Amica
        try:
            for i in range(len(sel.xpath('//div[@class="container"]'))):
                if driver.find_element_by_xpath(f'//h3[@class="prodSymbol"][{i + 1}]').text == model:
                    page_address = driver.find_element_by_xpath(f'//h3[@class="prodSymbol"][{i + 1}]/a').get_attribute(
                        'href')
                    break

        except NoSuchElementException:
            report_label['text'] += f"Nie znaleziono {model} na stronie Amica. Pomijam go."
            return -1

        driver.find_element_by_css_selector(
            '#produkty > div.moreProducts > div > div > div > div > div > div > div.image > a').click()
    sleep(1)
    driver.find_element_by_css_selector('#menu01 > div > div.product-view__media > img').click()

    first = driver.find_element_by_css_selector(
        '#prod_app > div.medialightbox__overlay > div > div.cool-lightbox__inner > div.cool-lightbox__wrapper > '
        'div > div > img').get_attribute('src')

    # Zapisywanie i obrabianie zdjęc do miniaturek
    i = 0
    while i < 15:
        if i == 0:
            res = requests.get(first)
        else:
            desc_img = driver.find_element_by_css_selector(
                '#prod_app > div.medialightbox__overlay > div > div.cool-lightbox__inner > div.cool-lightbox__wrapper '
                '> div > div > img').get_attribute('src')
            if desc_img == first:
                break
            res = requests.get(desc_img)
        with open(f'{file_path}/{model}/obrazki_produktu/{i}.jpg', 'wb') as file_format:
            file_format.write(res.content)
        try:
            driver.find_element_by_xpath('//*[@id="prod_app"]/div[4]/div/div[2]/div[2]/button[2]/div').click()
        except ElementNotInteractableException:
            pass

        sleep(1)
        i = i + 1

    for y in range(i):
        im = Image.open(f'{file_path}/{model}/obrazki_produktu/{y}.jpg')
        file_format = im.format
        width, height = im.size
        if width > height:
            ratio = width / 600
        else:
            ratio = height / 600
        new_width = round(width / ratio)
        new_height = round(height / ratio)
        im = im.resize((new_width, new_height))
        if file_format == 'PNG':
            im.save(f'{file_path}/{model}/obrazki_produktu/{y}.jpg', 'PNG')
        elif file_format == 'JPEG':
            im.save(f'{file_path}/{model}/obrazki_produktu/{y}.jpg', 'JPEG')
        else:
            print(f"Nie umiem zrobić zdjęcia nr {y} :'( (typ {file_format})")
    driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)

    html = requests.get(page_address).content
    sel = Selector(text=html)

    raw = sel.xpath('/html/body/div[1]/script[4]/text()').extract()

    for i in range(len(raw)):
        raw[i] = raw[i].replace('\n', '')
        raw[i] = raw[i].replace('\t', '')
        raw[i] = raw[i].replace('\xa0', '')
        raw[i] = raw[i].replace('\r', '')
        raw[i] = raw[i].replace('  ', '')

    t = raw[0]
    t = t[t.find('"descTitle":'):]
    t = t[:t.find('}]}')]
    desc = []
    imgs = []
    while t.find('"descTitle":') != -1:
        t = t[t.find('"descTitle":') + 13:]
        desc.append(t[:t.find('"')])
        t = t[t.find('"descIconUrl":') + 15:]
        imgs.append(t[:t.find('"')])
        t = t[t.find('"descText":') + 12:]
        desc.append(t[:t.find('"')])

    for i in range(len(imgs)):
        imgs[i] = imgs[i].replace('\\', '')

    # pobieranie zdjęć z opisu na dysk lokalny
    for i, img in enumerate(imgs):
        res = requests.get(img)
        with open(f'{file_path}/{model}/obrazki_opisu/{i}.jpg', 'wb') as file_format:
            file_format.write(res.content)

    for i in range(len(desc)):
        desc[i] = desc[i].replace('\\u0105', 'ą')
        desc[i] = desc[i].replace('\\u0119', 'ę')
        desc[i] = desc[i].replace('\\u0107', 'ć')
        desc[i] = desc[i].replace('\\u0144', 'ń')
        desc[i] = desc[i].replace('\\u015b', 'ś')
        desc[i] = desc[i].replace('\\u015a', 'Ś')
        desc[i] = desc[i].replace('\\u00f3', 'ó')
        desc[i] = desc[i].replace('\\u0141', 'Ł')
        desc[i] = desc[i].replace('\\u0142', 'ł')
        desc[i] = desc[i].replace('\\u017a', 'ź')
        desc[i] = desc[i].replace('\\u017b', 'Ż')
        desc[i] = desc[i].replace('\\u017c', 'ż')
        desc[i] = desc[i].replace('\\u017', 'Ź')
        desc[i] = desc[i].replace('\\u00ae', '®')
        desc[i] = desc[i].replace('\\u00b0', '°')
        desc[i] = desc[i].replace('\u00b0', '°')
        desc[i] = desc[i].replace('\u2070', '°')
        desc[i] = desc[i].replace('\\u2070', '°')
        desc[i] = desc[i].replace('\\u2013', '-')
        desc[i] = desc[i].replace('\u2013', '-')
        desc[i] = desc[i].replace('\\u2026', '...')
        desc[i] = desc[i].replace('\u2026', '...')
        desc[i] = desc[i].replace('\\n', '')
        desc[i] = desc[i].replace('\\/', '/')

    j = 0
    fin = ['<div class="product-description-section">']
    for i in range(0, len(desc), 6):
        fin.append('<div class="three-col-equaly">')
        try:
            fin.append(f'<div><img src="https://matrixmedia.pl/media/wysiwyg/Amica/'
                       f'{model}/{j}.jpg"/><br/><h2 class="important-header">{desc[i]}</h2>')
            fin.append(f'<p style="font-size: large;">{desc[i + 1]}</p></div>')
            fin.append(f'<div><img src="https://matrixmedia.pl/media/wysiwyg/Amica/'
                       f'{model}/{j + 1}.jpg"/><br/><h2 class="important-header"> {desc[i + 2]}</h2>')
            fin.append(f'<p style="font-size: large;">{desc[i + 3]}</p></div>')
            fin.append(f'<div><img src="https://matrixmedia.pl/media/wysiwyg/Amica/'
                       f'{model}/{j + 2}.jpg"/><br/><h2 class="important-header"> {desc[i + 4]}</h2>')
            fin.append(f'<p style="font-size: large;">{desc[i + 5]}</p></div>')
        except IndexError:
            pass
        finally:
            fin.append('</div>')
        j = j + 3
    fin.append('</div>')

    reg = ''.join(fin)
    reg = reg.replace('*Zdjęcie ma charakter poglądowy i może nie przedstawiać dokładnego modelu produktu.', '')
    print("------------ OPIS GRAFICZNY ------------")
    print(reg + '\n\n')

    """ OPIS TECHNICZNY """
    html = requests.get(page_address).content
    sel = Selector(text=html)

    tech_raw = sel.xpath('/html/body/div[1]/script[4]/text()').extract()
    tech_raw2 = tech_raw[0]
    tech_d = tech_raw2[tech_raw2.find('"attrGroupData"'):tech_raw2.find('"docFilesDataList"')]

    tech_desc_1 = []
    while tech_d.find('"attrName":') != -1:
        tech_d = tech_d[tech_d.find('"attrName":') + 12:]
        tech_desc_1.append(tech_d[:tech_d.find('"')])
        tech_d = tech_d[tech_d.find('"attrValue":') + 13:]
        tech_desc_1.append(tech_d[:tech_d.find('"')])

    tech_d2 = tech_d[tech_d.find(tech_desc_1[-1]):]

    tech_desc_2 = []
    while tech_d2.find('"attrValue":') != -1:
        tech_d2 = tech_d2[tech_d2.find('"attrValue":') + 13:]
        tech_desc_2.append(tech_d2[:tech_d2.find('"')])

    tech_desc = ['<table id="plan_b" class="data-table"><tbody><tr class="specs_category"><td '
                 'colspan="2">Specyfikacja</td></tr>']
    for i in range(0, len(tech_desc_1), 2):
        tech_desc.append(f'<tr><td class="c_left">{tech_desc_1[i]}</td>')
        tech_desc.append(f'<td class="c_left">{tech_desc_1[i + 1]}</td></tr>')

    for i in range(len(tech_desc_2)):
        if i == 0:
            tech_desc.append(f'<tr><td class="c_left">Funkcje</td>')
            tech_desc.append(f'<td class="c_left">{tech_desc_2[i]}</td></tr>')
        else:
            tech_desc.append(f'<tr><td class="c_left"></td>')
            tech_desc.append(f'<td class="c_left">{tech_desc_2[i]}</td></tr>')
    tech_desc.append('</tbody></table>')

    for i in range(len(tech_desc)):
        tech_desc[i] = tech_desc[i].replace('\\u0105', 'ą')
        tech_desc[i] = tech_desc[i].replace('\\u0119', 'ę')
        tech_desc[i] = tech_desc[i].replace('\\u0107', 'ć')
        tech_desc[i] = tech_desc[i].replace('\\u0144', 'ń')
        tech_desc[i] = tech_desc[i].replace('\\u015b', 'ś')
        tech_desc[i] = tech_desc[i].replace('\\u015a', 'Ś')
        tech_desc[i] = tech_desc[i].replace('\\u00f3', 'ó')
        tech_desc[i] = tech_desc[i].replace('\\u0141', 'Ł')
        tech_desc[i] = tech_desc[i].replace('\\u0142', 'ł')
        tech_desc[i] = tech_desc[i].replace('\\u017a', 'ź')
        tech_desc[i] = tech_desc[i].replace('\\u017b', 'Ż')
        tech_desc[i] = tech_desc[i].replace('\\u017c', 'ż')
        tech_desc[i] = tech_desc[i].replace('\\u017', 'Ź')
        tech_desc[i] = tech_desc[i].replace('\\u00ae', '®')
        tech_desc[i] = tech_desc[i].replace('\\u00b0', '°')
        tech_desc[i] = tech_desc[i].replace('\u00b0', '°')
        tech_desc[i] = tech_desc[i].replace('\u2070', '°')
        tech_desc[i] = tech_desc[i].replace('\\u2070', '°')
        tech_desc[i] = tech_desc[i].replace('\\u2013', '-')
        tech_desc[i] = tech_desc[i].replace('\u2013', '-')
        tech_desc[i] = tech_desc[i].replace('\\u2026', '...')
        tech_desc[i] = tech_desc[i].replace('\u2026', '...')
        tech_desc[i] = tech_desc[i].replace('\\n', '')
        tech_desc[i] = tech_desc[i].replace('\\/', '/')
        tech_desc[i] = tech_desc[i].replace(':', '')

    tech = ''.join(tech_desc)
    print('------------ OPIS TECHNICZNY ------------')
    print(tech + '\n\n')

    """ OPIS KRÓTKI """
    for i in range(len(tech_desc_1)):
        tech_desc_1[i] = tech_desc_1[i].replace('\\u0105', 'ą')
        tech_desc_1[i] = tech_desc_1[i].replace('\\u0119', 'ę')
        tech_desc_1[i] = tech_desc_1[i].replace('\\u0107', 'ć')
        tech_desc_1[i] = tech_desc_1[i].replace('\\u0144', 'ń')
        tech_desc_1[i] = tech_desc_1[i].replace('\\u015b', 'ś')
        tech_desc_1[i] = tech_desc_1[i].replace('\\u015a', 'Ś')
        tech_desc_1[i] = tech_desc_1[i].replace('\\u00f3', 'ó')
        tech_desc_1[i] = tech_desc_1[i].replace('\\u0141', 'Ł')
        tech_desc_1[i] = tech_desc_1[i].replace('\\u0142', 'ł')
        tech_desc_1[i] = tech_desc_1[i].replace('\\u017a', 'ź')
        tech_desc_1[i] = tech_desc_1[i].replace('\\u017b', 'Ż')
        tech_desc_1[i] = tech_desc_1[i].replace('\\u017c', 'ż')
        tech_desc_1[i] = tech_desc_1[i].replace('\\u017', 'Ź')
        tech_desc_1[i] = tech_desc_1[i].replace('\\u00ae', '®')
        tech_desc_1[i] = tech_desc_1[i].replace('\\u00b0', '°')
        tech_desc_1[i] = tech_desc_1[i].replace('\u00b0', '°')
        tech_desc_1[i] = tech_desc_1[i].replace('\u2070', '°')
        tech_desc_1[i] = tech_desc_1[i].replace('\\u2070', '°')
        tech_desc_1[i] = tech_desc_1[i].replace('\\u2013', '-')
        tech_desc_1[i] = tech_desc_1[i].replace('\u2013', '-')
        tech_desc_1[i] = tech_desc_1[i].replace('\\u2026', '...')
        tech_desc_1[i] = tech_desc_1[i].replace('\u2026', '...')
        tech_desc_1[i] = tech_desc_1[i].replace('\\n', '')
        tech_desc_1[i] = tech_desc_1[i].replace('\\/', '/')
        tech_desc_1[i] = tech_desc_1[i].replace(':', '')

    if len(tech_desc_1) < 12:
        n = len(tech_desc_1)
    else:
        n = 12

    short = ['<ul>']
    for i in range(0, n, 2):
        short.append(f'<li>{tech_desc_1[i]}: {tech_desc_1[i + 1]}</li>')
    short.append('</ul>')

    short = '\n'.join(short)
    print('------------ OPIS KRÓTKI ------------')
    print(short + '\n\n')

    return [reg, short, tech]
