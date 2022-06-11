from tests.helpers import CustomAssertionError
import json

def assert_response_contains_request_data(response_data, request_data):
    '''Custom assert to check if all fields in answer equals to fields in request'''
    results = [] # записыать все что не пустое
    for key in request_data:
        if request_data[key] != response_data[key]:
            results.append(f'CustomAssertionError {key} - {request_data[key]} not in response, {response_data[key]} instead')
    # TODO может тут захреначить обработку исключений
    if results:
        raise CustomAssertionError(*results)
        #return results # хрень т.к. не пустой список также true
    else:
        return True

response_data = {
    "firstname": "Harry",
    "lastname": "Potter",
    "totalprice": 100,
    "depositpaid": True,
    "bookingdates":
        {"checkin": "2026-03-15",
        "checkout": "2025-03-15"}}

request_data = {
    "firstname": "Ron",
    "lastname": "Potter",
    "totalprice": 200,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2025-03-15",
        "checkout": "2025-03-15",
    }}

#assert_response_contains_request_data(response_data, request_data)

part_upd_fields = [json.dumps(item) for item in [{"firstname": "Harry"}, {"lastname": "Potter"}, {"totalprice": 100},
                    {"depositpaid": True},{"checkin": "2025-03-02"},
                    {"checkout": "2025-03-15"}, {"additionalneeds": "Invisibility cloak"}]]

#print(part_upd_fields)

all = {'b' : {1:'a', 2 : 'b'}}
booking1 = {'b' : {1:'a'}}
all_2 = {'b' : {1:'a', 2 : 'b'}}
#print(list(all['b'].items()))
#print(list(booking1['b'].items()))

all_b = list(all['b'].items())
part_b = list(booking1['b'].items())
all_2_b = list(all['b'].items())

print(all_b)
print(part_b)
print(all_2_b)

def booking_dates_validator(request, response, results):
    for date in request:
        if date in response:
            continue
        else:
            results.append(f'{date} not in response')


if all_2_b[0] in all_b:
    print('true')
else:
    print('f')

# нужен универсальный способ для всех вариант дат



#print(booking1.values() in all.values())