import requests
import config
import pytest
import json
import os
from schema_assertion_helper import assert_booking_schema
from conftest import assert_response_contains_request_data



@pytest.mark.skip
class TestGetBooking:
    def test_get_all_booking_ids(self, booking_lifecycle):
        r = requests.get(f'{config.BASE_URL}/booking')
        assert booking_lifecycle in config.list_booking_ids(r.json())
        assert r.status_code == 200, 'All bookings request failed'

    def test_get_booking_by_id(self,booking_lifecycle):
        '''create booking --> booking_id'''
        r = requests.get(f'{config.BASE_URL}/booking/{booking_lifecycle}')

        assert r.status_code == 200, 'Booking by id not found with method GetBooking'

    def test_get_bookings_by_lastname(self, booking_lifecycle):
        r = requests.get(f'{config.BASE_URL}/booking?lastname=Potter')
        assert booking_lifecycle in config.list_booking_ids(r.json())
        assert r.status_code == 200, 'Booking by lastname not found with method GetBooking'

    def test_get_bookings_by_fullname(self, booking_lifecycle):
        r = requests.get(f'{config.BASE_URL}/booking?lastname=Potter&firstname=Harry')
        assert booking_lifecycle in config.list_booking_ids(r.json())
        assert r.status_code == 200, 'Booking by fullname not found with method GetBooking'

    def test_get_bookings_by_check_in(self, booking_lifecycle):
        r = requests.get(f'{config.BASE_URL}/booking?checkin=2025-03-02')
        assert booking_lifecycle in config.list_booking_ids(r.json()), 'Booking id is not ' \
                                                                       'present in GetBooking by check in'
        assert r.status_code == 200, 'Booking by check_in not found with method GetBooking'

    def test_get_bookings_by_check_out(self, booking_lifecycle):
        r = requests.get(f'{config.BASE_URL}/booking?checkout=2025-03-15')
        assert booking_lifecycle in config.list_booking_ids(r.json()), 'Booking id is not ' \
                                                                       'present in GetBooking by check out'
        assert r.status_code == 200, 'Booking by check_out not found with method GetBooking'

    def test_get_bookings_by_both_checkdates(self, booking_lifecycle):
        r = requests.get(f'{config.BASE_URL}/booking?checkin=2025-03-02&checkout=2025-03-15')

        assert booking_lifecycle in config.list_booking_ids(r.json()), 'Booking id is not ' \
                                                                       'present in GetBooking by check out and in'
        assert r.status_code == 200, 'Booking by check_out not found with method GetBooking'

    def test_get_non_existant_booking(self):
        r = requests.get(f'{config.BASE_URL}/booking?lastname=Potter&firstname=HarryJames')

        assert  r.json() == [], 'Found non-existant booking'
        assert r.status_code == 200, 'Not 200 in non-existant booking search'

    def test_get_booking_inside_check_in_boundary(self, booking_lifecycle):
        """Check if booking is in result with earlier check in date < (2025-03-01)"""
        r = requests.get(f'{config.BASE_URL}/booking?checkin=2025-03-01')

        assert  booking_lifecycle in config.list_booking_ids(r.json()), 'Booking not found inside check_in - 1 boundary'
        assert r.status_code == 200, 'Not 200 in check_in - 1 boundary request'

    def test_get_booking_inside_check_out_boundary(self, booking_lifecycle):
        """Check if booking is in result with earlier check out date < (2025-03-15)"""
        r = requests.get(f'{config.BASE_URL}/booking?checkout=2025-01-14')

        assert  booking_lifecycle in config.list_booking_ids(r.json()), 'Booking not found inside check_ot - 1 boundary'
        assert r.status_code == 200, 'Not 200 in check_out - 1 boundary request'

    def test_get_booking_by_invalid_check_in(self, booking_lifecycle):
        """Check if booking is NOT in result with later check in date > (2025-03-02)"""
        r = requests.get(f'{config.BASE_URL}/booking?checkin=2025-03-03')

        assert  booking_lifecycle not in config.list_booking_ids(r.json()), 'Found booking with invalid check_in date'
        assert r.status_code == 200, 'Not 200 in invalid check_in date'

    def test_get_booking_by_invalid_check_out(self, booking_lifecycle):
        """Check if booking is NOT in result with later check out date > (2025-03-15)"""
        r = requests.get(f'{config.BASE_URL}/booking?checkout=2025-01-16')

        assert  booking_lifecycle not in config.list_booking_ids(r.json()), 'Found booking with invalid check_out date'
        assert r.status_code == 200, 'Not 200 in invalid check_in date'

    def test_get_by_invalid_check_dates(self, booking_lifecycle):
        r = requests.get(f'{config.BASE_URL}/booking?checkin=2025-03-03&checkout=2025-01-16')

        assert booking_lifecycle not in config.list_booking_ids(r.json()), 'Found booking with invalid dates pair'
        assert r.status_code == 200, 'Not 200 in invalid check date pair'


    @pytest.mark.parametrize("invalid_id", [0, -1, 'id'])
    def test_get_booking_by_invalid_id(self, invalid_id):
        '''create booking --> booking_id'''
        r = requests.get(f'{config.BASE_URL}/booking/{invalid_id}')
        assert r.status_code == 404, 'Found booking with invalid id'

    def test_get_booking_by_nonexistent_id(self):
        '''create booking --> booking_id'''
        r = requests.get(f'{config.BASE_URL}/booking')
        nonexistent_id = config.nonexistent_id_generator(r.json())
        r2 = requests.get(f'{config.BASE_URL}/booking/{nonexistent_id}')

        assert r2.status_code == 404, 'Found booking with invalid id'

    @pytest.mark.parametrize("date_format", config.invalid_check_in_format_dates) # (2025-03-02)
    def test_invalid_check_in_format(self, booking_lifecycle, date_format):
        r = requests.get(f'{config.BASE_URL}/booking?checkin={date_format}')

        assert r.status_code == 422, 'Found booking by invalid check in date format'

    @pytest.mark.parametrize("date_format", config.invalid_check_out_format_dates) # (2025-03-15)
    def test_invalid_check_out_format(self, booking_lifecycle, date_format):
        r = requests.get(f'{config.BASE_URL}/booking?checkout={date_format}')

        assert r.status_code == 422, 'Found booking by invalid check out date format'


@pytest.mark.skip
class TestCreateBooking:
    """test booking creation"""
    def test_create_booking(self):
        r = requests.post(f'{config.BASE_URL}/booking', data=config.booking_data, headers=config.headers)

        assert r.status_code == 200, 'Booking is not created'

    def test_create_booking_without_mandatory(self):
        r = requests.post(f'{config.BASE_URL}/booking', data=config.booking_data_without_name, headers=config.headers)

        assert r.status_code == 500, 'Booking without mandatory field created'

    def test_create_booking_w_invalid_schema(self):
        r = requests.post(f'{config.BASE_URL}/booking', data=config.booking_data_invalid_schema, headers=config.headers)

        assert r.status_code == 500, 'Booking with invalid schema created'

    def test_create_booking_w_missed_in_schema(self):
        r = requests.post(f'{config.BASE_URL}/booking', data=config.booking_data_missing_in_schema, headers=config.headers)

        assert r.status_code == 500, 'Booking with missing in schema created'

    def test_create_booking_w_no_additional(self):
        r = requests.post(f'{config.BASE_URL}/booking', data=config.booking_data_with_no_additional, headers=config.headers)

        assert r.status_code == 200, 'Booking is not created without additional parameter'

    def test_create_booking_invalid_dates_sequence(self):
        r = requests.post(f'{config.BASE_URL}/booking', data=config.booking_data_chech_out_b4_check_in,
                          headers=config.headers)

        assert r.status_code == 500, 'Created booking w check_out before check_in'

    def test_create_booking_equal_dates(self):
        """должен 500тить"""
        r = requests.post(f'{config.BASE_URL}/booking', data=config.booking_data_equal_dates, headers=config.headers)

        assert r.status_code == 500, 'Created booking w equal check_in and check_out dates'

@pytest.mark.skip
class TestUpdateBooking:
    def test_update_booking_dates(self, booking_lifecycle, header_with_token):
        r = requests.put(f'{config.BASE_URL}/booking/{booking_lifecycle}',
                         data=config.update_data_change_dates, headers=header_with_token)
        assert_booking_schema(r.json())
        assert assert_response_contains_request_data(r.json(), json.loads(config.update_data_change_dates))
        assert r.status_code == 200, 'Created booking w equal check_in and check_out dates'


    def test_update_additional(self, booking_lifecycle, header_with_token):
        r = requests.put(f'{config.BASE_URL}/booking/{booking_lifecycle}',
                         data=config.update_additional, headers=header_with_token)

        assert_booking_schema(r.json())
        assert assert_response_contains_request_data(r.json(), json.loads(config.update_data_change_dates))
        assert r.status_code == 200, 'Wrong status code update_additional'

    def test_update_all_booking_data(self, booking_lifecycle, header_with_token):
        r = requests.put(f'{config.BASE_URL}/booking/{booking_lifecycle}',
                         data=config.update_all_booking_data, headers=header_with_token)
        print(r.json())
        assert_booking_schema(r.json())
        assert assert_response_contains_request_data(r.json(), json.loads(config.update_data_change_dates))
        assert r.status_code == 200, 'Created booking w equal check_in and check_out dates'

    def test_update_without_cert(self, booking_lifecycle):
        r = requests.put(f'{config.BASE_URL}/booking/{booking_lifecycle}',
                         data=config.update_data_change_dates)
        assert r.text == 'Forbidden'
        assert r.status_code == 403, 'No Forbidden status code in unauthorized update'

    def test_update_invalid_dates(self, booking_lifecycle, header_with_token):
        r = requests.put(f'{config.BASE_URL}/booking/{booking_lifecycle}',
                         data=config.update_unvalid_dates, headers=header_with_token)
        assert r.status_code == 500, 'No error for update with check out b4 check in'

    def test_update_dates_in_past(self, booking_lifecycle, header_with_token):
        r = requests.put(f'{config.BASE_URL}/booking/{booking_lifecycle}',
                         data=config.update_dates_in_past, headers=header_with_token)

        assert r.status_code == 500, 'Update with dates in past'

    def test_update_non_existant(self, header_with_token):
        r = requests.get(f'{config.BASE_URL}/booking')
        nonexistent_id = config.nonexistent_id_generator(r.json())

        r2 = requests.put(f'{config.BASE_URL}/booking/{nonexistent_id}',
                         data=config.update_all_booking_data, headers=header_with_token)

        assert r2.text == 'Not Found'
        assert r2.status_code == 404, 'Perform update booking with invalid id'

class TestPartialUpdateBooking:
    #@pytest.mark.skip
    #TODO тут добавить параметризацию в тк по одному и обновить все
    #TODOпроблема тут с проверкой checkin check out
    @pytest.mark.parametrize("dates", config.part_upd_dates_data)
    def test_part_update_dates(self, booking_lifecycle, dates, header_with_token):
        r = requests.patch(f'{config.BASE_URL}/booking/{booking_lifecycle}',
                         data=dates, headers=header_with_token)
        assert_booking_schema(r.json())
        assert assert_response_contains_request_data(r.json(), json.loads(dates))
        assert r.status_code == 200, 'Can`t perform partial update'

    @pytest.mark.skip
    def test_part_update_nonexistant_booking(self, header_with_token):
        r = requests.get(f'{config.BASE_URL}/booking')
        nonexistent_id = config.nonexistent_id_generator(r.json())

        r2 = requests.patch(f'{config.BASE_URL}/booking/{nonexistent_id}',
                         data=config.part_upd_dates_data, headers=header_with_token)
        assert r2.text == 'Not Found'
        assert r2.status_code == 404, 'Partial updates booking with invalid id'

    def test_part_update_with_empty_data(self, booking_lifecycle, header_with_token):
        """partial update with empty schema doesn`t affect booking"""
        r = requests.patch(f'{config.BASE_URL}/booking/{booking_lifecycle}',
                         data={}, headers=header_with_token)
        assert_booking_schema(r.json())
        assert assert_response_contains_request_data(r.json(), json.loads(config.booking_data))
        assert r.status_code == 200, 'Can`t perform empty partial update'

    @pytest.mark.parametrize("fields", config.part_upd_fields)
    def test_part_update_each_field(self, booking_lifecycle, fields, header_with_token):
        r = requests.patch(f'{config.BASE_URL}/booking/{booking_lifecycle}',
                         data=fields, headers=header_with_token)
        assert_booking_schema(r.json())
        assert assert_response_contains_request_data(r.json(), json.loads(fields))
        assert r.status_code == 200, 'Can`t perform empty partial update'
