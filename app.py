# Create a streamlit UI for text2sql usecase, write code similar to chatbot.ipynb to process the user query and show the results in a table format.

import streamlit as st
import os
from dotenv import load_dotenv # handle environment variables
from sqlalchemy import create_engine

from llama_index.core import SQLDatabase, VectorStoreIndex, Settings
from llama_index.core.objects import SQLTableNodeMapping, ObjectIndex, SQLTableSchema
from llama_index.core.query_engine import SQLTableRetrieverQueryEngine
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

load_dotenv()
hf_token = os.getenv("HF_TOKEN")


query_wrapper_prompt = (
    "### Instruction: Generate a SQL query that can answer the following question. "
    "Use complex JOINS and aliases where ever necessary.\n"
    "### Question: {query_str}\n"
    "### SQL Query:"
)

# setting up the thinker that writes sql
Settings.llm = HuggingFaceLLM(
    model_name="Qwen/Qwen2.5-Coder-7B-Instruct",
    tokenizer_name="Qwen/Qwen2.5-Coder-7B-Instruct",
    query_wrapper_prompt=query_wrapper_prompt,
    context_window=1024,
    max_new_tokens=256,
    model_kwargs={
        "token": hf_token,
        "trust_remote_code": True,
        "dtype":torch.bfloat16,
        "load_in_4bit": True,
        },
    generate_kwargs={"temperature": 0.1, "do_sample": False},
    device_map="auto",
)

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

engine = create_engine("sqlite:///employee.db")
sql_database = SQLDatabase(engine)

table_node_mapping = SQLTableNodeMapping(sql_database)
table_schema_objs = [
    SQLTableSchema(table_name=name)
    for name in sql_database.get_usable_table_names()
]

obj_index = ObjectIndex.from_objects(
    table_schema_objs, 
    table_node_mapping,
    VectorStoreIndex
)


query_engine = SQLTableRetrieverQueryEngine(
    sql_database, 
    obj_index.as_retriever(similarity_top_k=5)
)

def ask_chatbot(question:str):
    """Query the SQLTableRetrieverQueryEngine and return SQL + answer.

    Returns a tuple (sql_query, answer_text) on success, or (None, error_msg) on failure.
    """
    try:
        response = query_engine.query(question)
        sql = response.metadata.get("sql_query") if response.metadata else None
        answer = getattr(response, "response", None)
        if answer is None:
            # fallback to string representation
            answer = str(response)
        return sql, answer
    except Exception as e:
        return None, f"Error executing query: {e}"


if __name__ == "__main__":
    # Streamlit app entry - when run with `streamlit run app.py` this block will execute
    st.set_page_config(page_title="Text2SQL Chatbot", layout="wide")
    st.title("Text2SQL Chatbot")

    st.markdown("Enter a natural language question about the database and click **Ask**.")

    user_question = st.text_area("Your question", height=120)
    if st.button("Ask"):
        if not user_question or user_question.strip() == "":
            st.warning("Please enter a question before submitting.")
        else:
            with st.spinner("Generating SQL and fetching results..."):
                sql, answer = ask_chatbot(user_question)

            if sql:
                with st.expander("Generated SQL", expanded=True):
                    st.code(sql)

            st.subheader("Answer")
            # If answer looks like a tabular result, Streamlit will render it nicely when possible.
            try:
                # attempt to display as table if it's a list of dicts or similar
                if isinstance(answer, (list, tuple)):
                    st.table(answer)
                else:
                    st.write(answer)
            except Exception:
                st.write(str(answer))


