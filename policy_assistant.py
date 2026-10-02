from rag_pipeline import RAGPipeline


class PoliciesAssistant:

    def __init__(self):

        self.policy_urls = [

            # 1. Customer Rights Policy
            "https://www.hdfcbank.com/content/api/contentstream-id/723fb80a-2dde-42a3-9793-7ae1be57c87f/26c1d6cb-5423-49ed-bca2-b4ccb6c79974",

            # 2. Grievance Redressal Policy
            "https://www.hdfcbank.com/content/api/contentstream-id/723fb80a-2dde-42a3-9793-7ae1be57c87f/85e28432-ecfb-4a9e-bdb1-743e0cf2e00d",

            # 3. Fair Practice Code for Lending
            "https://www.hdfcbank.com/personal/about-us/corporate-governance/fair-practice-code-for-lending",

            # 4. HDFC Bank Terms & Conditions
            "https://www.hdfcbank.com/personal/useful-links/terms-and-conditions",

            # 5. HDFC Bank CSR Policy
            "https://v.hdfcbank.com/content/dam/hdfc-aem-microsites/csr/pdfs/CSR_Policy.pdf",

            # 6. HDFC Bank Whistleblower Policy
            "https://www.hdfcbank.com/content/bbp/repositories/723fb80a-2dde-42a3-9793-7ae1be57c87f/?path=%2FFooter%2FAbout+Us%2FCorporate+Governance%2FCodes+and+Policie%2Fpdf%2FWhistleblower-Policy-2019.pdf",

            # 7. HDFC Bank Code of Conduct and Ethics Manual
            "https://www.hdfcbank.com/content/bbp/repositories/723fb80a-2dde-42a3-9793-7ae1be57c87f/?path=%2FFooter%2FAbout+Us%2FCorporate+Governance%2FCodes+and+Policie%2Fpdf%2Fsept%2FCode_of_Conduct_and_Ethics_Manual_sept_2024.pdf"
        ]

        self.rag = RAGPipeline(
            urls=self.policy_urls,
            collection_name="policy_knowledge"
        )

    def build(self):
        """
        Initialize or update the policy knowledge base.
        """
        self.rag.initialize()

    def ask(self, question):
        """
        Ask a policy-related question.
        """
        return self.rag.ask(question)


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("\n===================================")
    print("HDFC BANK POLICY ASSISTANT")
    print("===================================")

    policy_assistant = PoliciesAssistant()

    policy_assistant.build()

    question = input("\nAsk your policy question: ")

    answer = policy_assistant.ask(question)

    print("\nAssistant:")
    print(answer)