from transformers import pipeline
import streamlit as st

# Cache the model so it loads only once across reruns
@st.cache_resource
def load_summarizer():
    return pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6",  # 4x faster than bart-large-cnn, nearly same quality
        device=-1  # CPU; change to 0 if you have GPU
    )

def split_text(text, max_words=350):
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunks.append(" ".join(words[i:i + max_words]))
    return chunks

def generate_summary(text, level):
    summarizer = load_summarizer()

    if level == "Short":
        max_len, min_len = 60, 20
    elif level == "Medium":
        max_len, min_len = 120, 40
    else:
        max_len, min_len = 200, 60

    chunks = split_text(text)

    # For long docs, only summarize first 3 chunks to keep it fast
    chunks = chunks[:3]

    summaries = []
    for chunk in chunks:
        # Skip chunks that are too short to summarize
        if len(chunk.split()) < 30:
            summaries.append(chunk)
            continue
        result = summarizer(
            chunk,
            max_length=max_len,
            min_length=min_len,
            do_sample=False,
            truncation=True
        )
        summaries.append(result[0]["summary_text"])

    return " ".join(summaries)