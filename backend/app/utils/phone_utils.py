import re

import phonenumbers
from phonenumbers import NumberParseException


INDIAN_SERVICE_NUMBERS = {
    "100",
    "101",
    "102",
    "108",
    "112",
}


def is_indian_service_number(phone_number: str) -> bool:
    """
    Check whether the input is a recognized Indian emergency/service number.
    """
    return phone_number.strip() in INDIAN_SERVICE_NUMBERS


def _validate_input_length(phone_number: str) -> None:
    """
    Perform basic input validation before passing the value to phonenumbers.

    This prevents obviously malformed Indian phone numbers, such as
    9-digit and 11-digit numbers, from being interpreted unexpectedly.
    """
    cleaned = phone_number.strip()

    # Remove common formatting characters.
    digits = re.sub(r"[^\d]", "", cleaned)

    # Indian local mobile number.
    if cleaned.isdigit():
        if len(digits) != 10:
            raise ValueError("Invalid Indian phone number length.")

    # Indian international formats.
    elif cleaned.startswith("+91"):
        if len(digits) != 12:
            raise ValueError("Invalid Indian phone number length.")

    elif cleaned.startswith("91") and len(digits) == 12:
        pass

    # For other international numbers, allow phonenumbers to perform
    # the country-specific validation.
    else:
        return


def normalize_phone_number(
    phone_number: str,
) -> phonenumbers.PhoneNumber:
    """
    Normalize a phone number into a phonenumbers.PhoneNumber object.

    Ten-digit Indian numbers are automatically interpreted as Indian
    numbers by adding the +91 country code.
    """
    phone_number = phone_number.strip()

    if not phone_number:
        raise ValueError("Phone number cannot be empty.")

    # Service numbers are handled before normalization by the analyzer.
    if is_indian_service_number(phone_number):
        raise ValueError("Service numbers should be handled separately.")

    _validate_input_length(phone_number)

    # Ten-digit Indian local number.
    if phone_number.isdigit() and len(phone_number) == 10:
        phone_number = "+91" + phone_number

    # 91XXXXXXXXXX without the + sign.
    elif phone_number.isdigit() and len(phone_number) == 12:
        phone_number = "+" + phone_number

    try:
        parsed_number = phonenumbers.parse(phone_number, None)
    except NumberParseException as exc:
        raise ValueError("Invalid phone number format.") from exc

    return parsed_number


def is_valid_phone_number(
    phone_number: phonenumbers.PhoneNumber,
) -> bool:
    """
    Check whether the parsed phone number is valid for its region.
    """
    return phonenumbers.is_valid_number(phone_number)


def get_phone_country(
    phone_number: phonenumbers.PhoneNumber,
) -> str:
    """
    Return the region code associated with the phone number.
    """
    region = phonenumbers.region_code_for_number(phone_number)

    if region is None:
        return "Unknown"

    return region


def get_phone_number_type(
    phone_number: phonenumbers.PhoneNumber,
) -> str:
    """
    Return a readable phone-number type.
    """
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