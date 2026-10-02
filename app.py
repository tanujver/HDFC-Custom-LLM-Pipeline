import streamlit as st
from loan_assistant import LoanAssistant
from kyc_assistant import KYCAssistant
from credit_card_assistant import CreditCardAssistant
from policy_assistant import PoliciesAssistant
from account_assistant import AccountAssistant


from assistant_router import AssistantRouter


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="HDFC Bank AI Assistant Factory",
    page_icon="🏦",
    layout="wide"
)


# =========================================================
# HEADER
# =========================================================

st.title("🏦 HDFC Bank AI Assistant")

st.write(
    "Ask your question. The system will automatically select "
    "the most relevant HDFC Bank assistant."
)


# =========================================================
# SESSION STATE
# =========================================================

if "router" not in st.session_state:
    st.session_state.router = AssistantRouter()


if "loan_assistant" not in st.session_state:
    st.session_state.loan_assistant = None


if "kyc_assistant" not in st.session_state:
    st.session_state.kyc_assistant = None


if "credit_card_assistant" not in st.session_state:
    st.session_state.credit_card_assistant = None


if "policies_assistant" not in st.session_state:
    st.session_state.policies_assistant = None


if "account_assistant" not in st.session_state:
    st.session_state.account_assistant = None


if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# HELPER FUNCTION
# =========================================================

def get_assistant(assistant_name):

    if assistant_name == "loan":

        if st.session_state.loan_assistant is None:

            with st.spinner("Initializing Loan Assistant..."):

                st.session_state.loan_assistant = LoanAssistant()

                st.session_state.loan_assistant.build()

        return st.session_state.loan_assistant


    elif assistant_name == "kyc":

        if st.session_state.kyc_assistant is None:

            with st.spinner("Initializing KYC Assistant..."):

                st.session_state.kyc_assistant = KYCAssistant()

                st.session_state.kyc_assistant.build()

        return st.session_state.kyc_assistant


    elif assistant_name == "credit_card":

        if st.session_state.credit_card_assistant is None:

            with st.spinner("Initializing Credit Card Assistant..."):

                st.session_state.credit_card_assistant = (
                    CreditCardAssistant()
                )

                st.session_state.credit_card_assistant.build()

        return st.session_state.credit_card_assistant


    elif assistant_name == "policy":

        if st.session_state.policies_assistant is None:

            with st.spinner("Initializing Policies Assistant..."):

                st.session_state.policies_assistant = (
                    PoliciesAssistant()
                )

                st.session_state.policies_assistant.build()

        return st.session_state.policies_assistant


    elif assistant_name == "account":

        if st.session_state.account_assistant is None:

            with st.spinner("Initializing Account Assistant..."):

                st.session_state.account_assistant = (
                    AccountAssistant()
                )

                st.session_state.account_assistant.build()

        return st.session_state.account_assistant


    else:

        return None


# =========================================================
# DISPLAY PREVIOUS CHAT
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

        # Show selected assistant for assistant messages
        if (
            message["role"] == "assistant"
            and "assistant_name" in message
        ):

            st.caption(
                f"🤖 Assistant used: {message['assistant_name']}"
            )


# =========================================================
# CLEAR CHAT
# =========================================================

if st.button("🗑️ Clear Chat"):

    st.session_state.messages = []

    st.rerun()


# =========================================================
# COMMON CHAT INPUT
# =========================================================

question = st.chat_input(
    "Ask any question about HDFC Bank..."
)


# =========================================================
# PROCESS QUESTION
# =========================================================

if question:

    # -----------------------------------------------------
    # SHOW USER QUESTION
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.write(question)


    # -----------------------------------------------------
    # ROUTE QUESTION
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Identifying the most relevant assistant..."
        ):

            try:

                routing_result = st.session_state.router.route(
                    question
                )

            except Exception as e:

                st.error(
                    f"Router Error: {str(e)}"
                )

                st.stop()


        # -------------------------------------------------
        # GET ROUTING INFORMATION
        # -------------------------------------------------

        if isinstance(routing_result, dict):

            assistant_name = routing_result.get(
                "assistant"
            )

            score = routing_result.get(
                "score",
                None
            )

        else:

            # If router returns only assistant name
            assistant_name = routing_result

            score = None


        # -------------------------------------------------
        # INVALID ROUTE
        # -------------------------------------------------

        if assistant_name is None:

            answer = (
                "I could not identify the appropriate "
                "HDFC Bank assistant for this question."
            )

            st.write(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "assistant_name": "None"
                }
            )

            st.stop()


        # -------------------------------------------------
        # INITIALIZE SELECTED ASSISTANT
        # -------------------------------------------------

        assistant = get_assistant(
            assistant_name
        )


        if assistant is None:

            answer = (
                "Sorry, I could not initialize the "
                "required assistant."
            )

            st.write(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "assistant_name": assistant_name
                }
            )

            st.stop()


        # -------------------------------------------------
        # GENERATE ANSWER USING EXISTING RAG
        # -------------------------------------------------

        with st.spinner(
            f"Searching HDFC Bank sources using "
            f"{assistant_name} assistant..."
        ):

            try:

                answer = assistant.ask(
                    question
                )

            except Exception as e:

                answer = (
                    f"Error while generating answer: {str(e)}"
                )


        # -------------------------------------------------
        # DISPLAY ANSWER
        # -------------------------------------------------

        st.write(answer)


        # -------------------------------------------------
        # ROUTING INFORMATION
        # -------------------------------------------------

        st.caption(
            f"🤖 Assistant used: {assistant_name}"
        )

        if score is not None:

            st.caption(
                f"Router matching score: {score}"
            )


    # -----------------------------------------------------
    # SAVE ASSISTANT RESPONSE
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "assistant_name": assistant_name
        }
    )