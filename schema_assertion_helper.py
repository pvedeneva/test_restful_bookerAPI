import jsonschema
import json

#TODO Schema validation
pattern = {
    "type" : "object",
    "properties": {
        "firstname": {"type" : "string"},
        "lastname": {"type" : "string"},
        "totalprice": {"type" : "number"},
        "depositpaid": {"type" : "boolean"},
        "bookingdates": {
            "type" : "object",
            "properties":
                {"checkin": {"type" : "string"},
                "checkout": {"type" : "string"}},
            "requered" : [ "checkin", "checkout"]
        },
        "additionalneeds": {"type" : "string"}
        #"additionalneeds": {"type" : "number"}
    },
    "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"]
}

response = {
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


def assert_booking_schema(response, schema_pattern = pattern):
    """ Checks whether the given data matches the schema """
    jsonschema.validate(response, schema_pattern)

#print(assert_booking_schema(response, schema))
