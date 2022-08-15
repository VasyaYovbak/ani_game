from parsers.functions.get_content import get_content
from parsers.functions.merge_dicts import merge_dicts
from parsers.one_piece.data.raw_data import keys


def parse_one_piece(url):
    content = get_content(url)

    ul = content.find('div', {"id": "site"}).find('ul', {"class": "editorial"})

    full_names = list()
    images = list()
    appearances = list()

    for li in ul.find_all('li'):
        appearance = int(li.find('span', {'class': 'further-detail'}).getText())
        if appearance >= 5:
            full_names.append(li.find('h3', {'class': 'title'}).getText())
            images.append(li.find('img').get('src'))
            appearances.append(appearance)

    characters = {'full_name': full_names, 'image': images, 'appearance': appearances}
    return characters


# I do not recommend to run more than 10 pages(if you have a lot of pages it is better to use multi threads)
one_piece_url = 'https://comicvine.gamespot.com/one-piece/4050-21397/characters/?page='
starting_page = 10
ending_page = 20
lst_of_dicts = list()

for i in range(starting_page, ending_page + 1):
    one_piece_data = parse_one_piece(one_piece_url + str(i))
    lst_of_dicts.append(one_piece_data)

one_piece_characters = merge_dicts(lst_of_dicts, keys)
print(one_piece_characters)
