"""Document Ingestion Module."""

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class DocumentChunk:
    """A chunk of a document."""

    id: str
    content: str
    source: str
    metadata: dict


class DocumentIngester:
    """Ingests documents and creates chunks for retrieval."""

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """Initialize ingester.

        Args:
            chunk_size: Target size of each chunk in characters
            chunk_overlap: Overlap between chunks in characters
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def _generate_id(self, content: str, source: str) -> str:
        """Generate unique ID for a chunk."""
        hash_input = f"{source}:{content[:100]}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:12]

    def chunk_text(self, text: str, source: str) -> list[DocumentChunk]:
        """Split text into overlapping chunks."""
        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size

            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence end within last 20% of chunk
                search_start = end - int(self.chunk_size * 0.2)
                for punct in [". ", "! ", "? ", "\n\n"]:
                    pos = text.rfind(punct, search_start, end)
                    if pos != -1:
                        end = pos + len(punct)
                        break

            chunk_content = text[start:end].strip()

            if chunk_content:
                chunk = DocumentChunk(
                    id=self._generate_id(chunk_content, source),
                    content=chunk_content,
                    source=source,
                    metadata={"start": start, "end": end},
                )
                chunks.append(chunk)

            start = end - self.chunk_overlap

        return chunks

    def ingest_file(self, path: Path) -> list[DocumentChunk]:
        """Ingest a single file."""
        text = path.read_text(encoding="utf-8")
        return self.chunk_text(text, source=str(path))

    def ingest_directory(self, directory: str) -> list[DocumentChunk]:
        """Ingest all text files in a directory."""
        path = Path(directory)
        all_chunks = []

        for file_path in path.rglob("*.txt"):
            chunks = self.ingest_file(file_path)
            all_chunks.extend(chunks)

        for file_path in path.rglob("*.md"):
            chunks = self.ingest_file(file_path)
            all_chunks.extend(chunks)

        return all_chunks

    def save_index(self, chunks: list[DocumentChunk], output_path: str) -> None:
        """Save chunks to index file."""
        path = Path(output_path)
        path.mkdir(parents=True, exist_ok=True)

        index_file = path / "chunks.jsonl"
        with open(index_file, "w", encoding="utf-8") as f:
            for chunk in chunks:
                f.write(json.dumps(asdict(chunk)) + "\n")

    @staticmethod
    def load_chunks(index_path: str) -> list[DocumentChunk]:
        """Load chunks from index file."""
        path = Path(index_path) / "chunks.jsonl"
        chunks = []

        with open(path, encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                chunks.append(DocumentChunk(**data))

        return chunks


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Ingest documents")
    parser.add_argument("--input", required=True, help="Input directory")
    parser.add_argument("--output", required=True, help="Output index directory")
    parser.add_argument("--chunk-size", type=int, default=500)
    parser.add_argument("--chunk-overlap", type=int, default=50)
    args = parser.parse_args()

    ingester = DocumentIngester(
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
    )

    chunks = ingester.ingest_directory(args.input)
    ingester.save_index(chunks, args.output)

    print(f"Ingested {len(chunks)} chunks")


if __name__ == "__main__":
    main()
