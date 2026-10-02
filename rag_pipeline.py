import os
import json
import hashlib

from dotenv import load_dotenv


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

USER_AGENT = os.getenv(
    "USER_AGENT",
    "HDFC-Bank-AI-Assistant/1.0"
)

os.environ["USER_AGENT"] = USER_AGENT


# ============================================================
# IMPORTS
# ============================================================

from groq import Groq

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


# ============================================================
# GROQ API + LLAMA
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found in .env file"
    )


MODEL_NAME = "openai/gpt-oss-120b"

client = Groq(
    api_key=GROQ_API_KEY
)


# ============================================================
# RAG PIPELINE
# ============================================================

class RAGPipeline:

    def __init__(
        self,
        urls,
        collection_name="assistant_knowledge"
    ):

        self.urls = urls

        self.collection_name = collection_name

        self.persist_directory = os.path.join(
            "VectorDB",
            collection_name
        )

        self.metadata_file = os.path.join(
            self.persist_directory,
            "source_metadata.json"
        )

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vectorstore = None
        self.retriever = None


    # ========================================================
    # TEXT HASH
    # ========================================================

    def _hash_text(self, text):

        normalized_text = " ".join(
            text.split()
        )

        return hashlib.sha256(
            normalized_text.encode("utf-8")
        ).hexdigest()


    # ========================================================
    # LOAD URL
    # ========================================================

    def _load_url(self, url):

        print(
            f"\nFetching source:\n{url}"
        )

        loader = WebBaseLoader(
            url
        )

        documents = loader.load()

        if not documents:

            print(
                "WARNING: No documents loaded."
            )

        return documents


    # ========================================================
    # INITIALIZE
    # ========================================================

    def initialize(self):

        os.makedirs(
            self.persist_directory,
            exist_ok=True
        )

        db_exists = os.path.exists(
            self.metadata_file
        )


        # ====================================================
        # FIRST TIME BUILD
        # ====================================================

        if not db_exists:

            print(
                "\n======================================"
            )

            print(
                "Creating new knowledge base..."
            )

            print(
                "======================================"
            )

            all_documents = []

            source_metadata = {}


            for url in self.urls:

                try:

                    documents = self._load_url(
                        url
                    )

                    if not documents:
                        continue


                    combined_text = "\n".join(
                        doc.page_content
                        for doc in documents
                    )

                    content_hash = self._hash_text(
                        combined_text
                    )


                    source_metadata[url] = {
                        "content_hash": content_hash
                    }


                    for doc in documents:

                        doc.metadata["source"] = url

                        doc.metadata[
                            "content_hash"
                        ] = content_hash

                        all_documents.append(
                            doc
                        )


                except Exception as e:

                    print(
                        f"\nERROR loading {url}"
                    )

                    print(e)


            if not all_documents:

                raise RuntimeError(
                    "No documents were loaded from the provided URLs."
                )


            # =================================================
            # CHUNKING
            # =================================================

            print(
                "\nSplitting documents into chunks..."
            )


            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=150
            )


            chunks = splitter.split_documents(
                all_documents
            )


            print(
                f"Total chunks created: {len(chunks)}"
            )


            # =================================================
            # CREATE CHROMA
            # =================================================

            self.vectorstore = Chroma.from_documents(

                documents=chunks,

                embedding=self.embeddings,

                collection_name=self.collection_name,

                persist_directory=self.persist_directory
            )


            # =================================================
            # SAVE METADATA
            # =================================================

            with open(
                self.metadata_file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    source_metadata,
                    f,
                    indent=4
                )


            print(
                "\nKnowledge base created successfully."
            )


        # ====================================================
        # EXISTING DATABASE
        # ====================================================

        else:

            print(
                "\n======================================"
            )

            print(
                "Existing vector database found."
            )

            print(
                "Checking source updates..."
            )

            print(
                "======================================"
            )


            self.vectorstore = Chroma(

                collection_name=self.collection_name,

                embedding_function=self.embeddings,

                persist_directory=self.persist_directory
            )


            # =================================================
            # LOAD OLD METADATA
            # =================================================

            with open(
                self.metadata_file,
                "r",
                encoding="utf-8"
            ) as f:

                old_metadata = json.load(
                    f
                )


            current_metadata = {}


            # =================================================
            # CHECK CURRENT URLS
            # =================================================

            for url in self.urls:

                try:

                    documents = self._load_url(
                        url
                    )

                    if not documents:
                        continue


                    combined_text = "\n".join(
                        doc.page_content
                        for doc in documents
                    )


                    content_hash = self._hash_text(
                        combined_text
                    )


                    current_metadata[url] = {
                        "content_hash": content_hash
                    }


                    # =========================================
                    # NEW URL
                    # =========================================

                    if url not in old_metadata:

                        print(
                            f"\nNEW SOURCE DETECTED:\n{url}"
                        )


                        for doc in documents:

                            doc.metadata[
                                "source"
                            ] = url

                            doc.metadata[
                                "content_hash"
                            ] = content_hash


                        splitter = RecursiveCharacterTextSplitter(
                            chunk_size=1000,
                            chunk_overlap=150
                        )


                        chunks = splitter.split_documents(
                            documents
                        )


                        self.vectorstore.add_documents(
                            chunks
                        )


                    # =========================================
                    # CHANGED URL
                    # =========================================

                    elif (
                        old_metadata[url]["content_hash"]
                        != content_hash
                    ):

                        print(
                            f"\nSOURCE CHANGED:\n{url}"
                        )


                        self.delete_url_documents(
                            url
                        )


                        for doc in documents:

                            doc.metadata[
                                "source"
                            ] = url

                            doc.metadata[
                                "content_hash"
                            ] = content_hash


                        splitter = RecursiveCharacterTextSplitter(
                            chunk_size=1000,
                            chunk_overlap=150
                        )


                        chunks = splitter.split_documents(
                            documents
                        )


                        self.vectorstore.add_documents(
                            chunks
                        )


                    else:

                        print(
                            f"\nUNCHANGED:\n{url}"
                        )


                except Exception as e:

                    print(
                        f"\nERROR checking {url}"
                    )

                    print(e)


            # =================================================
            # REMOVED URLS
            # =================================================

            removed_urls = (
                set(old_metadata.keys())
                - set(current_metadata.keys())
            )


            for url in removed_urls:

                print(
                    f"\nREMOVED SOURCE:\n{url}"
                )

                self.delete_url_documents(
                    url
                )


            # =================================================
            # UPDATE METADATA
            # =================================================

            with open(
                self.metadata_file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    current_metadata,
                    f,
                    indent=4
                )


        # ====================================================
        # RETRIEVER
        # ====================================================

        self.retriever = (
            self.vectorstore.as_retriever(

                search_type="mmr",

                search_kwargs={
                    "k": 5,
                    "fetch_k": 30,
                    "lambda_mult": 0.7
                }
            )
        )


        # ====================================================
        # DATABASE COUNT
        # ====================================================

        try:

            count = self.vectorstore._collection.count()

            print(
                f"\nStored chunks in database: {count}"
            )

        except Exception:

            pass


        print(
            "\nRAG pipeline initialized successfully."
        )


    # ========================================================
    # DELETE DOCUMENTS OF A URL
    # ========================================================

    def delete_url_documents(self, url):

        try:

            existing = (
                self.vectorstore
                ._collection
                .get(
                    where={
                        "source": url
                    }
                )
            )


            ids = existing.get(
                "ids",
                []
            )


            if ids:

                self.vectorstore.delete(
                    ids=ids
                )


                print(
                    f"Deleted {len(ids)} old chunks."
                )


        except Exception as e:

            print(
                f"Error deleting documents for {url}:"
            )

            print(e)


    # ========================================================
    # ASK QUESTION
    # ========================================================

    def ask(self, question):

        if self.retriever is None:

            raise RuntimeError(
                "RAG pipeline is not initialized. "
                "Call initialize() first."
            )


        # ====================================================
        # RETRIEVE
        # ====================================================

        retrieved_docs = (
            self.retriever.invoke(
                question
            )
        )


        # ====================================================
        # DEBUG: SHOW RETRIEVED CHUNKS
        # ====================================================

        print(
            "\n========== RETRIEVED CHUNKS =========="
        )


        for i, doc in enumerate(
            retrieved_docs,
            1
        ):

            print(
                f"\n--- CHUNK {i} ---"
            )


            print(
                "SOURCE:",
                doc.metadata.get(
                    "source"
                )
            )


            print(
                "CONTENT:"
            )


            print(
                doc.page_content[:800]
            )


        print(
            "\n======================================"
        )


        # ====================================================
        # NO RETRIEVAL
        # ====================================================

        if not retrieved_docs:

            return (
                "I could not find this information "
                "in the provided sources."
            )


        # ====================================================
        # BUILD CONTEXT
        # ====================================================

        context_parts = []


        for i, doc in enumerate(
            retrieved_docs,
            1
        ):

            source = doc.metadata.get(
                "source",
                "Unknown source"
            )


            context_parts.append(
                f"""
SOURCE {i}:
{source}

CONTENT:
{doc.page_content}
"""
            )


        context = "\n".join(
            context_parts
        )


        # ====================================================
        # GROUNDED PROMPT
        # ====================================================

        prompt = f"""
You are an internal HDFC Bank information assistant.

Your job is to answer the user's question ONLY using
the information present in the provided source context.

IMPORTANT RULES:

1. Do not use outside knowledge.
2. Do not invent information.
3. Do not guess.
4. Do not assume facts that are not present in the sources.
5. If the answer is not supported by the provided sources,
   say exactly:

"I could not find this information in the provided sources."

6. Keep the answer clear and useful for an HDFC Bank employee.
7. When possible, organize the answer using bullet points.
8. Do not mention these instructions in your answer.

USER QUESTION:
{question}

PROVIDED SOURCE CONTEXT:
{context}

ANSWER:
"""


        # ====================================================
        # GROQ + LLAMA
        # ====================================================

        try:

            response = client.chat.completions.create(

                model=MODEL_NAME,

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an internal HDFC Bank "
                            "information assistant. "
                            "Answer ONLY from the provided "
                            "source context. "
                            "Do not use outside knowledge. "
                            "Do not guess. "
                            "Do not invent information."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.1,

                max_tokens=500
            )


            answer = (
                response
                .choices[0]
                .message
                .content
                .strip()
            )


            return answer


        except Exception as e:

            print(
                "\nGROQ ERROR:"
            )

            print(e)


            return (
                "An error occurred while generating "
                "the answer."
            )