import json
import heapq
BASE_URL = 'https://restful-booker.herokuapp.com'
USER = 'admin'
PASSW = 'password123'


def list_booking_ids(response):
    list_of_ids = []
    for item in response:
        list_of_ids.append(item['bookingid'])
    return list_of_ids


def nonexistent_id_generator(response):
    valid_id = list_booking_ids(response)
    nonexistent_id = max(valid_id) + 1

    return nonexistent_id


headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

booking_data = json.dumps({
    "firstname": "Harry",
    "lastname": "Potter",
    "totalprice": 100,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2025-03-02",
        "checkout": "2025-03-15"
    },
    "additionalneeds": "Dobby`s assistance"
})

booking_data_without_name = json.dumps({
    "lastname": "Potter",
    "totalprice": 100,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2025-03-02",
        "checkout": "2025-03-15"
    },
    "additionalneeds": "Dobby`s assistance"
})

booking_data_invalid_schema = json.dumps({
    "firstname": "Harry",
    "lastname": "Potter",
    "totalprice": 100,
    "depositpaid": True,
    "checkin": "2025-03-02",
    "checkout": "2025-03-15",
    "additionalneeds": "Dobby`s assistance"
})

booking_data_missing_in_schema = json.dumps({
    "lastname": "Potter",
    "totalprice": 100,
    "depositpaid": True,
    "bookingdates":{
        "checkin": "2025-03-02",
        "": "2025-03-15"
    },
    "additionalneeds": "Dobby`s assistance"
})

booking_data_with_no_additional = json.dumps({
    "firstname": "Harry",
    "lastname": "Potter",
    "totalprice": 100,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2025-03-02",
        "checkout": "2025-03-15"
    },
})

booking_data_chech_out_b4_check_in = booking_data_equal_dates = json.dumps({
    "firstname": "Harry",
    "lastname": "Potter",
    "totalprice": 100,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2025-03-15",
        "checkout": "2025-03-12"
    },
})

booking_data_equal_dates = json.dumps({
    "firstname": "Harry",
    "lastname": "Potter",
    "totalprice": 100,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2025-03-15",
        "checkout": "2025-03-15"
    },
})


invalid_check_in_format_dates = ["2025/03/02", "02-03-2025", "02/03/2025", "02-03-25",
"02/03/25", "03-02-2025", "03/02/2025", "03-02-25", "03/02/25"]

invalid_check_out_format_dates = ["2025/03/15", "15-03-2025", "15/03/2025", "15-03-25",
"15/03/25", "03-15-2025", "03/15/2025", "03-15-25", "03/15/25"]

# UPDATE DATA
update_data_change_dates = json.dumps({
    "firstname": "Harry",
    "lastname": "Potter",
    "totalprice": 100,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2025-04-02",
        "checkout": "2025-04-15"
    },
})

update_additional = json.dumps({
    "firstname": "Harry",
    "lastname": "Potter",
    "totalprice": 100,
    "depositpaid": True,
    "bookingdates":{
        "checkin": "2025-03-02",
        "checkout": "2025-03-15"
    },
    "additionalneeds": "Invisibility cloak"
})

update_all_booking_data = json.dumps({
    "firstname": "Tom",
    "lastname": "Riddle",
    "totalprice": 500,
    "depositpaid": False,
    "bookingdates": {
        "checkin": "2024-05-05",
        "checkout": "2024-05-25"
    },
})

update_unvalid_dates = json.dumps({
    "firstname": "Harry",
    "lastname": "Potter",
    "totalprice": 100,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2025-04-02",
        "checkout": "2025-04-01"
    },
})


update_dates_in_past = json.dumps({
    "firstname": "Harry",
    "lastname": "Potter",
    "totalprice": 100,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2018-04-02",
        "checkout": "2018-04-15"
    },
})

# PARTIAL UPDATE
"""part_upd_dates_data = json.dumps({
    "bookingdates": {
        "checkin": "2026-04-03",
        "checkout": "2026-04-16"
}}) # +1 to each field"""


part_upd_dates_data = [json.dumps(item) for item in [{"bookingdates": {"checkin": "2026-04-03"}},
                                                    {"bookingdates": {"checkout": "2026-04-16"}},
                                                    {"bookingdates": {"checkin": "2027-04-03", "checkout": "2027-04-16"}}]]

part_upd_fields = [json.dumps(item) for item in [{"firstname": "CustomHarry"}, {"lastname": "Custom Potter"}, {"totalprice": 200},
                    {"depositpaid": False}, {"additionalneeds": "Invisibility cloak"}]]

