from fastapi.testclient import TestClient

from src.main import app

import json

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    request_unexist_user = {
        'email': 'unexist@examp.com'
    }
    response = client.get("/api/v1/user", params=request_unexist_user)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    request_create_user = {
        'name': 'max',
        'email': 'maxim@examp.com'
    }
    response = client. post("/api/v1/user", json=request_create_user)
    assert resoponse.status_code == 201
    assert isinstance(response.json(), int)
    
def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    request_user_existed_enail = {
        'name': 'Already Existed',
        'email': users[0]['email']
    }
    response = client.post("/api/v1/user", json-request_user_existed_email)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}

def test_delete_user():
    '''Удаление пользователя'''
    request_delete_user = {

        'email': users[1]['email'],
    }
    response = client.delete("/api/v1/user", params=request_delete_user)  
    assert response.status_code == 204
# Проверка, что пользователь действительно удалён:
    response_get = client.get("/api/v1/user", params=request_delete_user)
    assert response_get.status_code == 404
    assert response_get.json() == {'detail': 'User not found'}
