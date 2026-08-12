from abc import ABC, abstractmethod

from app.data.phone_reputation import PhoneReputationRecord


class PhoneReputationSource(ABC):

    @abstractmethod
    def lookup(
        self,
        phone_number: str,
    ) -> list[PhoneReputationRecord]:
        """Return reputation records for a phone number."""
        raise NotImplementedError
