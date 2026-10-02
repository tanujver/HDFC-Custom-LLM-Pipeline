import os
import sys
import json
import importlib
import inspect
import time

from dotenv import load_dotenv
from groq import Groq


# ============================================================
# PATH SETUP
# ============================================================

# Project structure:
#
# HDFC BANK AI ASSISTANT
# │
# ├── .env
# ├── app.py
# ├── loan_assistant.py
# ├── kyc_assistant.py
# ├── credit_card_assistant.py
# ├── policy_assistant.py
# ├── account_assistant.py
# │
# └── Evaluation
#     ├── run_evaluation.py
#     ├── evaluation_questions.json
#     └── evaluation_results.json
#
#
# run_evaluation.py is inside Evaluation folder.
#
# Therefore:
#
# EVALUATION_DIR = Evaluation folder
# BASE_DIR       = Main project folder


EVALUATION_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

BASE_DIR = os.path.dirname(
    EVALUATION_DIR
)


# ============================================================
# PYTHON PATH
# ============================================================

# Add main project folder to Python path
# so that Python can import:
#
# loan_assistant.py
# kyc_assistant.py
# credit_card_assistant.py
# policy_assistant.py
# account_assistant.py

if BASE_DIR not in sys.path:

    sys.path.insert(
        0,
        BASE_DIR
    )


# ============================================================
# FILE PATHS
# ============================================================

QUESTIONS_FILE = os.path.join(
    EVALUATION_DIR,
    "evaluation_questions.json"
)

RESULTS_FILE = os.path.join(
    EVALUATION_DIR,
    "evaluation_results.json"
)

ENV_FILE = os.path.join(
    BASE_DIR,
    ".env"
)


# ============================================================
# CHECK ENVIRONMENT FILE
# ============================================================

print("\nChecking environment file...")

print(
    f".env expected at:\n{ENV_FILE}"
)


if not os.path.exists(ENV_FILE):

    raise FileNotFoundError(

        "\n.env file was not found.\n\n"

        "Expected location:\n"
        f"{ENV_FILE}\n\n"

        "Please make sure your .env file is "
        "inside the main HDFC BANK AI ASSISTANT folder."
    )


print(
    "\n.env file found successfully."
)


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv(
    ENV_FILE
)


# ============================================================
# GROQ API KEY
# ============================================================

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)


if not GROQ_API_KEY:

    raise ValueError(

        "\nGROQ_API_KEY not found in .env file.\n\n"

        "Please make sure your .env contains:\n\n"

        "GROQ_API_KEY=your_api_key_here"
    )


print(
    "GROQ_API_KEY loaded successfully."
)


# ============================================================
# EVALUATION MODEL
# ============================================================

MODEL_NAME = "openai/gpt-oss-120b"


client = Groq(
    api_key=GROQ_API_KEY
)


# ============================================================
# PROJECT INFORMATION
# ============================================================

print(
    f"\nProject Directory:\n{BASE_DIR}"
)

print(
    f"\nEvaluation Directory:\n{EVALUATION_DIR}"
)

print(
    f"\nQuestions File:\n{QUESTIONS_FILE}"
)

print(
    f"\nResults File:\n{RESULTS_FILE}"
)

print(
    f"\nEvaluation Model:\n{MODEL_NAME}"
)


# ============================================================
# LOAD QUESTIONS
# ============================================================

def load_questions():

    if not os.path.exists(
        QUESTIONS_FILE
    ):

        raise FileNotFoundError(

            "\nevaluation_questions.json "
            "was not found.\n\n"

            "Expected location:\n"
            f"{QUESTIONS_FILE}"
        )


    with open(
        QUESTIONS_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        questions = json.load(f)


    if not isinstance(
        questions,
        list
    ):

        raise ValueError(
            "evaluation_questions.json "
            "must contain a JSON list."
        )


    return questions


# ============================================================
# FIND ASSISTANT CLASS
# ============================================================

def load_assistant(
    assistant_name
):

    # --------------------------------------------------------
    # Convert assistant name to module name
    # --------------------------------------------------------

    module_name = (
        assistant_name
        .lower()
        .strip()
        .replace(" ", "_")
        .replace("-", "_")
    )


    # Example:
    #
    # loan
    # ->
    # loan_assistant
    #
    # kyc
    # ->
    # kyc_assistant
    #
    # credit_card
    # ->
    # credit_card_assistant


    if not module_name.endswith(
        "_assistant"
    ):

        module_name += "_assistant"


    print(
        f"\nLoading assistant module: "
        f"{module_name}"
    )


    # --------------------------------------------------------
    # Import module
    # --------------------------------------------------------

    try:

        module = importlib.import_module(
            module_name
        )


    except Exception as e:

        raise ImportError(

            f"\nCould not import "
            f"{module_name}.py\n\n"

            f"Project directory:\n"
            f"{BASE_DIR}\n\n"

            f"Error:\n{e}"
        )


    # --------------------------------------------------------
    # Find Assistant class
    # --------------------------------------------------------

    assistant_class = None


    for name, obj in inspect.getmembers(
        module,
        inspect.isclass
    ):

        # Ignore imported RAGPipeline class
        if name == "RAGPipeline":
            continue


        # Only select Assistant class
        if (
            name.lower().endswith(
                "assistant"
            )
            and obj.__module__
            == module.__name__
        ):

            assistant_class = obj

            break


    if assistant_class is None:

        raise ImportError(

            f"\nCould not find an Assistant "
            f"class inside {module_name}.py"
        )


    print(
        f"Assistant class found: "
        f"{assistant_class.__name__}"
    )


    # --------------------------------------------------------
    # Create assistant object
    # --------------------------------------------------------

    assistant = assistant_class()


    # --------------------------------------------------------
    # Initialize RAG
    # --------------------------------------------------------

    if hasattr(
        assistant,
        "build"
    ):

        print(
            f"Initializing "
            f"{assistant_name} RAG..."
        )

        assistant.build()


    elif hasattr(
        assistant,
        "initialize"
    ):

        print(
            f"Initializing "
            f"{assistant_name} RAG..."
        )

        assistant.initialize()


    else:

        print(
            "No build() or initialize() "
            "method found."
        )


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

            "Assistant does not have "
            "an ask() method."
        )


    return assistant.ask(
        question
    )


# ============================================================
# EVALUATE ANSWER
# ============================================================

def evaluate_answer(
    question,
    expected_answer,
    actual_answer
):

    prompt = f"""
You are evaluating the answer produced by a banking RAG assistant.

Your task is to compare the ACTUAL ANSWER with the EXPECTED ANSWER.

QUESTION:
{question}

EXPECTED ANSWER:
{expected_answer}

ACTUAL ANSWER:
{actual_answer}


Classification rules:


1. correct

Use "correct" when the actual answer contains
the essential information required by the expected answer.

The wording does NOT need to be identical.

Extra relevant information is acceptable.


2. partial

Use "partial" when the actual answer contains
some correct information but misses an important
part of the expected answer.


3. incorrect

Use "incorrect" when:

- the answer contradicts the expected answer
- answers a different question
- provides unsupported information
- does not provide the required information
- says information could not be found when
  the expected answer contains the required information


Important rules:

- Judge semantic meaning.
- Do not judge writing style.
- Do not require exact wording.
- Do not reward an answer merely because it is long.
- Compare the actual answer with the expected answer.
- Be strict but fair.


Return ONLY valid JSON.

Required format:

{{
    "evaluation": "correct",
    "score": 1,
    "reason": "Short explanation"
}}


Scores:

correct = 1
partial = 0.5
incorrect = 0
"""


    # ========================================================
    # RETRY SETTINGS
    # ========================================================

    max_retries = 5

    base_wait = 10


    # ========================================================
    # EVALUATION API CALL
    # ========================================================

    for attempt in range(
        max_retries
    ):

        try:

            response = client.chat.completions.create(

                model=MODEL_NAME,

                messages=[

                    {
                        "role": "system",
                        "content": (
                            "You are a strict but fair "
                            "RAG evaluation judge. "
                            "Return only valid JSON."
                        )
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }

                ],

                temperature=0,

                max_tokens=300
            )


            content = (
                response
                .choices[0]
                .message
                .content
                .strip()
            )


            # ------------------------------------------------
            # Remove markdown code block if model returns it
            # ------------------------------------------------

            if content.startswith(
                "```"
            ):

                content = content.replace(
                    "```json",
                    ""
                )

                content = content.replace(
                    "```",
                    ""
                )

                content = content.strip()


            # ------------------------------------------------
            # Convert JSON string to Python dictionary
            # ------------------------------------------------

            evaluation = json.loads(
                content
            )


            return evaluation


        except Exception as e:

            error_text = str(e)


            # ------------------------------------------------
            # RATE LIMIT
            # ------------------------------------------------

            if (
                "rate limit"
                in error_text.lower()
                or "429"
                in error_text
            ):

                wait_time = (
                    base_wait
                    * (attempt + 1)
                )


                print(
                    "\nRate limit reached."
                )

                print(
                    f"Waiting {wait_time} seconds..."
                )


                time.sleep(
                    wait_time
                )


                continue


            # ------------------------------------------------
            # OTHER ERROR
            # ------------------------------------------------

            return {

                "evaluation":
                    "evaluation_error",

                "score":
                    None,

                "reason":
                    error_text
            }


    # ========================================================
    # RETRIES EXHAUSTED
    # ========================================================

    return {

        "evaluation":
            "evaluation_error",

        "score":
            None,

        "reason":
            (
                "Rate limit continued after "
                f"{max_retries} retries."
            )
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n")
    print("=" * 70)
    print("HDFC BANK RAG EVALUATION")
    print("=" * 70)


    # ========================================================
    # LOAD QUESTIONS
    # ========================================================

    questions = load_questions()


    total_questions = len(
        questions
    )


    print(
        f"\nTotal questions: "
        f"{total_questions}"
    )


    # ========================================================
    # ASSISTANT CACHE
    # ========================================================

    assistants = {}


    results = []


    # ========================================================
    # STATISTICS
    # ========================================================

    correct_count = 0

    partial_count = 0

    incorrect_count = 0

    evaluation_error_count = 0


    # ========================================================
    # PROCESS QUESTIONS
    # ========================================================

    for index, item in enumerate(
        questions,
        start=1
    ):

        assistant_name = item.get(
            "assistant",
            ""
        )


        question = item.get(
            "question",
            ""
        )


        expected_answer = item.get(
            "expected_answer",
            ""
        )


        source_url = item.get(
            "source_url",
            ""
        )


        print("\n")
        print("=" * 70)


        print(
            f"Question "
            f"{index}/{total_questions}"
        )


        print(
            f"Assistant: "
            f"{assistant_name}"
        )


        print(
            f"Question: "
            f"{question}"
        )


        # ====================================================
        # CREATE RESULT OBJECT
        # ====================================================

        result = dict(item)


        result["actual_answer"] = ""

        result["status"] = ""

        result["error"] = ""

        result["evaluation"] = ""

        result["score"] = None

        result["evaluation_reason"] = ""


        # ====================================================
        # LOAD ASSISTANT
        # ====================================================

        try:

            if assistant_name not in assistants:

                assistants[
                    assistant_name
                ] = load_assistant(
                    assistant_name
                )


            assistant = assistants[
                assistant_name
            ]


        except Exception as e:

            print(
                "\nERROR loading assistant:"
            )

            print(e)


            result[
                "status"
            ] = "error"


            result[
                "error"
            ] = str(e)


            results.append(
                result
            )


            # Save immediately
            with open(
                RESULTS_FILE,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    results,
                    f,
                    indent=4,
                    ensure_ascii=False
                )


            continue


        # ====================================================
        # ASK ASSISTANT
        # ====================================================

        try:

            actual_answer = ask_assistant(
                assistant,
                question
            )


            if actual_answer is None:

                actual_answer = ""


            actual_answer = str(
                actual_answer
            ).strip()


            result[
                "actual_answer"
            ] = actual_answer


            result[
                "status"
            ] = "completed"


            print(
                "\nActual Answer:"
            )


            print(
                actual_answer
            )


        except Exception as e:

            print(
                "\nERROR answering question:"
            )


            print(e)


            result[
                "status"
            ] = "error"


            result[
                "error"
            ] = str(e)


            results.append(
                result
            )


            # Save immediately
            with open(
                RESULTS_FILE,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    results,
                    f,
                    indent=4,
                    ensure_ascii=False
                )


            continue


        # ====================================================
        # EVALUATE ANSWER
        # ====================================================

        print(
            "\nEvaluating answer..."
        )


        evaluation = evaluate_answer(

            question,

            expected_answer,

            actual_answer
        )


        result[
            "evaluation"
        ] = evaluation.get(
            "evaluation",
            ""
        )


        result[
            "score"
        ] = evaluation.get(
            "score",
            None
        )


        result[
            "evaluation_reason"
        ] = evaluation.get(
            "reason",
            ""
        )


        # ====================================================
        # UPDATE STATISTICS
        # ====================================================

        if (
            result["evaluation"]
            == "correct"
        ):

            correct_count += 1


        elif (
            result["evaluation"]
            == "partial"
        ):

            partial_count += 1


        elif (
            result["evaluation"]
            == "incorrect"
        ):

            incorrect_count += 1


        else:

            evaluation_error_count += 1


        # ====================================================
        # PRINT EVALUATION
        # ====================================================

        print(
            "\nEvaluation:"
        )


        print(
            result["evaluation"]
        )


        print(
            f"Score: "
            f"{result['score']}"
        )


        print(
            "Reason:"
        )


        print(
            result["evaluation_reason"]
        )


        # ====================================================
        # SAVE RESULT
        # ====================================================

        results.append(
            result
        )


        with open(
            RESULTS_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                results,
                f,
                indent=4,
                ensure_ascii=False
            )


        # Small delay
        time.sleep(
            2
        )


    # ========================================================
    # FINAL STATISTICS
    # ========================================================

    evaluated_questions = (

        correct_count
        + partial_count
        + incorrect_count

    )


    if evaluated_questions > 0:

        exact_accuracy = (

            correct_count
            / evaluated_questions

        ) * 100


        effective_score = (

            (
                correct_count
                + (
                    partial_count
                    * 0.5
                )
            )
            / evaluated_questions

        ) * 100


    else:

        exact_accuracy = 0

        effective_score = 0


    # ========================================================
    # FINAL REPORT
    # ========================================================

    print("\n")
    print("=" * 70)
    print("RAG EVALUATION COMPLETED")
    print("=" * 70)


    print(
        f"Total questions       : "
        f"{total_questions}"
    )


    print(
        f"Correct               : "
        f"{correct_count}"
    )


    print(
        f"Partial               : "
        f"{partial_count}"
    )


    print(
        f"Incorrect             : "
        f"{incorrect_count}"
    )


    print(
        f"Evaluation errors     : "
        f"{evaluation_error_count}"
    )


    print(
        f"\nExact Accuracy        : "
        f"{exact_accuracy:.2f}%"
    )


    print(
        f"Effective Score       : "
        f"{effective_score:.2f}%"
    )


    print(
        "\nResults saved to:"
    )


    print(
        RESULTS_FILE
    )


    print("=" * 70)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()