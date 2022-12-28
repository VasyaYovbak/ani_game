from parsers.functions.get_content import get_content


def parse_my_hero_academia(url: str):
    content = get_content(url)
    characters_lists = content.find('main').find('div', {'id': 'content'}).find_all('div', {'class': 'chargallery'})
    full_names = list()
    images = list()
    no_image_available = 'https://static.wikia.nocookie.net/bokunoheroacademia/images/d/d5/NoPicAvailable.png/revision/latest/scale-to-width-down/135?cb=20160326222204'
    for character_list in characters_lists:
        character_div = character_list.find_all('div', {'class', 'wikia-gallery-item'})
        for character_info in character_div:
            a = character_info.find('div', {'class', 'lightbox-caption'}).find('div',
                                                                               {'class': 'chargallery-profile-caption'})
            img = character_info.find('div', {'class': 'thumb'}).find('a').find('img')

            full_name = a.getText()
            image = img.get('src')
            if full_name == '????' or image == no_image_available:
                continue

            full_names.append(full_name)
            images.append(image)
    return {'full_name': full_names, 'image': images}


my_hero_academia_url = 'https://myheroacademia.fandom.com/wiki/List_of_Characters'
my_hero_academia_characters = parse_my_hero_academia(my_hero_academia_url)
print(my_hero_academia_characters)
