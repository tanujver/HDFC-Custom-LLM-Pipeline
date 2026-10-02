import os
import sys
import json
import importlib
import inspect


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

    sys.path.insert(
        0,
        BASE_DIR
    )


# ============================================================
# FILE PATHS
# ============================================================

RESULTS_FILE = os.path.join(
    EVALUATION_DIR,
    "evaluation_results.json"
)

OUTPUT_FILE = os.path.join(
    EVALUATION_DIR,
    "debug_retrieval_results.json"
)


# ============================================================
# LOAD EVALUATION RESULTS
# ============================================================

def load_results():

    if not os.path.exists(
        RESULTS_FILE
    ):

        raise FileNotFoundError(
            f"Evaluation results not found:\n"
            f"{RESULTS_FILE}"
        )


    with open(
        RESULTS_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        results = json.load(f)


    if not isinstance(
        results,
        list
    ):

        raise ValueError(
            "evaluation_results.json "
            "must contain a JSON list."
        )


    return results


# ============================================================
# LOAD ASSISTANT
# ============================================================

def load_assistant(
    assistant_name
):

    module_name = (
        assistant_name
        .lower()
        .strip()
        .replace(" ", "_")
        .replace("-", "_")
    )


    if not module_name.endswith(
        "_assistant"
    ):

        module_name += "_assistant"


    print(
        f"\nLoading assistant: "
        f"{module_name}"
    )


    try:

        module = importlib.import_module(
            module_name
        )

    except Exception as e:

        raise ImportError(
            f"Could not import "
            f"{module_name}.py\n\n"
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

        if name == "RAGPipeline":
            continue


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
            f"No Assistant class found "
            f"inside {module_name}.py"
        )


    print(
        f"Assistant class: "
        f"{assistant_class.__name__}"
    )


    # --------------------------------------------------------
    # Create assistant
    # --------------------------------------------------------

    assistant = assistant_class()


    # --------------------------------------------------------
    # Initialize RAG
    # --------------------------------------------------------

    if hasattr(
        assistant,
        "build"
    ):

        assistant.build()


    elif hasattr(
        assistant,
        "initialize"
    ):

        assistant.initialize()


    else:

        raise AttributeError(
            f"{assistant_class.__name__} "
            f"does not have build() "
            f"or initialize()."
        )


    return assistant


# ============================================================
# FIND RAG PIPELINE
# ============================================================

def get_rag_pipeline(
    assistant
):

    # Most likely
    if hasattr(
        assistant,
        "rag"
    ):

        return assistant.rag


    # Alternative names
    if hasattr(
        assistant,
        "pipeline"
    ):

        return assistant.pipeline


    if hasattr(
        assistant,
        "rag_pipeline"
    ):

        return assistant.rag_pipeline


    raise AttributeError(
        "Could not find RAG pipeline "
        "inside assistant."
    )


# ============================================================
# RETRIEVE CHUNKS
# ============================================================

def retrieve_chunks(
    assistant,
    question
):

    rag = get_rag_pipeline(
        assistant
    )


    docs = rag.retrieve_chunks(
        question
    )


    chunks = []


    for rank, doc in enumerate(
        docs,
        start=1
    ):

        chunks.append({

            "rank": rank,

            "source": doc.metadata.get(
                "source",
                ""
            ),

            "content": doc.page_content

        })


    return chunks


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n")
    print("=" * 70)
    print("HDFC BANK RAG RETRIEVAL DEBUGGER")
    print("=" * 70)


    # ========================================================
    # LOAD RESULTS
    # ========================================================

    results = load_results()


    print(
        f"\nTotal evaluation results: "
        f"{len(results)}"
    )


    # ========================================================
    # FILTER INCORRECT
    # ========================================================

    incorrect_results = [

        item

        for item in results

        if item.get(
            "evaluation"
        ) == "incorrect"

    ]


    print(
        f"Incorrect questions found: "
        f"{len(incorrect_results)}"
    )


    if not incorrect_results:

        print(
            "\nNo incorrect questions found."
        )

        return


    # ========================================================
    # ASSISTANT CACHE
    # ========================================================

    assistants = {}


    debug_results = []


    # ========================================================
    # PROCESS INCORRECT QUESTIONS
    # ========================================================

    for index, item in enumerate(
        incorrect_results,
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


        print("\n")
        print("-" * 70)


        print(
            f"Debugging "
            f"{index}/{len(incorrect_results)}"
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
        # RESULT OBJECT
        # ====================================================

        debug_item = {

            "assistant":
                assistant_name,

            "question":
                question,

            "expected_answer":
                item.get(
                    "expected_answer",
                    ""
                ),

            "actual_answer":
                item.get(
                    "actual_answer",
                    ""
                ),

            "evaluation":
                item.get(
                    "evaluation",
                    ""
                ),

            "evaluation_reason":
                item.get(
                    "evaluation_reason",
                    ""
                ),

            "retrieved_chunks":
                []

        }


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
                "\nAssistant loading error:"
            )

            print(e)


            debug_item[
                "retrieval_error"
            ] = str(e)


            debug_results.append(
                debug_item
            )

            continue


        # ====================================================
        # RETRIEVE
        # ====================================================

        try:

            chunks = retrieve_chunks(
                assistant,
                question
            )


            debug_item[
                "retrieved_chunks"
            ] = chunks


            print(
                f"\nRetrieved "
                f"{len(chunks)} chunks."
            )


            # ------------------------------------------------
            # Print chunks
            # ------------------------------------------------

            for chunk in chunks:

                print("\n")
                print(
                    f"CHUNK "
                    f"{chunk['rank']}"
                )


                print(
                    "SOURCE:",
                    chunk["source"]
                )


                print(
                    "CONTENT:"
                )


                print(
                    chunk["content"][:500]
                )


        except Exception as e:

            print(
                "\nRetrieval error:"
            )

            print(e)


            debug_item[
                "retrieval_error"
            ] = str(e)


        # ====================================================
        # SAVE RESULT
        # ====================================================

        debug_results.append(
            debug_item
        )


        with open(
            OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                debug_results,
                f,
                indent=4,
                ensure_ascii=False
            )


    # ========================================================
    # FINAL
    # ========================================================

    print("\n")
    print("=" * 70)


    print(
        "RETRIEVAL DEBUG COMPLETED"
    )


    print(
        f"Incorrect questions analyzed: "
        f"{len(debug_results)}"
    )


    print(
        "\nDebug results saved to:"
    )


    print(
        OUTPUT_FILE
    )


    print("=" * 70)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()