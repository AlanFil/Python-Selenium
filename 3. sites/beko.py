import urllib.parse

import requests
from PIL import Image
from scrapy import Selector
from globals import file_path


def beko(raport_lab, product, model):
    html = requests.get(product[6]).content
    sel = Selector(text=html)

    """"""""""""""""" ZDJĘCIA PRODUKTU """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    imgs = sel.xpath('//div[@id="product-main-image"]//a/@href').extract()

    for i in range(len(imgs)):
        res = requests.get(f'https://www.beko.pl{imgs[i]}')
        with open(f'{file_path}/{model}/obrazki_produktu/{i}.jpg', 'wb') as file_format:
            file_format.write(res.content)
        im = Image.open(f'{file_path}/{model}/obrazki_produktu/{i}.jpg')
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
            im.save(f'{file_path}/{model}/obrazki_produktu/{i}.jpg', 'PNG')
        elif file_format == 'JPEG':
            im.save(f'{file_path}/{model}/obrazki_produktu/{i}.jpg', 'JPEG')
        else:
            print(f"Nie umiem zrobić zdjęcia nr {i} :'( (typ {file_format})")

    """"""""""""""""" OPIS TECHNICZNY """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    beko_tech = sel.css('table.table.table-beko ::text').extract()

    # czyszczenie treści opisu technicznego z pustych znaków
    for i in range(len(beko_tech)):
        beko_tech[i] = beko_tech[i].replace('\n', '')
        beko_tech[i] = beko_tech[i].replace('\t', '')
        beko_tech[i] = beko_tech[i].replace('\xa0', '')
        beko_tech[i] = beko_tech[i].replace('\r', '')
        beko_tech[i] = beko_tech[i].replace('  ', '')
        # czyszczenie ekementów, które są samymi spacjami
        if beko_tech[i].isspace():
            beko_tech[i] = beko_tech[i].replace(' ', '')

    # usuwanie psutych elementów
    beko_tech = list(filter(''.__ne__, beko_tech))

    # rozróżnienie wierszy, które są nazwami kategorii (specs_category)
    i = 0
    while i in range(len(beko_tech)):
        if i >= len(beko_tech) - 1:
            break
        if ":" not in beko_tech[i] and ":" not in beko_tech[i + 1]:
            beko_tech.insert(i + 2, '')
            i = i + 2
        i = i + 1
        if i >= len(beko_tech) - 1:
            break

    # usuwanie dwukropków
    for i in range(len(beko_tech)):
        beko_tech[i] = beko_tech[i].replace(':', '')

    # tworzenie gotowych pozycji kodu do wklejenia na stronę MatrixMedia
    i = 0
    opis_techniczny = []
    opis_krotki = []
    while i in range(len(beko_tech)):
        if i >= len(beko_tech) - 1:
            break
        # wykorzystanie rozróżnienia nazwy kategorii do nadania odpowienich znaczników
        if beko_tech[i + 1] == '':
            opis_techniczny.append(
                '<tr class="specs_category"><td colspan="2">' + beko_tech[i] + '</td></tr>')
        # dodawanie znaczników do zwykłych linijek nazwa-wartość
        else:
            opis_techniczny.append(
                '<tr><td class="c_left">' + beko_tech[i] + '</td><td class="c_left">' + beko_tech[i + 1] + '</td></tr>')
            if i in range(23, 43):
                opis_krotki.append(f'<li>{beko_tech[i]}: {beko_tech[i + 1]}</li>')
        i = i + 2
    opis_k = '<ul>' + ''.join(opis_krotki) + '</ul>'

    # dodanie znaczników początkowych i końcowych zgodnych z kodem strony MatrixMedia
    start = '<table id="plan_b" class="data-table"><tbody>'
    end = '</table></tbody>'
    opis_techniczny = [start] + opis_techniczny + [end]

    opis_t = ''.join(opis_techniczny)

    print("==================== Opis Techniczny ====================")
    print(opis_t + '\n\n')

    """"""""""""""""" OPIS GRAFICZNY """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    beko_graph = sel.css('div.row.hero div.col-xs-12 ::text').extract()

    # czyszenie treści opisu graficznego z pustych znaków
    for i in range(len(beko_graph)):
        beko_graph[i] = beko_graph[i].replace('\n', '')
        beko_graph[i] = beko_graph[i].replace('\t', '')
        beko_graph[i] = beko_graph[i].replace('\xa0', '')
        beko_graph[i] = beko_graph[i].replace('  ', '')
        if beko_graph[i].isspace():
            beko_graph[i] = beko_graph[i].replace(' ', '')

    # usuwanie psutych elemenetów
    beko_graph = list(filter(''.__ne__, beko_graph))

    # zdarza się, że jeden z kafelków opisu ma tylko nagłówek. Żeby go też obsłużyć dodałem poniższy warunek
    if len(beko_graph) % 2 != 0:
        for i, ele in enumerate(beko_graph):
            print(f'{i}. {ele}')
        # z jakiegoś powodu po uruchomieniu w konsoli programu następna wczytywana wartość wyrzuca błąd jakby została
        # uzupełniona ciągiem znaków, więc x przyjmuje tę wartość, a dopiero y służy do obsłużenia tej sytuacji
        try:
            x = int(input('\nNajwidoczniej któryś z nagłówków nie ma opisu. Wskaż jego numer, aby program mógł '
                          'kontynuować: '))
        except ValueError:
            x = int(input())
        beko_graph.insert(x + 1, ' ')

    # tworzenie gotowego kodu odpowiedniego dla strony MatrixMedia
    i = 0
    j = 0
    while i in range(len(beko_graph)):
        # dodawanie treści nagłowka
        if i % 2 == 0:
            beko_graph[
                i] = '<div class="two-col-asymmetrically"><div class="right-side"><h2 class="important-header">' + \
                     beko_graph[i] + '</h2>'
        else:
            beko_graph[i] = '<div class="two-col-asymmetrically"><div class="left-side"><h2 class="important-header">' + \
                            beko_graph[i] + '</h2>'
        # dodawanie treści paragrafu
        beko_graph[i + 1] = '<p style="font-size: large;">' + beko_graph[i + 1] + '</p></div>'
        # dodawanie ścieżki do zdjęcia
        beko_graph.insert(i + 2,
                          f'<img alt="" src="https://matrixmedia.pl/media/wysiwyg/Beko/{model}/{j}.jpg"></div>')
        i = i + 3
        j = j + 1

    # uzupełnienie kodu o znaczniki początkowe i końcowe
    graph_desc_beg = '<div class="product-description-section">'
    graph_desc_end = '</div>'
    beko_graph = [graph_desc_beg] + beko_graph + [graph_desc_end]

    # wyświetlenie wyniku
    print("==================== Opis Graficzny ====================")
    opis_g = '\n'.join(beko_graph)
    print(opis_g + '\n\n')

    """"""""""""""""" ZDJĘCIA DO OPISU GRAFICZNEGO """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    imgs = sel.xpath('//div[@class="tab-content"]//img[@class="img-responsive"]//@src').extract()

    # połączenie domyślnie nieobecnego początku kodu oraz przeformatowanie zebranego tekstu na UTF-8
    for i in range(len(imgs)):
        imgs[i] = 'http://beko.pl' + imgs[i]
        imgs[i] = imgs[i].replace('\n', '')
        imgs[i] = imgs[i].replace('\r', '')

    # pobieranie zdjęć z opisu na dysk lokalny
    for i, img in enumerate(imgs):
        res = requests.get(img)
        with open(f'{file_path}/{model}/obrazki_opisu/{i}.jpg', 'wb') as file_format:
            file_format.write(res.content)

    # zmiana rozdzielczości zdjęć tak, aby szerokość wynosiła 480px. Potrzebne jest to, aby zdjęcia na stronie
    # MatrixMedia wyświetlały się prawidłowo w dwóch kolumnach
    for i in range(len(imgs)):
        im = Image.open(f'{file_path}/{model}/obrazki_opisu/{i}.jpg')
        file_format = im.format
        width, height = im.size
        if width > 480:
            ratio = width / 480
            new_width = round(width / ratio)
            new_height = round(height / ratio)
            im = im.resize((new_width, new_height))
            if file_format == 'PNG':
                im.save(f'{file_path}/{model}/obrazki_opisu/{i}.jpg', 'PNG')
            elif file_format == 'JPEG':
                im.save(f'{file_path}/{model}/obrazki_opisu/{i}.jpg', 'JPEG')
            else:
                print(f"Nie umiem zrobić zdjęcia nr {i} :'( (typ {file_format}, jkbc)")
        elif width < 100:
            print(f"Zdjęcie {i}. jest wyjątkowo małe")
        else:
            print(f"Zdjęcie {i}. jest małe")

    return [opis_g, opis_k, opis_t]
