from typing import Literal, TypedDict


class PhoneReputationRecord(TypedDict):
    number: str
    classification: Literal["scam", "spam", "suspicious"]
    category: str
    source: Literal[
        "i4c_ncrp",
        "dot_chakshu",
        "trai_ucc",
        "verified_public_dataset",
        "development_fixture",
    ]
    evidence_type: Literal[
        "cybercrime_report",
        "fraud_report",
        "spam_report",
        "verified_dataset",
        "synthetic_test_data",
    ]
    report_count: int
    confidence: Literal["low", "medium", "high"]


# PHONE_REPUTATION_DATA: list[PhoneReputationRecord] = []

# Sample data for testing purposes
# Temporary development fixtures.
#
# This data is NOT an official government dataset and must not be
# presented to users as verified real-world reputation data.
#
# It exists only to test the reputation-analysis pipeline until
# a legitimate external data source is integrated.

PHONE_REPUTATION_DATA: list[PhoneReputationRecord] = [
    {
        "number": "+919999999999",
        "classification": "scam",
        "category": "banking_or_kyc_scam",
        "source": "i4c_ncrp",
        "evidence_type": "cybercrime_report",
        "report_count": 5,
        "confidence": "high",
    },
    {
        "number": "+919999999999",
        "classification": "spam",
        "category": "spam_call",
        "source": "trai_ucc",
        "evidence_type": "spam_report",
        "report_count": 10,
        "confidence": "medium",
    },
    {
        "number": "+919999999999",
        "classification": "suspicious",
        "category": "suspicious_activity",
        "source": "dot_chakshu",
        "evidence_type": "fraud_report",
        "report_count": 3,
        "confidence": "medium",
    },
    {
        "number": "+919777777777",
        "classification": "spam",
        "category": "telemarketing_spam",
        "source": "trai_ucc",
        "evidence_type": "spam_report",
        "report_count": 1,
        "confidence": "low",
    },
    {
        "number": "+919666666666",
        "classification": "suspicious",
        "category": "unknown_suspicious_activity",
        "source": "dot_chakshu",
        "evidence_type": "fraud_report",
        "report_count": 3,
        "confidence": "medium",
    },
    {
        "number": "+919555555555",
        "classification": "scam",
        "category": "investment_scam",
        "source": "i4c_ncrp",
        "evidence_type": "cybercrime_report",
        "report_count": 12,
        "confidence": "high",
    },
]
