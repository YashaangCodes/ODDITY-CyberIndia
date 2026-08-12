from app.data.phone_reputation import (
    PHONE_REPUTATION_DATA,
    PhoneReputationRecord,
)

from app.services.phone_reputation_sources.base import (
    PhoneReputationSource,
)


class LocalPhoneReputationSource(PhoneReputationSource):

    def lookup(
        self,
        phone_number: str,
    ) -> list[PhoneReputationRecord]:

        return [
            record
            for record in PHONE_REPUTATION_DATA
            if record["number"] == phone_number
        ]