import phonenumbers
from phonenumbers import NumberParseException


def normalize_phone_number(phone_number: str) -> phonenumbers.PhoneNumber:
    phone_number = phone_number.strip()

    if phone_number.isdigit() and len(phone_number) == 10:
        phone_number = "+91" + phone_number

    try:
        parsed_number = phonenumbers.parse(phone_number, None)
    except NumberParseException:
        raise ValueError("Invalid phone number format.")

    return parsed_number

def is_valid_phone_number(
    phone_number: phonenumbers.PhoneNumber,
) -> bool:
    return phonenumbers.is_valid_number(phone_number)

def get_phone_country(
    phone_number: phonenumbers.PhoneNumber,
) -> str:
    region = phonenumbers.region_code_for_number(phone_number)

    if region is None:
        return "Unknown"

    return region

def get_phone_number_type(
    phone_number: phonenumbers.PhoneNumber,
) -> str:
    number_type = phonenumbers.number_type(phone_number)

    type_names = {
        phonenumbers.PhoneNumberType.MOBILE: "mobile",
        phonenumbers.PhoneNumberType.FIXED_LINE: "landline",
        phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "mobile_or_landline",
        phonenumbers.PhoneNumberType.TOLL_FREE: "toll_free",
        phonenumbers.PhoneNumberType.PREMIUM_RATE: "premium_rate",
        phonenumbers.PhoneNumberType.SHARED_COST: "shared_cost",
        phonenumbers.PhoneNumberType.VOIP: "voip",
        phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "personal",
        phonenumbers.PhoneNumberType.PAGER: "pager",
    }

    return type_names.get(number_type, "unknown")

def is_indian_service_number(phone_number: str) -> bool:
    service_numbers = {
        "100",
        "101",
        "102",
        "108",
        "112",
    }

    return phone_number.strip() in service_numbers