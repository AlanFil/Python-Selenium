from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

from management.loggin_in import driver


def attributes(tech_desc, brand):
    tech_desc = tech_desc.lower()
    tech_desc = tech_desc.replace('<table id="plan_b" class="data-table"><tbody><tr class="specs_category"><td '
                                  'colspan="2">specyfikacja</td></tr><tr><td class="c_left">', '')
    tech_desc = tech_desc.replace('</td><td class="c_left">', ':')
    tech_desc = tech_desc.replace('</td></tr><tr><td class="c_left">', '\n')
    tech_desc = tech_desc.replace('</td></tr></tbody></table>', '')

    try:
        driver.find_element_by_xpath(f'//*[@id="marka"]/option[text()="{brand}"]').click()
    except NoSuchElementException:
        pass
    except ElementNotInteractableException:
        pass

    wysokosc = tech_desc[tech_desc.find('wysokość') + 9:]
    wysokosc = wysokosc[:wysokosc.find('\n')]
    wysokosc = wysokosc.replace(' ', '')
    wysokosc = wysokosc.replace('cm', '')
    wysokosc = wysokosc.replace(',', '.')
    try:
        wysokosc = float(wysokosc)
        if wysokosc < 84.9:
            driver.find_element_by_xpath(f'//*[@id="wysokosc"]/option[text()="do 84,9 cm"]').click()
        elif 84.9 < wysokosc < 99.9:
            driver.find_element_by_xpath(f'//*[@id="wysokosc"]/option[text()="od 85 do 99,9 cm"]').click()
        elif 100.0 < wysokosc < 129.9:
            driver.find_element_by_xpath(f'//*[@id="wysokosc"]/option[text()="od 100 do 129,9 cm"]').click()
        elif 130.0 < wysokosc < 159.9:
            driver.find_element_by_xpath(f'//*[@id="wysokosc"]/option[text()="od 130 do 159,9 cm"]').click()
        elif 160.0 < wysokosc < 179.9:
            driver.find_element_by_xpath(f'//*[@id="wysokosc"]/option[text()="od 170 do 179,9 cm"]').click()
        elif wysokosc > 180.0:
            driver.find_element_by_xpath(f'//*[@id="wysokosc"]/option[text()="od 180 cm"]').click()
    except NoSuchElementException:
        pass
    except ValueError:
        pass
    except ElementNotInteractableException:
        pass

    szerokosc = tech_desc[tech_desc.find('szerokość') + 10:]
    szerokosc = szerokosc[:szerokosc.find('\n')]
    szerokosc = szerokosc.replace(' ', '')
    szerokosc = szerokosc.replace('cm', '')
    szerokosc = szerokosc.replace(',', '.')
    try:
        szerokosc = float(szerokosc)
        if szerokosc < 39.9:
            driver.find_element_by_xpath(f'//*[@id="szerokosc"]/option[text()="do 39,9 cm"]').click()
        elif 40.0 < szerokosc < 50.9:
            driver.find_element_by_xpath(f'//*[@id="szerokosc"]/option[text()="od 40 do 50 cm"]').click()
        elif 51.0 < szerokosc < 60.9:
            driver.find_element_by_xpath(f'//*[@id="szerokosc"]/option[text()="od 51 do 60 cm"]').click()
        elif 61.0 < szerokosc < 79.9:
            driver.find_element_by_xpath(f'//*[@id="szerokosc"]/option[text()="od 60 do 79,9 cm"]').click()
        elif szerokosc > 80.0:
            driver.find_element_by_xpath(f'//*[@id="szerokosc"]/option[text()="od 80 cm"]').click()
    except ValueError:
        pass
    except NoSuchElementException:
        pass
    except ElementNotInteractableException:
        pass

    glebokosc = tech_desc[tech_desc.find('głębokość') + 10:]
    glebokosc = glebokosc[:glebokosc.find('\n')]
    glebokosc = glebokosc.replace(' ', '')
    glebokosc = glebokosc.replace('cm', '')
    glebokosc = glebokosc.replace(',', '.')
    try:
        glebokosc = float(glebokosc)
        if glebokosc < 35.9:
            driver.find_element_by_xpath('//*[@id="glebokosc"]/option[text()="od 31 do 35 cm"]').click()
        elif 36.0 < glebokosc < 39.9:
            driver.find_element_by_xpath('//*[@id="glebokosc"]/option[text()="od 36 do 40 cm"]').click()
        elif 40.0 < glebokosc < 44.9:
            driver.find_element_by_xpath('//*[@id="glebokosc"]/option[text()="40 do 44,9 cm"]').click()
        elif 45.0 < glebokosc < 49.9:
            driver.find_element_by_xpath('//*[@id="glebokosc"]/option[text()="od 45 do 49,9 cm"]').click()
        elif 50.0 < glebokosc < 54.9:
            driver.find_element_by_xpath('//*[@id="glebokosc"]/option[text()="od 50 do 54,9 cm"]').click()
        elif 55.0 < glebokosc < 59.9:
            driver.find_element_by_xpath('//*[@id="glebokosc"]/option[text()="od 55 do 59,9 cm"]').click()
        elif 60.0 < glebokosc < 64.9:
            driver.find_element_by_xpath('//*[@id="glebokosc"]/option[text()="od 60 do 65 cm"]').click()
        elif glebokosc < 65.0:
            driver.find_element_by_xpath('//*[@id="glebokosc"]/option[text()="od 65 cm"]').click()
    except ValueError:
        pass
    except NoSuchElementException:
        pass
    except ElementNotInteractableException:
        pass

    kolor = tech_desc[tech_desc.find('kolor') + 6:]
    kolor = kolor[:kolor.find('\n')]
    kolor = kolor.replace(' ', '')
    try:
        driver.find_element_by_xpath(f'//*[@id="dominujacy_odcien"]/option[text()="{kolor}"]').click()
    except NoSuchElementException:
        pass
    except ElementNotInteractableException:
        pass

    try:
        sterowanie = tech_desc[tech_desc.find('sterowanie') + 11:]
        sterowanie = sterowanie[:sterowanie.find('\n')]
        sterowanie = sterowanie.replace(' ', '')
        if 'mechan' in sterowanie:
            driver.find_element_by_xpath('//*[@id="sterowanie"]/option[text()="mechaniczne"]').click()
        else:
            driver.find_element_by_xpath(f'//*[@id="sterowanie"]/option[text()="{sterowanie}"]').click()
    except NoSuchElementException:
        pass
    except ElementNotInteractableException:
        pass

    halas = tech_desc[tech_desc.find('poziom hałasu') + 14:]
    halas = halas[:halas.find('\n')]
    halas = halas.replace(' ', '')
    halas = halas.replace('db', '')
    halas = halas.replace(',', '.')
    try:
        halas = float(halas)
        if halas < 36:
            driver.find_element_by_xpath('//*[@id="poziom_halasu"]/option[text()="do 36 dB"]').click()
        elif 36 <= halas <= 38:
            driver.find_element_by_xpath('//*[@id="poziom_halasu"]/option[text()="od 37 do 38 dB"]').click()
        elif 39 <= halas <= 40:
            driver.find_element_by_xpath('//*[@id="poziom_halasu"]/option[text()="od 39 do 40 dB"]').click()
        elif 41 <= halas <= 42:
            driver.find_element_by_xpath('//*[@id="poziom_halasu"]/option[text()="od 41 do 42 dB"]').click()
        elif 43 <= halas <= 44:
            driver.find_element_by_xpath('//*[@id="poziom_halasu"]/option[text()="od 43 do 44 dB"]').click()
        elif 44 < halas <= 45:
            driver.find_element_by_xpath('//*[@id="poziom_halasu"]/option[text()="od 44 do 45 dB"]').click()
        elif 46 <= halas <= 47:
            driver.find_element_by_xpath('//*[@id="poziom_halasu"]/option[text()="od 46 do 47 dB"]').click()
        elif 48 <= halas <= 49:
            driver.find_element_by_xpath('//*[@id="poziom_halasu"]/option[text()="od 48 do 49 dB"]').click()
        elif 51 <= halas <= 55:
            driver.find_element_by_xpath('//*[@id="poziom_halasu"]/option[text()="od 51 do 55 dB"]').click()
        elif 56 <= halas <= 60:
            driver.find_element_by_xpath('//*[@id="poziom_halasu"]/option[text()="od 56 do 60 dB"]').click()
        elif 61 <= halas <= 65:
            driver.find_element_by_xpath('//*[@id="poziom_halasu"]/option[text()="od 61 do 65 dB"]').click()
        elif 66 <= halas <= 70:
            driver.find_element_by_xpath('//*[@id="poziom_halasu"]/option[text()="od 66 do 70 dB"]').click()
        elif 71 <= halas <= 75:
            driver.find_element_by_xpath('//*[@id="poziom_halasu"]/option[text()="od 71 do 75 dB"]').click()
        elif 76 <= halas <= 80:
            driver.find_element_by_xpath('//*[@id="poziom_halasu"]/option[text()="od 76 do 80 dB"]').click()
        elif 81 <= halas <= 85:
            driver.find_element_by_xpath('//*[@id="poziom_halasu"]/option[text()="od 81 do 85 dB"]').click()
        elif 86 <= halas <= 90:
            driver.find_element_by_xpath('//*[@id="poziom_halasu"]/option[text()="od 86 do 90 dB"]').click()
    except ValueError:
        pass
    except NoSuchElementException:
        pass
    except ElementNotInteractableException:
        pass

    if tech_desc.find('wakacj') != -1:
        driver.find_element_by_xpath('//*[@id="funkcje_dodatkowe_lodowki"]/option[1]').click()
    if tech_desc.find('komora świeżości') != -1:
        driver.find_element_by_xpath('//*[@id="funkcje_dodatkowe_lodowki"]/option[text()="komora świeżości"]').click()
    if tech_desc.find('komora świeżości') != -1:
        driver.find_element_by_xpath('//*[@id="funkcje_dodatkowe_lodowki"]/option[text()="kostkarka"]').click()
    if tech_desc.find('kontrolą wilgotności') != -1:
        driver.find_element_by_xpath('//*[@id="funkcje_dodatkowe_lodowki"]/option[text()="szuflada z kontrolą '
                                     'wilgotności"]').click()

    poj_uz = tech_desc[tech_desc.find('pojemność użytkowa') + 27:]
    poj_uz = poj_uz[:poj_uz.find('\n')]
    poj_uz = poj_uz.replace(' ', '')
    poj_uz = poj_uz.replace('l', '')
    poj_uz = poj_uz.replace(',', '.')
    try:
        poj_uz = float(poj_uz)

        if poj_uz <= 30:
            driver.find_element_by_xpath('//*[@id="pojemnosc_uzytkowa"]/option[text()="do 30 litrów"]').click()
        elif 31 <= poj_uz <= 49:
            driver.find_element_by_xpath('//*[@id="pojemnosc_uzytkowa"]/option[text()="od 31 do 49 litrów"]').click()
        elif 50 <= poj_uz <= 59:
            driver.find_element_by_xpath('//*[@id="pojemnosc_uzytkowa"]/option[text()="od 50 do 59 litrów"]').click()
        elif 60 <= poj_uz <= 70:
            driver.find_element_by_xpath('//*[@id="pojemnosc_uzytkowa"]/option[text()="od 60 do 70 litrów"]').click()
        elif 71 <= poj_uz <= 90:
            driver.find_element_by_xpath('//*[@id="pojemnosc_uzytkowa"]/option[text()="od 71 do 90 litrów"]').click()
        elif 91 <= poj_uz <= 110:
            driver.find_element_by_xpath('//*[@id="pojemnosc_uzytkowa"]/option[text()="do 110 litrów"]').click()
        elif 110 <= poj_uz <= 130:
            driver.find_element_by_xpath('//*[@id="pojemnosc_uzytkowa"]/option[text()="od 110 do 130 litrów"]').click()
        elif 131 <= poj_uz <= 140:
            driver.find_element_by_xpath('//*[@id="pojemnosc_uzytkowa"]/option[text()="od 131 do 140 litrów"]').click()
        elif 141 <= poj_uz <= 159:
            driver.find_element_by_xpath('//*[@id="pojemnosc_uzytkowa"]/option[text()="od 141 do 159 litrów"]').click()
        elif 160 <= poj_uz <= 189:
            driver.find_element_by_xpath('//*[@id="pojemnosc_uzytkowa"]/option[text()="od 160 do 189 litrów"]').click()
        elif 190 <= poj_uz <= 209:
            driver.find_element_by_xpath('//*[@id="pojemnosc_uzytkowa"]/option[text()="od 190 do 209 litrów"]').click()
        elif 210 <= poj_uz <= 219:
            driver.find_element_by_xpath('//*[@id="pojemnosc_uzytkowa"]/option[text()="od 210 do 219 litrów"]').click()
        elif 220 <= poj_uz <= 249:
            driver.find_element_by_xpath('//*[@id="pojemnosc_uzytkowa"]/option[text()="od 220 do 249 litrów"]').click()
        elif 250 <= poj_uz <= 399:
            driver.find_element_by_xpath('//*[@id="pojemnosc_uzytkowa"]/option[text()="od 250 litrów"]').click()
        elif poj_uz > 400:
            driver.find_element_by_xpath('//*[@id="pojemnosc_uzytkowa"]/option[text()="od 400 litrów"]').click()
    except ValueError:
        pass
    except NoSuchElementException:
        pass
    except ElementNotInteractableException:
        pass
