import pandas as pd

from dict.electrolux_sheets import electrolux_sheets
from globals import file_path
from management.ImgRefractor import desc_img, prod_img


def electrolux_file(product, model):
    code = product[0]
    file_name = 'MatrixMedia30112020.xlsx'
    path = 'MatrixMedia\\' + file_name

    data_ExcelFile = pd.ExcelFile(path)
    data = {sheet_name: data_ExcelFile.parse(sheet_name) for sheet_name in data_ExcelFile.sheet_names}

    for key in data.keys():
        res_num = len(data[key].loc[data[key]["Model D"] == code])
        if res_num == 1:
            sheet = key
            keys = [key for key in data[key].keys()]
            product_data = data[key].loc[data[key]["Model D"] == code]
            break
        elif res_num > 1:
            print(f'Come, master! Check this out... {res_num} products found!')
            return

    try:
        product_data, keys, sheet
    except NameError:
        print(f'I found nothing, master! Mercy!')
        return

    product[6] = product_data["Installation Type"].iloc[0]  # wolnostojące / do zabudowy

    """ Producs imgs """
    imgs_link_list = product_data["Product standard"].iloc[0].split(';')
    imgs_link_list = [ill for ill in imgs_link_list if ill.startswith('http')]

    for img_link in imgs_link_list:
        prod_img(f'{file_path}/{model}', img_link, imgs_link_list.index(img_link), crop=False)

    short_description = '<p>' + str(product_data["Product Short Description"].iloc[1]) + '</p>'

    long_description = ['<div class="product-description-section">']
    columns = ['USP', 'SB1', 'SB2', 'SB3', 'SB4', 'SB5']
    for name in columns:
        text = product_data[name].iloc[1]
        if not text or text == ['', ''] or text.strip() == '':
            continue
        else:
            text = text.split('\n')

        header = '<div><h1 class="important-header" style="text-align: center;">' + text[0] + '</h1>'
        content = '<p style="font-size: large; text-align: center;">' + text[1] + '</p></div>'
        try:
            img = '<div style="text-align: center;"><img alt="" src="' + product_data[f'{name}Picture'].iloc[0] + '" /></div>'
        except TypeError:
            img = '<div style="text-align: center;"><img alt="" src="" /></div>'

        long_description.append(str(header) + str(content) + str(img))
    long_description.append('</div>')
    long_description = ''.join(long_description)

    start = ''
    if sheet in electrolux_sheets.keys():
        start = electrolux_sheets[sheet]

    tech_description = ['<table id="plan_b" class="data-table"><tbody><tr class="specs_category"><td colspan="2">Specyfikacja</td></tr>']
    columns = keys[keys.index(start):]
    for column in columns:
        value = str(product_data[column].iloc[0])
        if 'None' in value or 'brak' in value:
            continue
        tech_description.append(f'<tr><td class="c_left">{column}</td><td class="c_left">{value}</td></tr>')
    tech_description = ''.join(tech_description)

    return [long_description, short_description, tech_description]
