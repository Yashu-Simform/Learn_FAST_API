import requests
import asyncio
from getpass import getpass

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

def main():
    BASE_URL = 'http://127.0.0.1:8000'
    body = {
        'client':{
            'username': '@yashu1',
            'email': 'yashu1@gmail.com',
            'password': 'yashu1@123',
            'name': 'yashu'
        },
        'account_type': 'savings'
    }
    callAPI(f'{BASE_URL}/create/client/', 'POST', json=body)

main()

# asyncio.run(main())