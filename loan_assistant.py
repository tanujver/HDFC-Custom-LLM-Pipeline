from rag_pipeline import RAGPipeline



class LoanAssistant:

    def __init__(self):

        
        # LOAN-SPECIFIC HDFC BANK URLs
       

        self.loan_urls = [

            # Personal Loan
            "https://www.hdfcbank.com/personal/borrow/popular-loans/personal-loan",

            # Personal Loan Eligibility
            "https://v.hdfcbank.com/htdocs/amp/personal-loan/eligibility_criteria.html",

            # Home Loan
            "https://www.hdfcbank.com/personal/borrow/popular-loans/home-loan",

            # Car Loan
            "https://www.hdfcbank.com/personal/borrow/popular-loans/car-loan",

            # Two Wheeler Loan
            "https://www.hdfcbank.com/personal/borrow/popular-loans/two-wheeler-loan",

            # Two Wheeler Loan Documentation
            "https://www.hdfcbank.com/personal/borrow/popular-loans/two-wheeler-loan/documentation",

            # Business Growth Loan
            "https://v.hdfcbank.com/htdocs/amp/personal/borrow/popular-loans/business-growth-loan/menu-footer.html",

            # Loan Against Property
            "https://www.hdfcbank.com/personal/resources/learning-centre/sme/explained-loan-against-property-for-your-business"
        ]


        # ----------------------------------------------------
        # COMMON RAG PIPELINE
        # ----------------------------------------------------

        self.rag = RAGPipeline(
            urls=self.loan_urls
        )


    # ========================================================
    # BUILD LOAN KNOWLEDGE BASE
    # ========================================================

    def build(self):

        print("\nBuilding Loan Assistant knowledge base...")

        self.rag.initialize()

        print("Loan Assistant knowledge base ready.")


    # ========================================================
    # ASK LOAN QUESTION
    # ========================================================

    def ask(self, question):

        return self.rag.ask(question)


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("\n===================================")
    print("HDFC BANK LOAN ASSISTANT")
    print("===================================")

    loan_assistant = LoanAssistant()

    loan_assistant.build()

    question = input("\nAsk your loan question: ")

    answer = loan_assistant.ask(question)

    print("\nAssistant:")
    print(answer)