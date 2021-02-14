import requests
from scrapy import Selector
from globals import file_path
from management.ImgRefractor import prod_img, desc_img


def blaupunkt(model, html):
    sel = Selector(text=requests.get(html).content)

    # Zdjęcia produktu
    prod_imgs_links = sel.xpath('//div[@id="product_gallery_new"]//img/@src').extract()
    for prod_img_link in prod_imgs_links:
        prod_img(f'{file_path}/{model}', 'https://www.blaupunkt.com/' + prod_img_link,
                 prod_imgs_links.index(prod_img_link), crop=True)

    # Opis graficzny
    graph_desc = ['<div class="product-description-section">']
    for i, ele in enumerate(sel.xpath('//div[contains(@class, "newkeyvisual")]')):
        complete_element = []

        text = ele.xpath('.//text()').extract()
        if text[0].isupper():
            if i % 2 == 0:
                complete_element.append(f'<div class="two-col-asymmetrically"><div class="right-side"><h2 class="important-header">{text[0]}</h2>')
            else:
                complete_element.append(f'<div class="two-col-asymmetrically"><div class="left-side"><h2 class="important-header">{text[0]}</h2>')
            try:
                complete_element.append('<p style="font-size: large;">' + ''.join(text[1:]) + '</p></div>')
            except IndexError:
                complete_element.append('<p style="font-size: large;"></p></div>')
        else:
            complete_element.append('<div class="two-col-asymmetrically"><div class="right-side"><h2 class="important-header"></h2><p style="font-size: large;">' + '\n\n'.join(text) + '</p></div>')

        img = 'https://www.blaupunkt.com/' + ele.xpath('.//img/@src').extract()[0]
        desc_img(f'{file_path}/{model}', img, i, crop=False, force_small=True)

        complete_element.append(f'<img alt="" src="https://matrixmedia.pl/media/wysiwyg/Blaupunkt/{model}/{i}.jpg" /></div>')

        graph_desc.append(''.join(complete_element))
    graph_desc.append('</div>')

    # Opis techniczny
    short_desc = ['<ul>']
    tech_desc_data = sel.xpath('//div[@id="tab-details"]/ul/li/text()').extract()
    tech_desc = ['<table id="plan_b" class="data-table"><tbody><tr class="specs_category"><td colspan="2">Specyfikacja</td></tr>']
    tech_desc_end = []
    for ele in tech_desc_data:
        if len(ele.split(':')) == 2:
            name, value = ele.split(':')
            tech_desc.append(f'<tr><td class="c_left">{name}</td><td class="c_left">{value}</td></tr>')
            short_desc.append(f'<li>{name}: {value}</li>')
        else:
            if not tech_desc_end:
                tech_desc_end.append(f'<tr><td class="c_left">Dodatkowo</td><td class="c_left">{ele}</td></tr>')
            else:
                tech_desc_end.append(f'<tr><td class="c_left"></td><td class="c_left">{ele}</td></tr>')

    tech_desc.extend(tech_desc_end)
    tech_desc.append('</tbody></table>')
    tech_desc = ''.join(tech_desc)

    short_desc.append('</ul>')
    short_desc = ''.join(short_desc)

    graph_desc = ''.join(graph_desc)
    print(graph_desc)
    return [graph_desc, short_desc, tech_desc]


if __name__ == '__main__':
    blaupunkt('VCC301', 'https://www.blaupunkt.com/pl/nc/produkty/dom/odkurzacze/products/single/18609')
