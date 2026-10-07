import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import requests
import joblib


def get_embedding(text_list):
    response = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "bge-m3",
            "input": text_list
        }
    )

    data = response.json()
    return data["embeddings"]


def inference(prompt):
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 200
            }
        }
    )

    data = r.json()

    # actual generated answer
    return data["response"]


# ---------------- LOAD EMBEDDINGS ----------------

df = joblib.load("chunk_embeddings.joblib")

incoming_query = input("Enter your query: ")


# ---------------- QUERY EMBEDDING ----------------

query_embedding = get_embedding([incoming_query])[0]

print("\nQUERY EMBEDDING SHAPE:")
print(np.array(query_embedding).shape)


# ---------------- CHUNK EMBEDDINGS ----------------

chunk_embeddings = np.vstack(df["embedding"].values)

print("\nCHUNK EMBEDDINGS SHAPE:")
print(chunk_embeddings.shape)


# ---------------- COSINE SIMILARITY ----------------

similarities = cosine_similarity(
    chunk_embeddings,
    np.array(query_embedding).reshape(1, -1)
)

similarities = similarities.flatten()

print("\nSIMILARITIES:")

topvalue = 5

max_simi = similarities.argsort()[::-1][:topvalue]

print(max_simi)


# ---------------- TOP 5 CHUNKS ----------------

new_df = df.iloc[max_simi]

new_df = new_df[
    ["text", "chunk_id", "title", "start", "end"]
]


# ---------------- LLM PROMPT ----------------
prompt = f"""
You are a video search assistant.

The user asked:
"{incoming_query}"

Here are the relevant video chunks:
{new_df.to_json(orient="records")}

Your task:
- Identify the most relevant chunk.
- Return ONLY one very short instruction.
- Do NOT mention timestamps.
- Do NOT calculate timestamps.
- Do NOT write Python code.
- Do NOT invent information.
- Use only information explicitly present in the chunks.

If the chunks are not relevant, return exactly:
Not able to find relevant information in the provided videos.

Otherwise return something like:
Go to the section where CSS is taught.
"""

# ---------------- GENERATE RESPONSE ----------------
response = inference(prompt)

if response.strip() == "Not able to find relevant information in the provided videos.":
    final_response = response
else:
    best_chunk = new_df.iloc[0]

    def format_timestamp(seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    title = best_chunk["title"]
    timestamp = format_timestamp(best_chunk["start"])

    final_response = f"""Video Title: {title}
Timestamp: {timestamp}
{response}"""

print("\nFINAL RESPONSE:")
print(final_response)

with open("response.txt", "w") as f:
    f.write(final_response)