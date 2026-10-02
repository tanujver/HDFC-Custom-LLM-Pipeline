import os
import sys
import json
import importlib
import inspect
from dotenv import load_dotenv


# ============================================================
# PATH SETUP
# ============================================================

EVALUATION_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

BASE_DIR = os.path.dirname(
    EVALUATION_DIR
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv(
    os.path.join(BASE_DIR, ".env")
)


# ============================================================
# LOAD ASSISTANT
# ============================================================

def load_assistant(assistant_name):

    module_name = (
        assistant_name.lower()
        .strip()
        .replace(" ", "_")
        .replace("-", "_")
    )

    if not module_name.endswith("_assistant"):
        module_name += "_assistant"

    print(f"\nLoading: {module_name}")

    try:
        module = importlib.import_module(module_name)

    except Exception as e:

        raise ImportError(
            f"Could not import {module_name}.py\n"
            f"Error: {e}"
        )

    assistant_class = None

    for name, obj in inspect.getmembers(
        module,
        inspect.isclass
    ):

        if name == "RAGPipeline":
            continue

        if (
            name.lower().endswith("assistant")
            and obj.__module__ == module.__name__
        ):
            assistant_class = obj
            break

    if assistant_class is None:

        raise ImportError(
            f"Assistant class not found in "
            f"{module_name}.py"
        )

    assistant = assistant_class()

    # Initialize RAG
    if hasattr(assistant, "build"):

        assistant.build()

    elif hasattr(assistant, "initialize"):

        assistant.initialize()

    return assistant


# ============================================================
# ASK ASSISTANT
# ============================================================

def ask_assistant(
    assistant,
    question
):

    if not hasattr(
        assistant,
        "ask"
    ):

        raise AttributeError(
            "Assistant does not have ask() method."
        )

    answer = assistant.ask(question)

    if answer is None:
        return ""

    return str(answer).strip()


# ============================================================
# GATE TESTS
# ============================================================

GATE_TESTS = [

    {
        "id": 1,
        "name": "Grounded Loan Answer",

        "assistant": "loan",

        "question":
            "What is a personal loan?",

        "expected_keywords": [
            "unsecured",
            "loan"
        ],

        "must_not_contain": [
            "I don't know"
        ]
    },


    {
        "id": 2,
        "name": "KYC Answer",

        "assistant": "kyc",

        "question":
            "What does KYC stand for?",

        "expected_keywords": [
            "know",
            "your",
            "customer"
        ],

        "must_not_contain": [
            "I don't know"
        ]
    },


    {
        "id": 3,
        "name": "Credit Card Answer",

        "assistant": "credit_card",

        "question":
            "What is a credit card?",

        "expected_keywords": [
            "credit",
            "card"
        ],

        "must_not_contain": [
            "I don't know"
        ]
    },


    {
        "id": 4,
        "name": "Account Answer",

        "assistant": "account",

        "question":
            "What is a savings account?",

        "expected_keywords": [
            "savings",
            "account"
        ],

        "must_not_contain": [
            "I don't know"
        ]
    },


    {
        "id": 5,
        "name": "Policy Answer",

        "assistant": "policy",

        "question":
            "What is the purpose of the Fair Practice Code for Lending?",

        "expected_keywords": [
            "fair",
            "lending"
        ],

        "must_not_contain": [
            "I don't know"
        ]
    }

]


# ============================================================
# RUN ONE GATE TEST
# ============================================================

def run_gate_test(
    assistant,
    test
):

    answer = ask_assistant(
        assistant,
        test["question"]
    )

    answer_lower = answer.lower()

    keyword_results = []

    for keyword in test["expected_keywords"]:

        keyword_results.append(
            keyword.lower() in answer_lower
        )

    forbidden_results = []

    for phrase in test["must_not_contain"]:

        forbidden_results.append(
            phrase.lower() in answer_lower
        )

    keywords_passed = all(
        keyword_results
    )

    forbidden_passed = not any(
        forbidden_results
    )

    passed = (
        keywords_passed
        and forbidden_passed
    )

    return {
        "test_id": test["id"],
        "test_name": test["name"],
        "assistant": test["assistant"],
        "question": test["question"],
        "answer": answer,
        "passed": passed,
        "keyword_check": keywords_passed,
        "forbidden_check": forbidden_passed
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n")
    print("=" * 70)
    print("HDFC BANK AI — EVALUATION GATE")
    print("=" * 70)

    assistants = {}

    results = []

    passed_count = 0
    failed_count = 0


    # ========================================================
    # RUN ALL TESTS
    # ========================================================

    for test in GATE_TESTS:

        print("\n")
        print("-" * 70)

        print(
            f"Test {test['id']}: "
            f"{test['name']}"
        )

        print(
            f"Assistant: "
            f"{test['assistant']}"
        )

        print(
            f"Question: "
            f"{test['question']}"
        )


        # ----------------------------------------------------
        # LOAD ASSISTANT ONLY ONCE
        # ----------------------------------------------------

        try:

            if test["assistant"] not in assistants:

                assistants[
                    test["assistant"]
                ] = load_assistant(
                    test["assistant"]
                )

            assistant = assistants[
                test["assistant"]
            ]


        except Exception as e:

            print(
                f"\nAssistant loading failed: {e}"
            )

            result = {
                "test_id": test["id"],
                "test_name": test["name"],
                "assistant": test["assistant"],
                "question": test["question"],
                "answer": "",
                "passed": False,
                "error": str(e)
            }

            results.append(result)

            failed_count += 1

            continue


        # ----------------------------------------------------
        # RUN TEST
        # ----------------------------------------------------

        try:

            result = run_gate_test(
                assistant,
                test
            )

            results.append(result)


            print(
                "\nAnswer:"
            )

            print(
                result["answer"]
            )


            if result["passed"]:

                print(
                    "\nRESULT: PASS"
                )

                passed_count += 1

            else:

                print(
                    "\nRESULT: FAIL"
                )

                failed_count += 1


        except Exception as e:

            print(
                f"\nTest error: {e}"
            )

            result = {
                "test_id": test["id"],
                "test_name": test["name"],
                "assistant": test["assistant"],
                "question": test["question"],
                "answer": "",
                "passed": False,
                "error": str(e)
            }

            results.append(result)

            failed_count += 1


    # ========================================================
    # FINAL GATE STATUS
    # ========================================================

    total_tests = len(
        GATE_TESTS
    )

    gate_passed = (
        failed_count == 0
    )


    if gate_passed:

        gate_status = "PASS"

    else:

        gate_status = "FAIL"


    # ========================================================
    # SAVE RESULTS
    # ========================================================

    results_file = os.path.join(
        EVALUATION_DIR,
        "evaluation_gate_results.json"
    )

    final_results = {

        "gate_status": gate_status,

        "total_tests": total_tests,

        "passed": passed_count,

        "failed": failed_count,

        "tests": results
    }


    with open(
        results_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            final_results,
            f,
            indent=4,
            ensure_ascii=False
        )


    # ========================================================
    # FINAL REPORT
    # ========================================================

    print("\n")
    print("=" * 70)
    print("EVALUATION GATE RESULT")
    print("=" * 70)

    print(
        f"Total Tests : {total_tests}"
    )

    print(
        f"Passed      : {passed_count}"
    )

    print(
        f"Failed      : {failed_count}"
    )

    print(
        f"Gate Status : {gate_status}"
    )

    print(
        "\nResults saved to:"
    )

    print(
        results_file
    )

    print("=" * 70)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()