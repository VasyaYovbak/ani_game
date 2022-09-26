import pandas as pd

from parsers.functions.get_content import get_content
from parsers.functions.merge_dicts import merge_dicts


def parse_jojo(url):
    content = get_content(url)

    th = content.find('table', {"class": "diamonds"}).find_all('th')[1:]
    full_names = list()
    images = list()

    for th_data in th:
        span = th_data.find('span', {'class', 'fadeout'})
        if not span:
            continue

        a = span.find('a')
        full_names.append(a.get('title'))

        # image parse
        span = th_data.find('span', {'class', 'fadein'})
        image = span.find('a', {'class': 'image'}).get('href')
        images.append(image)
        # full_names.append(li.find('h3', {'class': 'title'}).getText())
        # images.append(li.find('img').get('src'))
    characters = {'full_name': full_names, 'image': images}
    # print(len(full_names) == len(images))
    return characters


def get_jojo_url(part: int):
    return f'https://jojo.fandom.com/wiki/Template:Part_{str(part)}_Character_Table'


start_part = 1
end_part = 6
lst_of_dicts = list()

for i in range(start_part, end_part + 1):
    jojo_data = parse_jojo(get_jojo_url(i))
    lst_of_dicts.append(jojo_data)

keys = ['full_name', 'image']
jojo_data_characters = merge_dicts(lst_of_dicts, keys)
print(jojo_data_characters)
df = pd.DataFrame(jojo_data_characters)
# print(df)
