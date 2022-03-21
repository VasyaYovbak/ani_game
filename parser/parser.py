import requests
from character_view.models import Character
from connection import engine
from sqlalchemy.orm import Session

from bs4 import BeautifulSoup

f = open("styles.txt", 'r', encoding="utf8")

lines = f.read().split('\n')
characters_background = dict()
i = 1
prev = ''
for line in lines:
    if i % 4 == 1:
        prev = line.split()[0][1:]
    if i % 4 == 2:
        characters_background[prev] = line[4:]
    i += 1

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
}

r = requests.get('https://jut.su/ninja', headers=headers)
soup = BeautifulSoup(r.text)
character_ul = soup.find('ul', {'class': "ninja_list"})
character_li_list = character_ul.find_all('li')
characters = []
session = Session(bind=engine)
for character_li in character_li_list:
    try:
        character = dict()
        character['name'] = character_li.find('a').attrs['href'].split('/')[2].replace('_', ' ')
        if character['name'].find('%') != -1:
            character['name'] = character_li.find('span').get_text()
        character['image'] = characters_background[character_li.find('div').attrs['class'][1]].split(':')[1]
        table_character = Character(**character)
        print(table_character)
        session.add(table_character)
    except:
        pass

session.commit()

