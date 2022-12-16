from parsers.functions.get_content import get_content
from parsers.functions.merge_dicts import merge_dicts


def parse_attack_on_titan(url: str):
    content = get_content(url)
    ul = content.find('div', {"id": "default-content"}).find('ul', {"class": "editorial"})

    full_names = list()
    images = list()
    appearances = list()
    blank_image = 'https://comicvine.gamespot.com/a/uploads/square_small/11122/111222211/6373148-blank.png'

    for li in ul.find_all('li'):
        appearance = int(li.find('span', {'class': 'further-detail'}).getText())
        if appearance >= 2:
            image_link = li.find('img').get('src')
            if image_link == blank_image:
                continue
            full_names.append(li.find('h3', {'class': 'title'}).getText())
            images.append(image_link)
            appearances.append(appearance)

    characters = {'full_name': full_names, 'image': images, 'appearance': appearances}
    return characters

    # table = content.find('div', {"id": "content"}).find('table', {"id": 'toc'})
    # # print(table)
    #
    # for character_list in content.find_all('div', {"class": "characterbox-container"}):
    #     # print(character_list)
    #     character_table = character_list.find('table', {'class': 'characterbox'})
    #
    #     print(character_table)
    #
    #     # td = character_table.find('td')
    #     # td_div = td.find('div')
    #     # a = td_div.find('a')
    #     # print(a)
    #     # # print(td)
    #     # a = td.get('a')
    #     # print(a)
    #     # img = td.find('img')
    #     # image_link = img.get('data-src')
    #     # print(image_link)
    #     # # character_name = a.getText()
    #     # # print(character_name)
    # # print(content)


attack_on_titan_url = 'https://comicvine.gamespot.com/attack-on-titan/4075-345/characters?page='
start_page = 1
end_page = 3
list_of_dicts = list()

for i in range(start_page, end_page + 1):
    attack_on_titan_data = parse_attack_on_titan(attack_on_titan_url + str(i))
    list_of_dicts.append(attack_on_titan_data)

keys = ['full_name', 'image', 'appearance']
attack_on_titan_characters = merge_dicts(list_of_dicts, keys)
print(attack_on_titan_characters)
