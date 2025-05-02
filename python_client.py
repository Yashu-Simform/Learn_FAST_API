import requests
import asyncio
from getpass import getpass
from email_validator import validate_email

BASE_URL = 'http://127.0.0.1:8000'

def callAPI(p_url, method = 'GET', *args, **kwargs):
    method_map = {
        'GET': requests.get,
        'POST': requests.post,
        'PUT': requests.put,
        'DELETE': requests.delete,
        'PATCH': requests.patch
    }

    req_method = method_map[method]

    get_response = req_method(p_url, *args, **kwargs)

    print(get_response.json())

    return get_response


def getAuthenticate():
    
    password = getpass()

    l_body = {
        'username' : 'worker1',
        'password' : password
    }

    auth_response = callAPI('http://127.0.0.1:8000/auth/', 'POST', json=l_body)
    return auth_response

# def view_teachers_list():

def user_registration():
    username = input('Enter the Username: ')
    email = input('Enter you email address: ')
    try:
        email = validate_email(email).email
    except Exception as e:
        print('Got error: ', e)

    password = input(
        '''Enter password:
            [Password must contain at least 1 Uppercase, 1 Lowercase and 1 special character.]
        '''
        )
    first_name = input('Enter first name: ')
    last_name = input('Enter last name: ')

    req_body = {
        "username": username,
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name
    }
    print(req_body)

    res = callAPI(f'{BASE_URL}/user/register/', 'POST', json=req_body)
    print(res)


def update_client_data():
    update_data = {
        "email": "yashu.ranparia@simformsolutions.com",
        "name": "Yashu",
        "password": "********",
        "username": "@yashu123"
        }
    
    res = callAPI('http://127.0.0.1:8000/update/client/0', 'PUT', json=update_data)
    print(res)


def main():
    # body = {
    #     'client':{
    #         'username': '@yashu1',
    #         'email': 'yashu1@gmail.com',
    #         'password': 'yashu1@123',
    #         'name': 'yashu'
    #     },
    #     'account_type': 'savings'
    # }
    # callAPI(f'{BASE_URL}/create/client/', 'POST', json=body)

    # user_registration()
    update_client_data()

main()

# asyncio.run(main())