"""
Funkcja desc_img:
- sprawdza czy ścieżka prowadzi do zdjęcia,
- weryfikuje rozszerzenie pliku. Jeżeli jest różne niż .jpg i .png, to wyświetla komunikat i próbuje zapisać plik w .jpg
- pobiera plik i dobiera szerokość do normy MatrixMedia (480 lub 1180px)
- zapisuje zdjęcie pod wskazaną ścieżką
"""

import requests
from PIL import Image
from requests.exceptions import InvalidURL


def desc_img(file_path, img, name, border=800, crop=False, force_small=False):
    try:
        res = requests.get(img)
    except InvalidURL:
        print(f'{img} - nie udało się pobrać zdjęcia z tego linku')

    # zweryfikuj typ pliku
    if 'jpg' in img[-5:].lower():
        file_type = 'jpg'
    elif 'png' in img[-5:].lower():
        file_type = 'png'
    else:
        print('Rozszerzenie różne niż .jpg i .png. Przypisuję .jpg')
        print(img)
        file_type = 'jpg'

    # pobierz zdjęcie
    with open(f'{file_path}/obrazki_opisu/{name}.{file_type}', 'wb') as file_format:
        file_format.write(res.content)
    im = Image.open(f'{file_path}/obrazki_opisu/{name}.{file_type}')

    # przytnij pustą przestrzeń
    if crop:
        im = im.crop(im.getbbox())

    # przeskalowanie do zdjęcia na pół ekranu lub cały
    width, height = im.size
    size = 'full'
    ratio = 1
    if width < border or force_small:
        ratio = width / 480
        size = 'half'
    elif width > 1180:
        ratio = width / 1180

    if ratio != 1:
        new_width = round(width / ratio)
        new_height = round(height / ratio)
        im = im.resize((new_width, new_height))

    # zapisz plik
    im.save(f'{file_path}/obrazki_opisu/{name}.{file_type}')

    return size, file_type


def prod_img(file_path, img, name, crop=False):
    res = requests.get(img)

    # zweryfikuj typ pliku
    if 'jpg' in img[-5:].lower():
        file_type = 'jpg'
    elif 'png' in img[-5:].lower():
        file_type = 'png'
    else:
        print('Rozszerzenie różne niż .jpg i .png. Przypisuję .jpg')
        print(img)
        file_type = 'jpg'

    # pobierz zdjęcie
    with open(f'{file_path}/obrazki_produktu/{name}.{file_type}', 'wb') as file_format:
        file_format.write(res.content)
    im = Image.open(f'{file_path}/obrazki_produktu/{name}.{file_type}')

    # przytnij pustą przestrzeń
    if crop:
        im = im.crop(im.getbbox())

    # przeskalowanie do zdjęcia do rozmiarów na MatrixMedia
    width, height = im.size
    if width > 600:
        ratio = width / 600
        new_width = round(width / ratio)
        new_height = round(height / ratio)
        im = im.resize((new_width, new_height))

    # zapisz plik
    try:
        im.save(f'{file_path}/obrazki_produktu/{name}.{file_type}')
    except OSError:
        print(f'OSError. Nie udało się zapisać zdjęcia: {img}')

    return
