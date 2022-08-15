import pandas as pd


# Request to website and download HTML contents
from parsers.functions.get_content import get_content


def parse_bleach(url):
    content = get_content(url)

    ul = content.find('div', {"id": "wiki-3025-735-characters"}).find('ul', {"class": "editorial"})
    full_names = list()
    images = list()

    for li in ul.find_all('li'):
        full_names.append(li.find('h3', {'class': 'title'}).getText())
        images.append(li.find('img').get('src'))
    characters = {'full_name': full_names, 'image': images}
    return characters
    # df = pd.dataFrame(characters)
    # return df


bleach_url1 = 'https://www.giantbomb.com/bleach/3025-735/characters/?page=1'
bleach_url2 = 'https://www.giantbomb.com/bleach/3025-735/characters/?page=2'

bleach_characters_1 = parse_bleach(bleach_url1)
bleach_characters_2 = parse_bleach(bleach_url2)

all_bleach_characters = {'full_name': list(), 'image': list()}
for curr in [bleach_characters_1, bleach_characters_2]:
    all_bleach_characters['full_name'] += curr['full_name']
    all_bleach_characters['image'] += curr['image']

print(all_bleach_characters)
df = pd.DataFrame(all_bleach_characters)

# print(df)
