# assistant_router.py

import re


class AssistantRouter:
    """
    Routes a user question to the most relevant HDFC Bank assistant.

    Available assistants:
        - loan
        - kyc
        - credit_card
        - policy
        - account
    """

    def __init__(self):
        self.assistants = {
            "loan": [
                "loan",
                "loans",
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
                "eligibility",
                "borrow",
                "borrowing",
                "tenure",
                "interest rate",
                "collateral",
                "documentation",
                "documents",
            ],

            "kyc": [
                "kyc",
                "know your customer",
                "video kyc",
                "video verification",
                "identity verification",
                "customer verification",
                "pan card",
                "aadhaar",
                "aadhaar verification",
                "payzapp kyc",
                "kyc compliant",
            ],

            "credit_card": [
                "credit card",
                "credit cards",
                "creditcard",
                "cvv",
                "credit limit",
                "card limit",
                "card payment",
                "card bill",
                "credit card bill",
                "cash advance",
                "cash withdrawal",
                "reward points",
                "cashback",
                "add-on card",
                "addon card",
                "mycards",
                "lifetime free card",
                "annual fee",
                "joining fee",
            ],

            "policy": [
                "policy",
                "policies",
                "fair practice",
                "fair practice code",
                "grievance",
                "grievance redressal",
                "complaint",
                "complaint resolution",
                "whistleblower",
                "code of conduct",
                "ethics",
                "csr",
                "corporate social responsibility",
                "lending code",
                "terms and conditions",
                "customer rights",
                "discrimination",
                "recovery practices",
            ],

            "account": [
                "account",
                "accounts",
                "savings account",
                "saving account",
                "current account",
                "salary account",
                "nri account",
                "nre account",
                "nro account",
                "instaaccount",
                "insta account",
                "savingsmax",
                "regular savings",
                "account opening",
                "open account",
                "bank account",
                "netbanking",
                "mobile banking",
            ],
        }

    # ---------------------------------------------------------
    # CLEAN QUESTION
    # ---------------------------------------------------------

    def _clean_text(self, text):
        """
        Normalize the user question.
        """

        if not text:
            return ""

        text = text.lower().strip()

        # Remove unnecessary punctuation
        text = re.sub(r"[^\w\s-]", " ", text)

        # Remove extra spaces
        text = re.sub(r"\s+", " ", text)

        return text

    # ---------------------------------------------------------
    # ROUTE QUESTION
    # ---------------------------------------------------------

    def route(self, question):
        """
        Return the assistant name best matching the question.

        Returns:
            loan
            kyc
            credit_card
            policy
            account
            unknown
        """

        question = self._clean_text(question)

        if not question:
            return "unknown"

        scores = {
            "loan": 0,
            "kyc": 0,
            "credit_card": 0,
            "policy": 0,
            "account": 0,
        }

        # -----------------------------------------------------
        # Keyword matching
        # -----------------------------------------------------

        for assistant, keywords in self.assistants.items():

            for keyword in keywords:

                keyword = keyword.lower()

                # Exact phrase match
                if keyword in question:

                    # Longer phrases are more meaningful
                    if len(keyword.split()) > 1:
                        scores[assistant] += 3
                    else:
                        scores[assistant] += 1

        # -----------------------------------------------------
        # Special rules for ambiguous questions
        # -----------------------------------------------------

        # KYC has priority when explicitly mentioned
        if "kyc" in question:
            scores["kyc"] += 10

        # Credit card has priority when explicitly mentioned
        if "credit card" in question or "credit cards" in question:
            scores["credit_card"] += 10

        # Loan has priority when explicitly mentioned
        if "personal loan" in question:
            scores["loan"] += 10

        if "home loan" in question:
            scores["loan"] += 10

        if "car loan" in question:
            scores["loan"] += 10

        if "two wheeler loan" in question:
            scores["loan"] += 10

        # Account-specific products
        if "savings account" in question:
            scores["account"] += 10

        if "current account" in question:
            scores["account"] += 10

        if "salary account" in question:
            scores["account"] += 10

        if "instaaccount" in question or "insta account" in question:
            scores["account"] += 10

        # Policy-specific terms
        if "fair practice code" in question:
            scores["policy"] += 10

        if "grievance redressal" in question:
            scores["policy"] += 10

        if "whistleblower" in question:
            scores["policy"] += 10

        # -----------------------------------------------------
        # Find best assistant
        # -----------------------------------------------------

        best_assistant = max(
            scores,
            key=scores.get
        )

        best_score = scores[best_assistant]

        # -----------------------------------------------------
        # Unknown question
        # -----------------------------------------------------

        if best_score == 0:
            return "unknown"

        return best_assistant

    # ---------------------------------------------------------
    # ROUTE WITH SCORE
    # ---------------------------------------------------------

    def route_with_score(self, question):
        """
        Returns both selected assistant and matching score.

        Example:
            {
                "assistant": "loan",
                "score": 10
            }
        """

        question = self._clean_text(question)

        if not question:
            return {
                "assistant": "unknown",
                "score": 0
            }

        scores = {
            "loan": 0,
            "kyc": 0,
            "credit_card": 0,
            "policy": 0,
            "account": 0,
        }

        for assistant, keywords in self.assistants.items():

            for keyword in keywords:

                keyword = keyword.lower()

                if keyword in question:

                    if len(keyword.split()) > 1:
                        scores[assistant] += 3
                    else:
                        scores[assistant] += 1

        # Explicit keyword boosts

        if "kyc" in question:
            scores["kyc"] += 10

        if "credit card" in question:
            scores["credit_card"] += 10

        if "personal loan" in question:
            scores["loan"] += 10

        if "home loan" in question:
            scores["loan"] += 10

        if "car loan" in question:
            scores["loan"] += 10

        if "savings account" in question:
            scores["account"] += 10

        if "current account" in question:
            scores["account"] += 10

        if "instaaccount" in question:
            scores["account"] += 10

        if "fair practice code" in question:
            scores["policy"] += 10

        if "grievance redressal" in question:
            scores["policy"] += 10

        if "whistleblower" in question:
            scores["policy"] += 10

        best_assistant = max(
            scores,
            key=scores.get
        )

        best_score = scores[best_assistant]

        if best_score == 0:
            return {
                "assistant": "unknown",
                "score": 0
            }

        return {
            "assistant": best_assistant,
            "score": best_score
        }


# ---------------------------------------------------------
# TESTING
# ---------------------------------------------------------

if __name__ == "__main__":

    router = AssistantRouter()

    test_questions = [
        "What is a personal loan?",
        "What documents are required for KYC?",
        "What is the credit card annual fee?",
        "What is the Fair Practice Code?",
        "How can I open a savings account?",
        "What is an InstaAccount?",
        "What is Video KYC?",
        "What is a home loan?",
    ]

    print("\nAssistant Router Test\n")
    print("-" * 60)

    for question in test_questions:

        result = router.route_with_score(question)

        print(f"Question   : {question}")
        print(f"Assistant  : {result['assistant']}")
        print(f"Score      : {result['score']}")
        print("-" * 60)