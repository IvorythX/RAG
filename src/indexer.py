import pickle
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer


def build_and_save_index(documents: list[dict], processed_dir: dir = "data/processed") -> None:
    Path(processed_dir).mkdir(parents=True, exist_ok=True)
    texts = [doc["text"] for doc in documents]
    vectorizer = TfidfVectorizer(lowercase=True)
    tfidf_matrix = vectorizer.fit_transform(texts)
    index_data = {
        "vectorizer": vectorizer,
        "matrix": tfidf_matrix,
        "documents": documents
    }
    index_path = Path(processed_dir) / "tfidf_index.pkl"
    with open(index_path, 'wb') as f:
        pickle.dump(index_data, f)
    print(
        f"Ingestion complete! Indexed {len(documents)} chunks under "
        f"{processed_dir}/")
