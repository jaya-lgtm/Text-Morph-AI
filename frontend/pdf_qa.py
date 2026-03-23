from transformers import pipeline
import streamlit as st

@st.cache_resource
def load_qa_pipeline():
    return pipeline(
        "question-answering",
        model="deepset/roberta-base-squad2"
    )

def split_into_chunks(text, chunk_size=400, overlap=50):
    """Split text into overlapping chunks so answers near boundaries aren't missed."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap  # overlap so boundary answers aren't lost
    return chunks


def answer_question(context, question):
    if not context.strip() or not question.strip():
        return "Please provide both text and a question."

    qa_pipeline = load_qa_pipeline()
    chunks = split_into_chunks(context, chunk_size=400, overlap=50)

    best_answer = ""
    best_score = 0.0

    for chunk in chunks:
        try:
            result = qa_pipeline({
                "context": chunk,
                "question": question
            })
            # Pick the chunk whose answer has the highest confidence score
            if result["score"] > best_score:
                best_score = result["score"]
                best_answer = result["answer"]
        except Exception:
            continue

    if best_score < 0.20:
        return "This information is not mentioned in the provided text."

    return best_answer