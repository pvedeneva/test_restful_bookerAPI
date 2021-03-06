"""file for storing fixtures"""
import pytest
import config
import json
import requests
from tests.helpers import CustomAssertionError

# token fixture
"""headers = {
    'Content-Type': 'application/json'
}

token_credentials = json.dumps({
    "username": config.USER,
    "password": config.PASSW
})

update_header = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'

}"""

#TODO функция которая заполняет update_header
#TODO возможно добавить это в фикстуру
def add_token_to_update_header(token):
    return json.dumps({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Cookie': f'token={token}'
    })


@pytest.fixture(scope="session") #token 2b0b91d3ad3bb7d
def header_with_token(request):
    '''get auth token fixture
    return --> token string'''
    r = requests.post(f'{config.BASE_URL}/auth', data = config.token_credentials, headers = config.headers)
    auth_token = r.json()['token']
    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Cookie': f'token={auth_token}'
    }

#TODO добавить Basic аутентификацию

@pytest.fixture(scope="class")
def booking_lifecycle(request, header_with_token):
    '''delete used booking fixture
    auth creds = token in header'''
    # tests is executed here
    r = requests.post(f'{config.BASE_URL}/booking', data = config.booking_data, headers = config.headers)
    booking_id = r.json()['bookingid']
    yield booking_id
    r = requests.delete(f'{config.BASE_URL}/booking/{booking_id}', headers = header_with_token)
    print('booking deleted')

@pytest.fixture()
def create_booking(request):
    '''create booking fixture'''
    r = requests.post(f'{config.BASE_URL}/booking', data = config.booking_data, headers = config.headers)
    booking_id = r.json()['bookingid']
    return booking_id


#TODO зачем это здесь!!
request_data = {
    "firstname": "Harry",
    "lastname": "Potter",
    "totalprice": 100,
    "depositpaid": False,
    "bookingdates": {
        "checkin": "2025-03-02",
        "checkout": "2025-03-15"
    },
    "additionalneeds": "Dobby`s assistance"
}

response_data = {
    "firstname": "Harry",
    "lastname": "Potter",
    "totalprice": 200,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2026-03-02",
        "checkout": "2025-03-15"
    },
    "additionalneeds": "Dobby`s assistance"
}




















# OTHER TRIED FIXTURES
@pytest.fixture()
def create_booking(request):
    '''create booking fixture'''
    r = requests.post(f'{config.BASE_URL}/booking', data = config.booking_data, headers = headers)
    booking_id = r.json()['bookingid']
    return booking_id

header_with_tokendelete_body = {
    'Content-Type': 'application/json',
    'Cookie': 'token=2b0b91d3ad3bb7d'
}


@pytest.fixture() #input request&bookingId 2677
def delete_booking(request, booking_id):
    yield
    r = requests.delete(f'{config.BASE_URL}/booking/{booking_id}', headers = delete_body)
    print(r.text)
    print(r.status_code)

def foo_token():
    '''get auth token fixture
    return --> token string'''
    r = requests.post(f'{config.BASE_URL}/auth', data = token_credentials, headers = headers)
    auth_token = r.json()['token']
    return auth_token

def foo_add_token_to_undate_header():
    return json.dumps({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Cookie': f'token={foo_token()}'
    })


"""@pytest.fixture(scope="class")
def booking_lifecycle(request, token):
    '''delete used booking fixture
    auth creds = token in header'''
    # tests is executed here
    delete_body = {
        'Content-Type': 'application/json',
        'Cookie': f'token={token}'
    }
    r = requests.post(f'{config.BASE_URL}/booking', data = config.booking_data, headers = headers)
    booking_id = r.json()['bookingid']
    yield booking_id
    r = requests.delete(f'{config.BASE_URL}/booking/{booking_id}', headers = delete_body)
    print('booking deleted')
"""
"""res_data = {"bookingdates": {
        "checkin": "2026-03-02",
        "checkout": "2025-03-15"
    }}

req_data = {"bookingdates": {
        "checkin": "2026-03-02",
        "checkout": "2027-03-15"
    }}
#print(assert_response_contains_request_data(res_data, req_data))
"""
"""

def assert_response_contains_request_data(response_data, request_data):
    '''Custom assert to check if all fields in answer equals to fields in request'''
    # TODO доделать кастоный ассерт
    for key in request_data:
        compare_values(key, response_data[key], request_data[key])
    return True"""