import requests
import os
import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
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



jsons = os.listdir("jsons")

chunk_id = 0
my_dict = []

for json_file in jsons:

    if not json_file.endswith(".json"):
        continue

    with open(f"jsons/{json_file}", "r") as f:
        content = json.load(f)

    chunks = content["chunks"]

    # Saare texts ek saath Ollama ko do
    texts = [chunk["text"] for chunk in chunks]

    embeddings = get_embedding(texts)

    for i, chunk in enumerate(chunks):
        chunk["chunk_id"] = chunk_id
        chunk_id += 1
        chunk["embedding"] = embeddings[i]
        my_dict.append(chunk)
        


df = pd.DataFrame.from_records(my_dict)
joblib.dump(df, 'chunk_embeddings.joblib')