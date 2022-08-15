from parsers.functions.setup import *

from parsers.functions.get_content import get_content
from parsers.functions.merge_dicts import merge_dicts


def parse_dragon_ball(url):
    content = get_content(url)

    ul = content.find('div', {"id": "default-content"}).find('ul', {"class": "editorial"})

    full_names = list()
    images = list()
    appearances = list()

    for li in ul.find_all('li'):
        appearance = int(li.find('span', {'class': 'further-detail'}).getText())
        if appearance >= 0:
            full_names.append(li.find('h3', {'class': 'title'}).getText())
            images.append(li.find('img').get('src'))
            appearances.append(appearance)

    characters = {'full_name': full_names, 'image': images, 'appearance': appearances}
    return characters


# I do not recommend to run more than 10 pages(if you have a lot of pages it is better to use multi threads)
dragon_ball_url = 'https://comicvine.gamespot.com/dragon-ball-super/4075-581/characters/?page='
starting_page = 1
ending_page = 6
lst_of_dicts = list()

for i in range(starting_page, ending_page + 1):
    dragon_ball_data = parse_dragon_ball(dragon_ball_url + str(i))
    lst_of_dicts.append(dragon_ball_data)


keys = ['full_name', 'image', 'appearance']
dragon_ball_characters = merge_dicts(lst_of_dicts, keys)
print(dragon_ball_characters)
df = pd.DataFrame(dragon_ball_characters)
print(df)


