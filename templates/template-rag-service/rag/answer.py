"""Answer Generation Module."""

from dataclasses import dataclass

from rag.retrieve import RetrievalResult, Retriever


@dataclass
class Answer:
    """Generated answer with sources."""

    text: str
    sources: list[str]
    context_used: list[str]


class MockLLM:
    """Mock LLM for demonstration.

    Replace with real LLM:
    - OpenAI GPT
    - Anthropic Claude
    - Local model via Ollama
    """

    def generate(self, prompt: str) -> str:
        """Generate mock response."""
        # Extract question from prompt
        if "Question:" in prompt:
            question = prompt.split("Question:")[-1].split("\n")[0].strip()
        else:
            question = "the question"

        return f"Based on the provided context, {question.lower().rstrip('?')} is explained in the documents. This is a mock response - integrate a real LLM for actual answers."


class RAGPipeline:
    """RAG Pipeline combining retrieval and generation."""

    def __init__(
        self,
        retriever: Retriever,
        llm: MockLLM | None = None,
        top_k: int = 3,
    ):
        """Initialize RAG pipeline."""
        self.retriever = retriever
        self.llm = llm or MockLLM()
        self.top_k = top_k

    def _build_prompt(self, query: str, results: list[RetrievalResult]) -> str:
        """Build prompt with context."""
        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(
                f"[{i}] {result.content}\nSource: {result.source}"
            )

        context = "\n\n".join(context_parts)

        prompt = f"""Use the following context to answer the question. If you cannot answer from the context, say so.

Context:
{context}

Question: {query}

Answer:"""

        return prompt

    def answer(self, query: str) -> Answer:
        """Generate answer for query."""
        # Retrieve relevant chunks
        results = self.retriever.search(query, top_k=self.top_k)

        # Build prompt with context
        prompt = self._build_prompt(query, results)

        # Generate answer
        response = self.llm.generate(prompt)

        # Extract sources
        sources = list(set(r.source for r in results))
        context_used = [r.content[:200] + "..." for r in results]

        return Answer(
            text=response,
            sources=sources,
            context_used=context_used,
        )


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Query RAG system")
    parser.add_argument("--index", default="./index", help="Index directory")
    parser.add_argument("--query", required=True, help="Query string")
    parser.add_argument("--top-k", type=int, default=3, help="Number of results")
    args = parser.parse_args()

    retriever = Retriever.load(args.index)
    rag = RAGPipeline(retriever=retriever, top_k=args.top_k)

    answer = rag.answer(args.query)

    print(f"Answer: {answer.text}\n")
    print("Sources:")
    for source in answer.sources:
        print(f"  - {source}")


if __name__ == "__main__":
    main()
