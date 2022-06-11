import requests
import config


class CustomAssertionError(Exception):
    pass


# CUSTOM ASSERTIONS
def booking_dates_assert(request, response, results):
    """Search dates from request in responce"""
    for date in request:
        if request[date] == response[date]:
            continue
        else:
            results.append(f'{date} - {request[date]} not in response')

def assert_response_contains_request_data(response_data, request_data):
    """Custom assert for UpdateBooking and PartialUpdate
    to check if all fields in answer equals to fields in request"""
    results = [] # track non-empty fields
    for key in request_data:
        if key == 'bookingdates': # case w check in
            request_check = request_data['bookingdates']
            response_check = response_data['bookingdates']
            booking_dates_assert(request_check, response_check, results)
            continue
        if request_data[key] != response_data[key]:
            results.append(f'{key} - {request_data[key]} not in response')
    if results:
        raise CustomAssertionError(*results)
    else:
        return True


def assert_delete_successful(booking_id):
    "Get deleted booking"
    r = requests.get(f'{config.BASE_URL}/booking/{booking_id}')
    print(r.text)
    print(r.status_code)
    if r.status_code == 404 and r.text == 'Not Found':
        return True
    else:
        raise CustomAssertionError(f'{r.status_code} and {r.text} != 404 and Not Found')
