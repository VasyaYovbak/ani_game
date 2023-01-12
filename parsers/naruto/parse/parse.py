import pandas as pd

from parsers.functions.get_content import get_content
from parsers.functions.merge_dicts import merge_dicts


def parse_naruto_characters(url: str):
    content = get_content(url)
    ul = content.find('div', {"id": "default-content"}).find('ul', {"class": "editorial"})

    full_names = list()
    images = list()
    appearances = list()

    for li in ul.find_all('li'):
        appearance = int(li.find('span', {'class': 'further-detail'}).getText())
        if appearance >= 4:
            image_link = li.find('img').get('src')
            full_names.append(li.find('h3', {'class': 'title'}).getText())
            images.append(image_link)
            appearances.append(appearance)

    characters = {'full_name': full_names, 'image': images, 'appearance': appearances}
    return characters


def get_naruto_url(part: int):
    return f'https://comicvine.gamespot.com/naruto/4050-34585/characters/?page={part}'


start_part = 1
end_part = 6
lst_of_dicts = list()

for i in range(start_part, end_part + 1):
    jojo_data = parse_naruto_characters(get_naruto_url(i))
    lst_of_dicts.append(jojo_data)

keys = ['full_name', 'image', 'appearance']
naruto_characters = merge_dicts(lst_of_dicts, keys)
print(naruto_characters)
