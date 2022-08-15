from parsers.functions.get_content import get_content


def parse_one_punch(url):
    content = get_content(url)

    full_names = list()
    images = list()
    tables = content.find('div', {'class', 'wds-tab__content wds-is-current'}).find_all(
        'table')
    for table in tables:
        inner_tables = table.find_all('table')
        for inner_table in inner_tables:
            div = inner_table.find('div').find('div', {'class': 'floatnone'})
            a = div.find('a')
            full_name = a.get('title')
            full_names.append(full_name)
            image = a.find('img').get('src')
            images.append(image)
    return {'full_name': full_names, 'image': images}


one_punch_url = 'https://onepunchman.fandom.com/wiki/Characters'
one_punch_data = parse_one_punch(one_punch_url)
print(one_punch_data)
# df = pd.DataFrame(one_punch_data)
# print(df)
