from management.loggin_in import driver


def categories(name, parameter, attr_set):
    name = name.lower()
    parameter = parameter.lower()
    # TV i Audio
    if 'Telewizory' in attr_set or 'Słuchawki' in attr_set:
        driver.find_element_by_xpath(
            '//div[contains(@class, "x-tree-node")]//span[contains(text(), "TV i Audio")]').click()
        if 'Telewizory' in attr_set:  # Telewizory
            driver.find_element_by_xpath(
                '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Telewizory")]').click()
        if 'Słuchawki' in attr_set:  # Słuchawki
            driver.find_element_by_xpath(
                '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Słuchawki")]').click()

    # AGD
    if 'wolnost' in parameter or 'zabudo' in parameter:
        driver.find_element_by_xpath('//div[contains(@class, "x-tree-node")]//span[contains(text(), "AGD")]').click()

        if 'wolnost' in parameter:  # Wolnostojące
            driver.find_element_by_xpath(
                '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Wolnostojące")]').click()
            if 'Pralki' in attr_set:  # Pralki
                driver.find_element_by_xpath(
                    '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Pralki")]').click()
            if 'Suszarki' in attr_set:  # Suszarki
                driver.find_element_by_xpath(
                    '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Suszarki")]').click()
            if 'Pralko-suszarki' in attr_set:  # Pralko-suszarki
                driver.find_element_by_xpath(
                    '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Pralko-suszarki")]').click()
            if 'Lodówki' in attr_set:  # Lodówki
                driver.find_element_by_xpath(
                    '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Lodówki")]').click()
            if 'Zamrażarki' in attr_set:  # Zamrażarki
                driver.find_element_by_xpath(
                    '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Zamrażarki")]').click()
            if 'Kuchnie wolnostojące > Kuchnie' in attr_set:  # Kuchnie wolnostojące
                driver.find_element_by_xpath(
                    '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Kuchnie wolnostojące")]').click()
            if 'Okapy' in attr_set:  # Okapy
                driver.find_element_by_xpath(
                    '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Okapy")]').click()
            if 'Zmywarki' in attr_set:  # Zmywarki
                driver.find_element_by_xpath(
                    '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Zmywarki")]').click()
            if 'Kuchnie mikrofalowe' in attr_set:  # Kuchnie mikrofalowe
                driver.find_element_by_xpath(
                    '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Kuchnie mikrofalowe")]').click()

        elif 'zabudo' in parameter:  # Do zabudowy
            driver.find_element_by_xpath(
                '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Do zabudowy")]').click()
            if 'Lodówki do zabudowy' in attr_set:  # Lodówki (do zabudowy)
                driver.find_element_by_xpath(
                    '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Lodówki")]').click()
            if 'Zmywarki' in attr_set:  # Zmywarki (do zabudowy)
                driver.find_element_by_xpath(
                    '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Zmywarki")]').click()
            if 'Piekarniki do zabudowy' in attr_set:  # Piekarniki (do zabudowy)
                driver.find_element_by_xpath(
                    '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Piekarniki")]').click()
            if 'Płyty do zabudowy' in attr_set:  # Płyty do zabudowy
                driver.find_element_by_xpath(
                    '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Płyty")]').click()
            if 'Kuchenki mikrofalowe do zabudowy' in attr_set:  # Kuchenki mikrofalowe do zabudowy
                driver.find_element_by_xpath(
                    '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Kuchenki mikrofalowe")]').click()
            if 'Okapy' in attr_set:  # Okapy (do zabudowy)
                driver.find_element_by_xpath(
                    '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Okapy kuchenne")]').click()
            if 'Ekspresy' in attr_set:  # Ekspresy (do zabudowy)
                driver.find_element_by_xpath(
                    '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Ekspresy")]').click()
            if 'Parownice' in attr_set:  # Parowary (do zabudowy)
                driver.find_element_by_xpath(
                    '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Parowary")]').click()

        else:  # Akcesoria AGD
            driver.find_element_by_xpath(
                '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Akcesoria AGD")]').click()

    # AGD małe
    if 'Depilatory' in attr_set or 'Maszynki do strzyżenia' in attr_set:
        driver.find_element_by_xpath(
            '//div[contains(@class, "x-tree-node")]//span[contains(text(), "AGD małe")]').click()
        # Sprzątanie #
        # Kuchnia #
        if 'Depilatory' in attr_set or 'Maszynki do strzyżenia' in attr_set:  # Uroda i zdrowie
            driver.find_element_by_xpath(
                '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Uroda i zdrowie")]').click()
            if 'Depilatory' in attr_set or 'Maszynki do strzyżenia' in attr_set:  # Golenie i strzyżenie
                driver.find_element_by_xpath(
                    '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Golenie i strzyżenie")]').click()
        # Lodówki turystyczne #

    # Smartfony i GPS
    if 'watch' in name or 'zegarek' in name or 'telefon' in name or 'smartfon' in name or 'smartphone' in name:
        driver.find_element_by_xpath(
            '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Smartfony i GPS")]').click()
        # Smartfony
        if 'smartfon' in name or 'smartphone' in name:
            driver.find_element_by_xpath(
                '(//div[contains(@class, "x-tree-node")]//span[contains(text(), "Smartfony")])[2]').click()
            if attr_set == 'Telefony i smartfony > Smartfony z Android':
                driver.find_element_by_xpath(
                    '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Smartfony z Androidem")]').click()

        if 'watch' in name or 'zegarek' in name:  # Smartwatche i Opaski sportowe
            driver.find_element_by_xpath(
                '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Smartwatche i Opaski sportowe")]').click()
        # Smarthome #
        # Akcesoria GSM #
        if 'do telefonu' in name:
            driver.find_element_by_xpath(
                '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Akcesoria GSM")]').click()
        # Akcesoria samochodowe #

    # Komputery i laptopy
    if 'Laptopy / Ultrabooki' in attr_set or 'Tablety' in attr_set:
        driver.find_element_by_xpath(
            '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Komputery i Laptopy")]').click()
        if 'Tablety' in attr_set:  # Tablety
            driver.find_element_by_xpath(
                '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Tablety")]').click()
        # AIO #
        if 'Laptopy / Ultrabooki' in attr_set:  # Laptopy / Ultrabooki
            driver.find_element_by_xpath(
                '//ul[contains(@class, "x-tree-node-ct")]//span[contains(text(), "Laptopy")]').click()
        # Peryferia
        if 'Dyski HDD' in attr_set or 'Dyski SSD' in attr_set:
            driver.find_element_by_xpath(
                '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Peryferia")]').click()
            if 'Dyski HDD' in attr_set or 'Dyski SSD' in attr_set:  # Dyski
                driver.find_element_by_xpath(
                    '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Dyski")]').click()
        # Akcesoria do komputerów #
        # Akcesoria do laptopów #

    # Sport i rekreacja
    if 'Deskorolki' in attr_set:
        driver.find_element_by_xpath(
            '//div[contains(@class, "x-tree-node")]//span[contains(text(), "Sport i rekreacja")]').click()

    # Gaming
    if 'Gry' in attr_set:
        driver.find_element_by_xpath('//div[contains(@class, "x-tree-node")]//span[contains(text(), "Gaming")]').click()

    # Foto i Video #
    # Lego #
    # >> Outlet << #
    # Oferta specjana #
    # Sony #
    # Samsung #
    if 'samsung' in name:
        driver.find_element_by_xpath('//div[contains(@class, "x-tree-node")]//span[contains(text(), "Samsung")]').click()
    # Karcher #
    # Miele #
    # Apple #
    # AB #
    # MORAX #

    return
