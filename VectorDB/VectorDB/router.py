from typing import Literal


AssistantType = Literal[
    "loan",
    "kyc",
    "credit_card",
    "policy",
    "account"
]


def route_question(question: str) -> AssistantType:
    """
    Decide which HDFC assistant should handle the user question.
    """

    q = question.lower().strip()

    # -------------------------
    # LOAN
    # -------------------------
    loan_keywords = [
        "loan",
        "personal loan",
        "home loan",
        "car loan",
        "two wheeler",
        "two-wheeler",
        "business loan",
        "business growth loan",
        "loan against property",
        "lap",
        "emi",
        "loan eligibility",
        "loan application",
        "loan tenure",
        "loan documents"
    ]

    # -------------------------
    # KYC
    # -------------------------
    kyc_keywords = [
        "kyc",
        "know your customer",
        "video kyc",
        "video verification",
        "payzapp kyc",
        "kyc document",
        "kyc verification",
        "aadhaar verification",
        "identity verification"
    ]

    # -------------------------
    # CREDIT CARD
    # -------------------------
    credit_card_keywords = [
        "credit card",
        "creditcard",
        "credit limit",
        "credit card bill",
        "credit card payment",
        "credit card charges",
        "credit card fee",
        "annual fee",
        "joining fee",
        "cash advance",
        "reward points",
        "mycards",
        "add-on card",
        "addon card"
    ]

    # -------------------------
    # POLICY
    # -------------------------
    policy_keywords = [
        "policy",
        "fair practice",
        "fair practice code",
        "grievance",
        "grievance redressal",
        "complaint",
        "whistleblower",
        "code of conduct",
        "ethics",
        "csr policy",
        "corporate governance",
        "lending code",
        "recovery practices"
    ]

    # -------------------------
    # ACCOUNT
    # -------------------------
    account_keywords = [
        "bank account",
        "savings account",
        "current account",
        "salary account",
        "nre account",
        "nro account",
        "savingsmax",
        "regular savings",
        "instaaccount",
        "insta account",
        "account opening",
        "open account",
        "account number",
        "netbanking",
        "mobilebanking"
    ]

    # Check specific assistants first
    if any(keyword in q for keyword in kyc_keywords):
        return "kyc"

    if any(keyword in q for keyword in credit_card_keywords):
        return "credit_card"

    if any(keyword in q for keyword in policy_keywords):
        return "policy"

    if any(keyword in q for keyword in account_keywords):
        return "account"

    if any(keyword in q for keyword in loan_keywords):
        return "loan"

    # If nothing matches
    return "loan"