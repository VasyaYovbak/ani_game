import requests

from character_view.models import Character
from tests.test_user.test_user import login_as_admin, login_as_user
from connection import session

url = 'http://127.0.0.1:2012'

access_token = ''


def test_characters_post():
    access_token = login_as_admin()
    headers = {'Authorization': 'Bearer ' + access_token}
    prev_count_of_data = len(session.query(Character).all())
    res = requests.post(url + '/characters', headers=headers, json=[{
        "name": "test",
        "is_alive": True,
        "is_good": True,
        "image": "bla"}])
    session.commit()
    new_count_of_data = len(session.query(Character).all())
    assert res.status_code == 200 #Okey
    assert new_count_of_data == prev_count_of_data + 1
    res2 = requests.post(url + '/characters', headers=headers, json=[{
        "name": "test",
        "is_alive": True,
        "asdsadsadsa": True,
        "asdsad": "bla"}])
    assert res2.status_code == 400  # bad input data
    res3 = requests.post(url + '/characters', headers=headers, json=[{
        "name": "test",
        "is_alive": True,
        "is_good": True,
        "image": "bla"}])
    assert res3.status_code == 409  # Character already exists
    access_token = login_as_user()
    headers = {'Authorization': 'Bearer ' + access_token}
    res4 = requests.post(url + '/characters', headers=headers, json=[{
        "name": "Naruto",
        "is_alive": True,
        "is_good": True,
        "image": "bla"}])
    assert res4.status_code == 403  # All input data is correct , but user don't have permission


def test_characters_get():
    res = requests.get(url + '/characters')
    assert res.status_code == 200


def test_character_get():
    character_id = session.query(Character).filter(Character.name == "test").first().character_id
    res = requests.get(url + f'/character/{character_id}')
    assert res.status_code == 200
    res2 = requests.get(url + f'/character/100000')
    assert res2.status_code == 400


def test_characters_put():
    character_id = session.query(Character).filter(Character.name == "test").first().character_id
    access_token = login_as_admin()
    headers = {'Authorization': 'Bearer ' + access_token}
    res = requests.put(url + f'/character/{character_id}', headers=headers, json={
        "name": "lol",
        "is_alive": True,
        "is_good": True,
        "image": "bla"})

    assert res.status_code == 200
    res2 = requests.put(url + f'/character/100000', headers=headers, json={
        "name": "lol",
        "is_alive": True,
        "is_good": True,
        "image": "bla"})

    assert res2.status_code == 404  # Character doesn't exist
    res3 = requests.put(url + f'/character/{character_id}', headers=headers, json={
        "name": "lol",
        "adsadasd": True,
        "asdadsa": True,
        "image": "bla"})
    assert res3.status_code == 400  # bad input data
    access_token = login_as_user()
    headers = {'Authorization': 'Bearer ' + access_token}
    res = requests.put(url + f'/character/{character_id}', headers=headers, json={
        "name": "lol",
        "is_alive": True,
        "is_good": True,
        "image": "bla"})

    assert res.status_code == 403  # All input data is correct , but user don't have permission


def test_character_delete():
    character_id = session.query(Character).filter(Character.name == "test").first().character_id
    access_token = login_as_admin()
    headers = {'Authorization': 'Bearer ' + access_token}
    prev_count_of_data = len(session.query(Character).all())
    res = requests.delete(url + f'/character/{character_id}', headers=headers)
    session.commit()
    new_count_of_data = len(session.query(Character).all())
    assert res.status_code == 200
    assert new_count_of_data == prev_count_of_data - 1

    res = requests.delete(url + f'/character/10000', headers=headers)
    assert res.status_code == 404

    access_token = login_as_user()
    headers = {'Authorization': 'Bearer ' + access_token}
    res = requests.delete(url + f'/character/10000', headers=headers)
    assert res.status_code == 403
