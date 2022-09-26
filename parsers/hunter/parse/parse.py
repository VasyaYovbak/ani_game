from collections import defaultdict

from parsers.functions.get_content import get_content


def parse_hunter(url):
    content = get_content(url)

    full_names = list()
    images = list()
    empty = 'https://static.wikia.nocookie.net/hunterxhunter/images/e/ec/Unseen_Character_Portrait.png/revision/latest/scale-to-width-down/130?cb=20191018055944'
    for table in content.find_all('table', {'id': 'w'}):
        for td in table.find_all('td', {'width': '20%'}):
            if td.find('img', {"class": "lazyload"}) is not None:
                if ("???" not in td.find('td', {"class": "headerbackground"}).find('span').getText()) and \
                        ((td.find('img', {"class": "lazyload"}).get('data-src')) != empty):
                    images.append(td.find('img', {"class": "lazyload"}).get('data-src'))
                    full_names.append(td.find('td', {"class": "headerbackground"}).find('span').getText())

    characters = {'full_name': full_names, 'image': images}
    return characters


hunter_url = 'https://hunterxhunter.fandom.com/wiki/List_of_Hunter_%C3%97_Hunter_Characters'

raw_hunter_characters = parse_hunter(hunter_url)
cleaned_hunter_characters = {'full_name': list(), 'image': list()}

for curr in [raw_hunter_characters]:
    cleaned_hunter_characters['full_name'] += curr['full_name']
    cleaned_hunter_characters['image'] += curr['image']

cleaned_hunter_characters = zip(cleaned_hunter_characters['full_name'], cleaned_hunter_characters['image'])

complete = defaultdict()
for key, value in cleaned_hunter_characters:
    complete[key] = value

all_hunter_characters = {'full_name': complete.keys(), 'image': complete.values()}
print(all_hunter_characters)
