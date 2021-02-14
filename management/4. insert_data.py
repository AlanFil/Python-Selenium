import mysql.connector
import pyautogui
from time import sleep

from keyboard import wait
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException, \
    ElementNotInteractableException
from selenium.webdriver.common.keys import Keys

from management.attributes import attributes
from management.categories import categories
from management.loggin_in import driver


def insert_data(report_label, product, model=None, descriptions=None, brand=None):
    folder_name = model
    set_images = False  # parametr służący w przyszłości do wybierania czy algorytm ma dodawać zdjęcia opisu do bazy

    if descriptions is None:
        descriptions = [1, '', '']

    try:
        driver.find_element_by_css_selector('td.a-right button').click()  # Dodaj produkt
    except NoSuchElementException:
        pass

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

    attr_set = ''
    # szukanie zestawu cech
    for i in range(len(results)):
        if results[i][1].lower() in product[1].lower() and 'zabudo' in product[6].lower():
            attr_set = results[i][4]
            weight = str(results[i][3])
            if weight == '':
                weight = '1'
            break
        elif results[i][1].lower() in product[1].lower():
            attr_set = results[i][2]
            weight = str(results[i][3])
            if weight == '':
                weight = '1'
            break
        else:
            weight = '1'

    try:
        # zaznaczanie zestawu cech
        driver.find_element_by_xpath(f'//*[@id="attribute_set_id"]/option[text()="{attr_set}"]').click()
    except NoSuchElementException:
        print(f'Nie znaleziono zestawu cech. Zrób to ręcznie i wciśnij Enter ({product[1]})\n')
        wait('enter')

    driver.find_element_by_css_selector('button[title="Kontynuuj"]').click()  # Konunuuj

    driver.implicitly_wait(3)  # Zawsze czekaj 3 sekundy przed wyświetleniem błędu na wczytanie elementów strony
    driver.find_element_by_name('product[name]').send_keys(product[1])  # umieść nazwę produktu

    # umieść opis graficzny
    driver.find_element_by_name('product[description]').send_keys(descriptions[0])

    # jeżeli nie ma opisu, to nie ma też grafik
    if set_images:
        try:
            driver.find_element_by_xpath('(//button[@title="Edytor WYSIEYG"])[1]').click()  # kliknij na edytor WYSIEYG

            if folder_name is not None:
                driver.find_element_by_xpath('/html/body/div[2]/table[2]/tbody/tr/td[2]/div/div['
                                             '1]/div/span/div/span/table/tbody/tr[1]/td/div/span/table[2]/tbody/tr/td['
                                             '24]/a/span[1]').click()  # kliknij na "Wstawianie obrazka"
                sleep(1)  # poczekaj sekundę, aż wczyta się okno
                pyautogui.click(1135, 470)  # kliknij na "Browse" (nie znalazłem lepszego sposobu)

                sleep(7)  # poczekaj 7 sekund (+ ew. 3 sekundy z metody "implicitly_wait") na wczytanie treści
                try:
                    driver.find_element_by_xpath(f'//a/span[text()="{brand}"]').click()  # wybierz folder z nazwą marki
                    driver.find_element_by_xpath(f'//a/span[text()="{brand}"]').click()  # wybierz folder z nazwą marki
                except ElementNotInteractableException:
                    print("Spróbuj ponownie (enter)")
                    wait('Enter')
                    driver.find_element_by_xpath(f'//a/span[text()="{brand}"]').click()
                    driver.find_element_by_xpath(f'//a/span[text()="{brand}"]').click()

                sleep(3)
                try:
                    driver.find_element_by_xpath('/html/body/div[1]/table[2]/tbody/tr/td[2]/div/div/div/div/div/div/div['
                                                 '2]/div/div[2]/table/tbody/tr/td[2]/button[1]').click()  # Utwórz folder
                    sleep(1)
                    pyautogui.click(900, 160)  # ustaw focus na oknie do wpisywania nazwy folderu
                    pyautogui.typewrite(folder_name)  # wprowadź nazwę folderu
                    pyautogui.press('Enter')  # zatwierdź enterem
                    sleep(12)
                    driver.find_element_by_xpath(
                        f'//a/span[text()="{folder_name}"]').click()  # kliknij na nazwę folderu
                    sleep(2)
                    pyautogui.press('Home')  # wróć na górę
                    sleep(2)
                    pyautogui.click(900, 290)  # kliknij na "Choose files"
                    pyautogui.click(900, 305)  # drugi dla pewności
                    sleep(2.5)  # poczekaj na załadownie okna
                    pyautogui.hotkey('ctrl', 'l')  # Ctrl + L (przejdź do adresu folderu)
                    # wprowadź ścieżkę folderu z obrazkami do opisu
                    pyautogui.typewrite(
                        f'C:/Users/user/PycharmProjects/Adding-automating-products/Imgs/{folder_name}/obrazki_opisu')
                    pyautogui.press('enter')  # zatwierdź enterem
                    sleep(2)
                    pyautogui.click(300, 300)
                    pyautogui.hotkey('ctrl', 'a')  # Ctrl + A (zaznacz wszystko)
                    pyautogui.press('enter')  # zatwierdź Enterem
                    pyautogui.press('Home')  # wróć na górę
                    sleep(7)
                except UnexpectedAlertPresentException:
                    report_label['text'] += f'Produkt {product[1]} już jest dodany.\n'
                    pyautogui.click(1150, 180)
        except NoSuchElementException:
            pass
        finally:
            try:
                driver.find_element_by_xpath('//*[@id="browser_window_close"]').click()  # zamknij jedno okno
                driver.find_element_by_xpath('/html/body/div[6]/div/a[5]').click()  # zamknij drugie okno
                driver.find_element_by_xpath('//button[@title="Submit"]').click()  # zamknij trzecie okno
            except NoSuchElementException:
                pass

    driver.find_element_by_name('product[short_description]').send_keys(descriptions[1])  # wprowadź krótki opis
    if not descriptions[1] == '':
        try:
            driver.find_element_by_xpath('(//button[@title="Edytor WYSIEYG"])[2]').click()  # otwórz edytor WYSIEYG
            # zamknij edytory WYSIEYG (żeby sformatować tekst)
            driver.find_element_by_xpath('//button[@title="Submit"]').click()
        except NoSuchElementException:
            print("Otwórz Edytor WYSIEYG dla opisu krótkiego, zatwierdź i wciśnij Enter")
            wait('Enter')

    driver.find_element_by_name('product[sku]').send_keys(product[2])  # wprowadzenie Eanu
    driver.find_element_by_name('product[weight]').send_keys(weight)  # wprowadzenie wagi

    driver.find_element_by_xpath('//*[@id="status"]/option[3]').click()  # status: Nieaktywny
    # jeżeli marka jest znana - zaznacz ją
    if brand != 'nie wykryto':
        try:
            driver.find_element_by_xpath(f'//*[@id="manufacturer"]/option[text()="{brand}"]').click()
        except NoSuchElementException:
            try:
                driver.find_element_by_xpath(f'//*[@id="manufacturer"]/option[text()="{brand.upper()}"]').click()
            except NoSuchElementException:
                pass

    driver.find_element_by_name('product[url_key]').send_keys(product[1])  # wprowadzenie klucza url
    driver.find_element_by_name('product[manufacturer_code]').send_keys(product[0])  # wprowadzenie klucza producenta

    # znajdź link do aukcji ceneo
    driver.execute_script('''window.open("about:blank", "_blank");''')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(f'https://www.ceneo.pl/;szukaj-{model}?nocatnarrow=1')
    try:
        ceneo_name = driver.find_element_by_xpath('//div[@class="cat-prod-row__desc"]//a').text
        # weź tylko litery z dwóch nazw modeli (ceneo_name oraz mod)
        buffor = ''
        for i in range(len(ceneo_name)):
            if ceneo_name[i].isalpha():
                buffor += ceneo_name[i]
        ceneo_name = buffor
        mod = ''
        for i in range(len(model)):
            if model[i].isalpha():
                mod += model[i]

        # sprawdzenie ręczne czy analiza jest poprawna
        print(f'Model: {mod.lower()} -- Ceneo: {ceneo_name.lower()} -- {mod.lower() in ceneo_name.lower()}')
        if mod.lower() in ceneo_name.lower():
            link = driver.find_element_by_xpath('//div[@class="cat-prod-row__desc"]//a').get_attribute('href')
            driver.execute_script("window.close('');")
            driver.switch_to.window(driver.window_handles[0])
            driver.find_element_by_name('product[link_ceneo]').send_keys(link)
        else:
            driver.execute_script("window.close('');")
            driver.switch_to.window(driver.window_handles[0])
    except NoSuchElementException:
        driver.execute_script("window.close('');")
        driver.switch_to.window(driver.window_handles[0])

    driver.find_element_by_name('product[tech_description]').send_keys(descriptions[2])  # wprowadź opis techniczny
    if not descriptions[2] == '':
        driver.find_element_by_xpath('(//button[@title="Edytor WYSIEYG"])[3]').click()  # otwórz edytor WYSIEYG
        driver.find_element_by_xpath('//button[@title="Submit"]').click()  # zamknij edytor WYSIEYG

    # zazancz centralę w punktach odbioru
    try:
        driver.find_element_by_xpath(f'//*[@id="pickup_store"]/option[1]').click()
    except NoSuchElementException:
        pass

    if 'sony' in product[1].lower():
        sony_rec = [2, 3, 4, 7, 8, 9, 10, 11, 21, 25]
        for ele in sony_rec:
            driver.find_element_by_xpath(
                f'//*[@id="pickup_store"]/option[{ele}]').click()
    if 'samsung' in product[1].lower():
        samsing_rec = [5, 6, 12, 13, 14, 15, 16, 17, 18, 19, 20, 23]
        for ele in samsing_rec:
            driver.find_element_by_xpath(
                f'//*[@id="pickup_store"]/option[{ele}]').click()
    if 'huawei' in product[1].lower():
        huawei_rec = [24]
        for ele in huawei_rec:
            driver.find_element_by_xpath(
                f'//*[@id="pickup_store"]/option[{ele}]').click()

        # wyłącz Huaweia z negocjacji cen
        driver.find_element_by_xpath('//select[@name="product[price_negotiation_hide]"]/option[1]').click()

    # podobno nie są już potrzebne, więc zakomentowałem, ale zostawiam w razie W
    # driver.find_element_by_name('product[search_keywords]').send_keys(f'{product[1]} {product[2]}')  # słowa kluczowe

    # Ceny
    driver.find_element_by_tag_name('body').send_keys(
        Keys.HOME)  # powrót na górę strony, aby można było odnaleźć szukane elementy
    sleep(0.5)  # poczekaj na działanie klawisza Home
    driver.find_element_by_css_selector('a[title="Ceny"]').click()  # przejdź do zakładki "Ceny"
    driver.find_element_by_name('product[price]').send_keys('9999,99')  # wprowadź domyślną cenę 9999,99
    driver.find_element_by_css_selector('#tax_class_id > option:nth-child(2)').click()  # Klasa podatku: Brak

    # Matrix Media
    driver.find_element_by_css_selector('a[title="Matrix Media"]').click()  # przejdź do zakładki "Matrix Media"

    # jeżeli reguła i priorytet nadawcy są poprawnie wpisane, to zaznacz je
    try:
        driver.find_element_by_xpath(
            f'//*[@id="rule"]/option[text()="{product[4]}"]').click()
    except NoSuchElementException:
        report_label['text'] += "Błędnie wpisana reguła\n"
    try:
        driver.find_element_by_xpath(
            f'//*[@id="supplier"]/option[text()="{product[5]}"]').click()
    except NoSuchElementException:
        report_label['text'] += "Błędnie wpisany dostawca\n"

    # Porównywarki cenowe
    driver.find_element_by_css_selector('a[title="Porównywarki cenowe"]').click()
    driver.find_element_by_xpath('//*[@id="export_ceneo"]/option[1]').click()

    # Kategorie
    driver.find_element_by_css_selector('a[title="Kategorie"]').click()

    categories(product[1], product[6], attr_set)  # Zbyt rozległe, żeby to zostawiać tutaj

    # Zestaw cech
    try:
        driver.find_element_by_css_selector(f'a[title="{attr_set}"]').click()
        attributes(descriptions[2], brand)
    except NoSuchElementException:
        pass

    # Obrazki produktu
    driver.find_element_by_css_selector('a[title="Obrazki produktu"]').click()

    # jeżeli nie ma opisu, to nie ma też grafik
    if not descriptions[0] == 1:
        driver.find_element_by_tag_name('body').send_keys(
            Keys.HOME)  # powrót na górę strony, aby można było odnaleźć szukane elementy
        sleep(2)
        pyautogui.click(500, 570)
        pyautogui.click(500, 620)
        pyautogui.click(500, 650)  # trzy razy dla pewności, bo bywało różnie
        sleep(2)
        pyautogui.hotkey('ctrl', 'l')  # Ctrl + L
        pyautogui.keyUp('ctrl')
        pyautogui.keyUp('l')  # puszczenie Ctrl + L
        # wprowadzenie ścieżki gdzie znajdują się obrazki produktu
        pyautogui.typewrite(
            f'C:/Users/user/PycharmProjects/Adding-automating-products/Imgs/{folder_name}/obrazki_produktu')
        pyautogui.press('enter')  # Enter
        sleep(0.5)
        pyautogui.click(300, 300)
        pyautogui.hotkey('ctrl', 'a')  # Ctrl + A
        pyautogui.press('enter')  # Enter
        sleep(1)

    sleep(2)
    driver.find_element_by_css_selector('button[title="Zapisz i kontynuuj edycję"]').click()  # Zapisz
    wait('enter')

    sleep(3)
    driver.find_element_by_css_selector('button[title="Zapisz"]').click()  # Zapisz
    sleep(3)

    report_label['text'] += f'Dodano {product[1]}\n'
