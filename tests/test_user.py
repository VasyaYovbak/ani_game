import pytest
import requests
from sqlalchemy import desc

from connection import session
from user_view.models import User, TokenBlocklist

url = 'http://127.0.0.1:2012'


def login_as_admin():
    res = requests.post(url + '/login', json={"email": "vasa23102003@gmail.com", "password": "123"})
    access_token = res.json()["access_token"]
    return access_token


def login_as_user():
    res = requests.post(url + '/login', json={"email": "vasavasavasa", "password": "123"})
    access_token = res.json()["access_token"]
    return access_token


def test_register():
    prev_count_of_user = len(session.query(User).all())
    res = requests.post(url + '/registration', json={
        "username": "test",
        "email": "test",
        "password": "test"
    })
    session.commit()
    new_count_of_user = len(session.query(User).all())
    assert res.status_code == 200  # Okey
    assert new_count_of_user == prev_count_of_user + 1

    res2 = requests.post(url + '/registration', json={
        "username": "test",
        "email": "test",
        "password": "test"
    })
    assert res2.status_code == 409  # User already registered

    res3 = requests.post(url + '/registration', json={
        "KTO": "test",
        "emailasdadsad": "test",
        "sadsadasd": "test"
    })
    assert res3.status_code == 400  # Wrong registration input

    access_token = login_as_admin()
    headers = {'Authorization': 'Bearer ' + access_token}
    res4 = requests.post(url + '/registration', headers=headers, json={
        "username": "test",
        "email": "test",
        "password": "test"
    })
    assert res4.status_code == 405  # Sorry, you can't register now. Please first logout


def test_login():
    res = requests.post(url + '/login', json={
        "email": "test",
        "password": "test"
    })
    assert res.status_code == 200
    res2 = requests.post(url + '/login', json={
        "email": "testaaaa",
        "password": "test"
    })
    assert res2.status_code == 403  # wrong email or password

    res3 = requests.post(url + '/login', json={
        "emailLLLLLLL": "test",
        "passwordDDDDD": "test"
    })
    assert res3.status_code == 400  # Wrong input data

    access_token = login_as_admin()
    headers = {'Authorization': 'Bearer ' + access_token}
    res4 = requests.post(url + '/login', headers=headers, json={
        "email": "test",
        "password": "test"
    })
    assert res4.status_code == 405  # Sorry, you can't register now. Please first logout"


def test_logout():
    access_token = login_as_admin()
    headers = {'Authorization': 'Bearer ' + access_token}
    res = requests.post(url + '/logout', headers=headers)
    assert res.status_code == 200  # token successfuly banned

    res2 = requests.post(url + '/logout', headers=headers)
    assert res2.status_code == 401  # Token already in ban list

    res3 = requests.post(url + '/characters', headers=headers, json=[{
        "name": "test",
        "is_alive": True,
        "is_good": True,
        "image": "bla"}])
    assert res3.status_code == 401  # Can't add character becouse this token in ban list


def test_profile():
    res = requests.get(url + '/profile/2')
    assert res.status_code == 200
    res = requests.get(url + '/profile/100')
    assert res.status_code == 404
    after_test_clear()


def after_test_clear():
    user = session.query(User).filter(User.email == "test").first()
    session.delete(user)
    session.commit()

