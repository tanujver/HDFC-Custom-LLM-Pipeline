from rag_pipeline import RAGPipeline


# ============================================================
# CREDIT CARD ASSISTANT
# ============================================================

class CreditCardAssistant:

    def __init__(self):

        # ====================================================
        # HDFC BANK CREDIT CARD SOURCES
        # ====================================================

        self.credit_card_urls = [

            # ------------------------------------------------
            # GENERAL CREDIT CARD INFORMATION
            # ------------------------------------------------

            "https://www.hdfcbank.com/personal/resources/learning-centre/pay/credit-card-information-the-basics-to-know",

            "https://www.hdfcbank.com/personal/resources/learning-centre/pay/unique-credit-card-features-that-you-may-not-know",

            "https://www.hdfcbank.com/personal/resources/learning-centre/pay/are-credit-cards-free",

            "https://www.hdfcbank.com/personal/resources/learning-centre/pay/what-is-add-on-credit-card-and-its-working",

            "https://www.hdfcbank.com/personal/resources/learning-centre/pay/can-existing-hdfc-bank-credit-card-holders-apply-for-pixel-credit-card",


            # ------------------------------------------------
            # CREDIT CARD BILL PAYMENT
            # ------------------------------------------------

            "https://www.hdfcbank.com/personal/pay/cards/credit-cards/pay-credit-card-bill",


            # ------------------------------------------------
            # MYCARDS / CREDIT CARD MANAGEMENT
            # ------------------------------------------------

            "https://www.hdfcbank.com/personal/pay/cards/credit-cards/mycards-pwa",


            # ------------------------------------------------
            # CREDIT CARD SERVICES / ACTIVATION
            # ------------------------------------------------

            "https://www.hdfcbank.com/personal/pay/cards/credit-cards/credit-card-services/new-activation-offers",


            # ------------------------------------------------
            # CREDIT CARD PRODUCTS
            # ------------------------------------------------

            "https://www.hdfcbank.com/personal/pay/cards/credit-cards",


            # ------------------------------------------------
            # EXAMPLE INDIVIDUAL CREDIT CARD
            # ------------------------------------------------

            "https://www.hdfcbank.com/personal/pay/cards/credit-cards/paytm-hdfc-bank-select-credit-card",

            "https://www.hdfcbank.com/personal/pay/cards/credit-cards/snapdeal-hdfc-bank-credit-card",


            # ------------------------------------------------
            # BUSINESS CREDIT CARDS
            # ------------------------------------------------

            "https://www.hdfcbank.com/personal/pay/cards/business-credit-cards",


            # ------------------------------------------------
            # COMMERCIAL CREDIT CARDS
            # ------------------------------------------------

            "https://www.hdfcbank.com/personal/pay/cards/commercial-credit-cards",


            # ------------------------------------------------
            # CREDIT CARD TERMS & CONDITIONS
            # ------------------------------------------------

            "https://www.hdfcbank.com/personal/useful-links/terms-and-conditions"
        ]


        # ====================================================
        # COMMON RAG PIPELINE
        # ====================================================

        self.rag = RAGPipeline(

            urls=self.credit_card_urls,

            collection_name="credit_card_knowledge"
        )


    # ========================================================
    # BUILD / INITIALIZE
    # ========================================================

    def build(self):

        print("\n===================================")
        print("INITIALIZING CREDIT CARD ASSISTANT")
        print("===================================")

        self.rag.initialize()

        print("\nCredit Card Assistant ready.")


    # ========================================================
    # ASK QUESTION
    # ========================================================

    def ask(self, question):

        return self.rag.ask(question)


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    print("\n===================================")
    print("HDFC BANK CREDIT CARD ASSISTANT")
    print("===================================")

    credit_card_assistant = CreditCardAssistant()

    credit_card_assistant.build()

    question = input(
        "\nAsk your Credit Card question: "
    )

    answer = credit_card_assistant.ask(
        question
    )

    print("\nAssistant:")
    print(answer)