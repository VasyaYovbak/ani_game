import pytest
import requests

from character_view.models import Character
from test_user import login_as_admin, login_as_user
from connection import session
from user_view.models import Achievement

url = 'http://127.0.0.1:2012'


def test_achievements_post():
    access_token = login_as_admin()
    headers = {'Authorization': 'Bearer ' + access_token}
    prev_count_of_data = len(session.query(Achievement).all())
    res = requests.post(url + '/achievements', headers=headers, json=[{
        "name": "test",
        "experience": 20,
        "description": "abc"
    }])
    session.commit()
    new_count_of_data = len(session.query(Achievement).all())
    assert res.status_code == 200 #Okey
    assert new_count_of_data == prev_count_of_data + 1
    res2 = requests.post(url + '/achievements', headers=headers, json=[{
        "name": "test2",
        "asdadsadsadasd": 20,
        "description": "abc"
    }])
    assert res2.status_code == 400  # bad input data
    res3 = requests.post(url + '/achievements', headers=headers, json=[{
        "name": "test",
        "experience": 20,
        "description": "abc"
    }])
    assert res3.status_code == 409  # Achievement already exists
    access_token = login_as_user()
    headers = {'Authorization': 'Bearer ' + access_token}
    res4 = requests.post(url + '/achievements', headers=headers, json=[{
        "name": "test2",
        "experience": 20,
        "description": "abc"
    }])
    assert res4.status_code == 403  # All input data is correct , but user don't have permission


def test_achievements_get():
    res = requests.get(url + '/achievements')
    assert res.status_code == 200 #Okey


def test_achievement_get():
    achievement_id = session.query(Achievement).filter(Achievement.name == "test").first().id
    res = requests.get(url + f'/achievement/{achievement_id}')
    assert res.status_code == 200 #Okey
    res2 = requests.get(url + f'/achievement/100000')
    assert res2.status_code == 400


def test_achievement_put():
    achievement_id = session.query(Achievement).filter(Achievement.name == "test").first().id
    access_token = login_as_admin()
    headers = {'Authorization': 'Bearer ' + access_token}
    res = requests.put(url + f'/achievement/{achievement_id}', headers=headers, json={
        "name": "test",
        "experience": 20,
        "description": "abc"
    })

    assert res.status_code == 200 #Okey
    res2 = requests.put(url + f'/achievement/100000', headers=headers, json={
        "name": "test",
        "experience": 20,
        "description": "abc"
    })

    assert res2.status_code == 404  # Achievement doesn't exist
    res3 = requests.put(url + f'/achievement/{achievement_id}', headers=headers, json={
        "name": "test",
        "sdafafsafsaf": 20,
        "description": "abc"
    })
    assert res3.status_code == 400  # bad input data
    access_token = login_as_user()
    headers = {'Authorization': 'Bearer ' + access_token}
    res = requests.put(url + f'/achievement/{achievement_id}', headers=headers, json={
        "name": "test2",
        "experience": 20,
        "description": "abc"
    })

    assert res.status_code == 403  # All input data is correct , but user don't have permission


def test_achievement_delete():
    achievement_id = session.query(Achievement).filter(Achievement.name == "test").first().id
    access_token = login_as_admin()
    headers = {'Authorization': 'Bearer ' + access_token}
    prev_count_of_data = len(session.query(Achievement).all())
    res = requests.delete(url + f'/achievement/{achievement_id}', headers=headers)
    session.commit()
    new_count_of_data = len(session.query(Achievement).all())
    assert res.status_code == 200 #Okey
    assert new_count_of_data == prev_count_of_data - 1

    res = requests.delete(url + f'/achievement/10000', headers=headers)
    assert res.status_code == 404 # Achievement doesn't exist

    access_token = login_as_user()
    headers = {'Authorization': 'Bearer ' + access_token}
    res = requests.delete(url + f'/achievement/10000', headers=headers)
    assert res.status_code == 403 # All input data is correct , but user don't have permission
