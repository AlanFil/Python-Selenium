from selenium.common.exceptions import NoSuchElementException
from globals import file_path
from management import ImgRefractor
from management.loggin_in import driver


def electrolux(report_lab, product, model):
    driver.implicitly_wait(2)
    driver.get(product[6])
    driver.find_element_by_xpath(
        '/html/body/div[2]/form/div[4]/div/div/div/div[1]/div/div[2]/table/tbody/tr[2]/td/input').send_keys(
        'rafal.zalas@matrixmedia.pl')
    driver.find_element_by_xpath(
        '/html/body/div[2]/form/div[4]/div/div/div/div[1]/div/div[2]/table/tbody/tr[4]/td/input').send_keys('raza849')
    driver.find_element_by_xpath(
        '/html/body/div[2]/form/div[4]/div/div/div/div[1]/div/div[2]/table/tbody/tr[7]/td/input').click()

    """ Obrazki produktu """
    imgs_desc = driver.find_elements_by_xpath('//*[@id="Family"]//div[@class="colPicture"]//img')
    prod_img_names = []
    for link in imgs_desc:
        prod_img_name = link.get_attribute('src')
        prod_img_name = prod_img_name[prod_img_name.rfind('/') + 1:]
        prod_img_name = prod_img_name[:prod_img_name.find('.')]
        prod_img_names.append(prod_img_name)

    """ Opis graficzny """
    tiles = driver.find_elements_by_xpath('//div[@id="KeyFeatures"]/div[@class="SecondaryBenefits"]/div[@class="sb"]')
    full = []
    for i in range(len(tiles)):
        content = tiles[i].text.split('\n')
        header = f'<div class="two-col-asymmetrically"><div class="right-side"><h2 class="important-header">{content[0]}</h2>'
        description = f'<p style="font-size: large; text-align: center;">{content[1]}</p></div>'
        link = driver.find_element_by_xpath(
            f'//div[@id="KeyFeatures"]/div[@class="SecondaryBenefits"]/div[@class="sb"][{i + 1}]//img').get_attribute(
            'src')
        if 'gif' in link:
            link = 'random '

        full.append([header, description, link])

    for i in range(len(full)):
        # obetnij link i rozszerzenie (do znalezienia nazwy obrazka do pobrania)
        full[i][2] = full[i][2][full[i][2].rfind('/') + 1:]
        full[i][2] = full[i][2][:full[i][2].find('.')]

    driver.find_element_by_xpath('//a[contains(text(), "Medias")]').click()
    driver.switch_to.window(driver.window_handles[2])

    # zbierz wszystkie nazwy plików
    rows = driver.find_elements_by_xpath('//li')
    rows_links = driver.find_elements_by_xpath('//li/a')
    rows_text = [row.text for row in rows]
    # podczas wybierania losowego obrazka łatwiej znaleźć ładny od końca
    rows_text = rows_text[::-1]

    # oddziel obrazki znalezione, aby ich nie powielać
    used = [x[2] for x in full if x[2] != 'random']
    for prod_img_name in prod_img_names:
        used.append(prod_img_name)

    for i in range(len(full)):
        img_link = False
        for row_t in rows_text:
            link_to_image = rows_links[rows_text.index(row_t)*(-1)-1].get_attribute('href')
            name_of_image = row_t[row_t.find(':') + 2:row_t.find('.')]

            # Odrzuć inne możliwości niż "700x700 Presentation"
            if '700x700 Presentation' not in row_t:
                continue

            # odrzucaj rozszerzenia "bmp" oraz "eps"
            excension = link_to_image[-5:].lower()
            if 'bmp' in excension or 'eps' in excension:
                continue

            # sprawdź czy znaleziony wiersz należy do tych z opisu graficznego
            # Jeżeli nie został ustlaony, to wybierz pierwsz-lepszy
            if full[i][2] == 'random':
                if name_of_image not in used:
                    img_link = link_to_image
                    print(f'Wybrano: {row_t} w miejce Random ({name_of_image})')
                    break
            elif full[i][2] in row_t:
                img_link = link_to_image
                print(f'Wybrano: {row_t} w miejce {full[i][2]} ({name_of_image})')
                break

            # na wszelki wypadek jeżeli nie znajdzie poszukiwanego zdjęcia, to wybierze losowe
            if not img_link and name_of_image not in used:
                print(f'Wybrano: {row_t} w miejce obrazka produktu ({name_of_image})')
                img_link = link_to_image

            # jak już tu jesteś, to pobierz też obrazki produktu
            for prod_img_name in prod_img_names:
                if prod_img_name in row_t:
                    prod_img_link = link_to_image
                    ImgRefractor.prod_img(f'{file_path}/{model}', prod_img_link, i)
                    break

        if not img_link:
            print(f'Nie znaleziono obrazka dla: {full[i][2]}')
            continue

        print(img_link)
        # dodaj nazwę pliku do listy użytych ("used")
        if name_of_image not in used:
            used.append(name_of_image)

        size, file_type = ImgRefractor.desc_img(f'{file_path}/{model}', img_link, i)
        full[i][2] = f'<img src="https://matrixmedia.pl/media/wysiwyg/Electrolux/{model}/{i}.{file_type}" /></div>'

    print(used)
    driver.switch_to.window(driver.window_handles[1])

    """ Opis krótki """
    try:
        # weź do 8 elementów z opisu funkcji. Pierwszy element to słowo "funkcje"
        short = driver.find_element_by_id('FeaturesBullet').text.split('\n')[1:9]
        for i in range(len(short)):
            while True:
                if short[i][0] == ' ':
                    short[i] = short[i][1:]
                else:
                    # dodaj tagi HTML'a
                    short[i] = f'<li>{short[i]}<li>'
                    break
        short = '<ul>' + ''.join(short) + '</ul>'
    except NoSuchElementException:
        short = 'Popraw'
        print('Coś jest nie tak ze ścieżką w Selenium do krótkiego opisu')

    """ Opis techniczny """
    tech = [
        '<table id="plan_b" class="data-table"><tbody><tr class="specs_category"><td colspan="2">Specyfikacja</td></tr>']
    for row in driver.find_elements_by_xpath('//div[@id="TechnicalSpecs"]//div[@class="element"]'):
        name, value = row.text.split('\n')
        tech.append(f'<tr><td class="c_left">{name}</td><td class="c_left">{value}</td></tr>')
    tech.append('</tbody></table>')

    full = [['<div class="product-description-section">']] + full + [['</div>']]
    reg = []
    for ele in full:
        reg.append(''.join(ele))
    reg = ''.join(reg)

    tech = ''.join(tech)

    return [reg, short, tech]
