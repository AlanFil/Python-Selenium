import requests
from googlesearch import search
from scrapy import Selector


def google_search(product):
    stop = 10
    # tworzymy pętlę, która wyświetli nam 10 wyników
    while 1:
        links_list = []
        headlines_list = []
        n = 1
        for link in search(product,  # wyszukiwana fraza
                           lang='pl',  # język
                           num=stop,  # numer wyników na stronę
                           stop=stop  # na tym wyniku skończ wyszukiwanie
                           ):
            # dodajemy nowy adres do listy
            links_list.append(link)
            # wyznaczamy tytuł strony
            sel = Selector(text=requests.get(link).content)
            try:
                headline = sel.css('title::text').extract()
            except ValueError:
                headline = 'Nie rozpoznano'
            # dodajemy tytuł strony do listy
            headlines_list.append(headline)
            # wypisujemy wyszukane wyniki
            print(f'{n}. {headline[0]}\n{link}')
            n = n + 1

        web_n = int(input('Którą stronę odwiedzić? (po więcej wpisz "0"): '))

        if web_n in range(1, n + 1):
            break
        if web_n == 0:
            stop = stop + 10
    # zwracamy stronę wybraną przez użytkownika
    return links_list[web_n - 1]
