from app.data.phone_reputation import PhoneReputationRecord

from app.services.phone_reputation_sources.local import (
    LocalPhoneReputationSource,
)


def lookup_phone_reputation(
    phone_number: str,
) -> list[PhoneReputationRecord]:

    source = LocalPhoneReputationSource()

    return source.lookup(phone_number)

