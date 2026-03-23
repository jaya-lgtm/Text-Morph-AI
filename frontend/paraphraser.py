from transformers import pipeline
import streamlit as st

@st.cache_resource
def load_paraphraser():
    return pipeline(
        "text2text-generation",
        model="Vamsi/T5_Paraphrase_Paws",  # fine-tuned specifically for paraphrasing, much better than t5-small
        device=-1  # CPU; change to 0 if you have GPU
    )

def split_text(text, max_words=100):
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunks.append(" ".join(words[i:i + max_words]))
    return chunks

def paraphrase_text(text, level):
    paraphraser = load_paraphraser()

    # Adjust beam width by level — fewer beams = faster
    if level == "Beginner":
        num_beams = 2
        max_length = 128
    elif level == "Intermediate":
        num_beams = 3
        max_length = 150
    else:  # Advanced
        num_beams = 4
        max_length = 180

    chunks = split_text(text)

    # Cap chunks to keep it fast
    chunks = chunks[:4]

    results = []
    for chunk in chunks:
        if len(chunk.split()) < 5:
            results.append(chunk)
            continue

        prompt = f"paraphrase: {chunk} </s>"

        output = paraphraser(
            prompt,
            max_length=max_length,
            num_beams=num_beams,
            early_stopping=True,
            truncation=True
        )
        results.append(output[0]["generated_text"])

    return " ".join(results)