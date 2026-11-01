from pathlib import Path
from .chunker import chunk_python, chunks_index, chunk_markdown


def process_file(raw_path: str = "data/raw") -> list[dict]:
    documents = []
    base_path = Path(raw_path)
    for file_path in base_path.rglob("*"):
        if not file_path.is_file():
            continue
        if file_path.suffix not in ['.py', '.md']:
            continue
        try:
            text = file_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Skipping {file_path} due to read error: {e}")
            continue
        if file_path.suffix == '.py':
            chunks = chunk_python(text)
        else:
            chunks = chunk_markdown(text)
        spans = chunks_index(chunks, text)
        str_path = str(file_path)
        for chunk, (start, end) in zip(chunks, spans):
            documents.append({
                "file_path": str_path,
                "text": chunk,
                "first_character_index": start,
                "last_character_index": end
            })

    return documents
