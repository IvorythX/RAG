import fire
from src.process import process_file
from src.indexer import build_and_save_index


class RAGPipeline:
    """Retrieval-Augmented Generation CLI."""

    def index(self, max_chunk_size: int = 2000) -> None:
        """Ingest data/raw/ and build the index under data/processed/."""
        print(f"Starting indexer with max_chunk_size={max_chunk_size}...")
        documents = process_file(raw_path="data/raw")

        if not documents:
            print("No files found in data/raw/ to index.")
            return

        build_and_save_index(documents, processed_dir="data/processed")

    def search(self, query: str, k: int) -> None:
        """Return the top-k sources for a single query."""
        pass

    def search_dataset(
        self, dataset_path: str, k: int, save_directory: str
    ) -> None:
        """Run search over a whole dataset and write a
        StudentSearchResults JSON file."""
        pass

    def answer(self, query: str, k: int) -> None:
        """Answer a single query using the retrieved context."""
        pass

    def answer_dataset(
        self, student_search_results_path: str, save_directory: str
    ) -> None:
        """Generate answers for a dataset, producing a
        StudentSearchResultsAndAnswer JSON file."""
        pass

    def evaluate(
            self, student_search_results_path: str, dataset_path: str
    ) -> None:
        """Report your own recall@k against a ground-truth dataset."""
        pass


def main() -> None:
    fire.Fire(RAGPipeline)


if __name__ == '__main__':
    main()
