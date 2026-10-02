from rag_pipeline import RAGPipeline


class KYCAssistant:

    def __init__(self):

        # =================================================
        # OFFICIAL HDFC BANK KYC-RELATED SOURCES
        # =================================================

        self.kyc_urls = [

            # 1. KYC and Digital Wallets
            "https://www.hdfcbank.com/personal/resources/learning-centre/pay/kyc--digital-wallets-everything-you-wanted-to-know",

            # 2. Video KYC
            "https://www.hdfcbank.com/personal/resources/learning-centre/save/how-video-kyc-works",

            # 3. Savings Accounts
            "https://www.hdfcbank.com/personal/save/accounts/savings-accounts",

            # 4. Savings Account in India
            "https://www.hdfcbank.com/personal/save/accounts/savings-account-in-india",

            # 5. InstaAccount
            "https://www.hdfcbank.com/personal/save/accounts/savings-accounts/insta-account",

            # 6. Terms and Conditions
            "https://www.hdfcbank.com/personal/useful-links/terms-and-conditions"
        ]


        # =================================================
        # COMMON RAG PIPELINE
        # =================================================

        self.rag = RAGPipeline(

            urls=self.kyc_urls,

            collection_name="kyc_knowledge"
        )


    # =====================================================
    # BUILD / INITIALIZE KYC ASSISTANT
    # =====================================================

    def build(self):

        print("\n===================================")
        print("INITIALIZING KYC ASSISTANT")
        print("===================================")

        self.rag.initialize()

        print("\nKYC Assistant ready.")


    # =====================================================
    # ASK KYC QUESTION
    # =====================================================

    def ask(self, question):

        return self.rag.ask(
            question
        )


# =========================================================
# DIRECT TEST
# =========================================================

if __name__ == "__main__":

    print("\n===================================")
    print("HDFC BANK KYC ASSISTANT")
    print("===================================")


    kyc_assistant = KYCAssistant()


    kyc_assistant.build()


    question = input(
        "\nAsk your KYC question: "
    )


    answer = kyc_assistant.ask(
        question
    )


    print("\nAssistant:")

    print(answer)