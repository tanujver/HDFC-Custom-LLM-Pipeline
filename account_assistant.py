from rag_pipeline import RAGPipeline


class AccountAssistant:

    def __init__(self):

        self.account_urls = [

            # 1. HDFC Bank - All Account Types
            "https://www.hdfcbank.com/personal/save/accounts",

            # 2. Savings Accounts
            "https://www.hdfcbank.com/personal/save/accounts/savings-accounts",

            # 3. Savings Account in India
            "https://www.hdfcbank.com/personal/save/accounts/savings-account-in-india",

            # 4. Regular Savings Account
            "https://www.hdfcbank.com/personal/save/accounts/savings-accounts/regular-savings-accounts",

            # 5. SavingsMax Account
            "https://www.hdfcbank.com/personal/save/accounts/savings-accounts/savings-max-account",

            # 6. InstaAccount - Instant Savings / Salary Account
            "https://www.hdfcbank.com/personal/save/accounts/savings-accounts/insta-account",

            # 7. Current Account - Online Application
            "https://www.hdfcbank.com/personal/save/accounts/current-accounts/plus-current-account/apply-online",

            # 8. Institutional Current Account
            "https://www.hdfcbank.com/personal/save/accounts/current-accounts/institutional-current-account/fees-and-charges",

            # 9. RERA Current Account
            "https://www.hdfcbank.com/personal/save/accounts/current-accounts/rera-current-account",

            # 10. Salary Account - Terms and Conditions
            "https://www.hdfcbank.com/personal/save/accounts/salary-accounts/premium-with-platinum-debit-card/terms-and-conditions",

            # 11. NRE Savings Account Documentation
            "https://www.hdfcbank.com/nri-banking/save/nri-accounts/savings-account/nre-savings-account/documentation",

            # 12. Returning NRI / RFC Accounts
            "https://www.hdfcbank.com/nri-banking/save/nri-accounts/accounts-for-returning-nris",

            # 13. HDFC Bank Terms and Conditions
            "https://www.hdfcbank.com/personal/useful-links/terms-and-conditions"
        ]

        self.rag = RAGPipeline(
            urls=self.account_urls,
            collection_name="account_knowledge"
        )

    def build(self):
        """
        Initialize or update the Account knowledge base.
        """
        self.rag.initialize()

    def ask(self, question):
        """
        Ask an account-related question.
        """
        return self.rag.ask(question)


