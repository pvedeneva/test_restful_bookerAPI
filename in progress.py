from helpers import CustomAssertionError
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

assert_response_contains_request_data(response_data, request_data)