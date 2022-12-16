from parsers.functions.get_content import get_content
from parsers.functions.merge_dicts import merge_dicts


def parse_fairy_tail(url: str):
    content = get_content(url)
    ul = content.find('div', {"id": "default-content"}).find('ul', {"class": "editorial"})

    full_names = list()
    images = list()
    appearances = list()
    blank_image = 'https://comicvine.gamespot.com/a/uploads/square_small/11122/111222211/6373148-blank.png'

    for li in ul.find_all('li'):
        appearance = int(li.find('span', {'class': 'further-detail'}).getText())
        if appearance >= 1:
            image_link = li.find('img').get('src')
            if image_link == blank_image:
                continue
            full_names.append(li.find('h3', {'class': 'title'}).getText())
            images.append(image_link)
            appearances.append(appearance)

    characters = {'full_name': full_names, 'image': images, 'appearance': appearances}
    return characters


fairy_tail_url = 'https://comicvine.gamespot.com/fairy-tail/4050-46777/characters/?page='

start_page = 1
end_page = 7
list_of_dicts = list()

for i in range(start_page, end_page + 1):
    fairy_tail_data = parse_fairy_tail(fairy_tail_url + str(i))
    list_of_dicts.append(fairy_tail_data)

keys = ['full_name', 'image', 'appearance']
fairy_tail_characters = merge_dicts(list_of_dicts, keys)
print(fairy_tail_characters)
