import re


def chunk_markdown(text: str, max_chunk_size: int = 2000) -> list[str]:
    """Split Markdown text by headers and paragraphs.

    Strictly respects ``max_chunk_size``.
    """
    chunks = []
    current_chunk = ""

    sections = re.split(r'(?=\n# )', text)

    for section in sections:
        section = section.strip()
        if not section:
            continue

        if len(section) > max_chunk_size:
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""
            paragraphs = section.split('\n\n')
            for para in paragraphs:
                para = para.strip()
                if len(para) > max_chunk_size:
                    if current_chunk:
                        chunks.append(current_chunk)
                        current_chunk = ""
                    for i in range(0, len(para), max_chunk_size):
                        chunks.append(para[i:i + max_chunk_size])
                elif len(current_chunk) + len(para) + 2 <= max_chunk_size:
                    current_chunk += ("\n\n" if current_chunk else "") + para
                else:
                    if current_chunk:
                        chunks.append(current_chunk)
                    current_chunk = para
        elif len(current_chunk) + len(section) + 2 <= max_chunk_size:
            current_chunk += ("\n\n" if current_chunk else "") + section
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = section

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def chunk_python(text: str, max_chunk_size: int = 2000) -> list[str]:
    chunks = []
    currrent_chunk = ""
    sections = re.split(r'(?=\n(?:class|def|async def)\s)', text)
    for section in sections:
        section = section.strip()
        if not section:
            continue
        if len(section) > max_chunk_size:
            if currrent_chunk:
                chunks.append(currrent_chunk)
                currrent_chunk = ""
            blocks = section.split("\n\n")
            for block in blocks:
                block = block.strip()
                if len(block) > max_chunk_size:
                    if currrent_chunk:
                        chunks.append(currrent_chunk)
                        currrent_chunk = ""
                    for i in range(0, len(block), max_chunk_size):
                        chunks.append(block[i: i + max_chunk_size])
                elif len(currrent_chunk) + len(block) + 2 <= max_chunk_size:
                    currrent_chunk += (
                        ("\n\n" if currrent_chunk else "") + block
                    )
                else:
                    if currrent_chunk:
                        chunks.append(currrent_chunk)
                    currrent_chunk = block
        elif len(currrent_chunk) + len(section) + 2 <= max_chunk_size:
            currrent_chunk += ("\n\n" if currrent_chunk else "") + section
        else:
            if currrent_chunk:
                chunks.append(currrent_chunk)
            currrent_chunk = section
    if currrent_chunk:
        chunks.append(currrent_chunk)

    return chunks


def chunks_index(chunks: list[str], text: str) -> list[tuple[int, int]]:
    indexs = []
    start = 0
    for chunk in chunks:
        start_idx = text.find(chunk, start)
        end_idx = start_idx + len(chunk)
        indexs.append((start_idx, end_idx))
        start = end_idx
    return indexs


# # Add this to the bottom of src/chunker.py
# if __name__ == "__main__":
#     sample_md = """# Introduction
# Welcome to the vLLM documentation.

# # Configuration
# To set up the server, you need to configure the environment variables correctly.
# Ensure your API keys are secure.

# # Deep Dive
# """ + (
#         "This is a very long sentence designed to force the paragraph splitter "
#         "to engage. " * 5
#     ) + """

# # Conclusion
# That covers the basic setup."""

#     # Using a small limit of 200 to test the fallbacks
#     results = chunk_markdown(sample_md, max_chunk_size=200)

#     for idx, chunk in enumerate(results):
#         print(f"--- Chunk {idx + 1} (Size: {len(chunk)}) ---")
#         print(repr(chunk))

if __name__ == "__main__":
    sample_py = """import os
import sys

def initialize_server():
    print("Starting server...")
    return True

class Handler:
""" + ("    # This is a very long loop that simulates a massive block of code inside a class.\n" * 5) + """
def cleanup():
    print("Done")
"""
    results = chunk_python(sample_py, max_chunk_size=150)

    for idx, chunk in enumerate(results):
        print(f"--- Chunk {idx + 1} (Size: {len(chunk)}) ---")
        print(repr(chunk))
    print(chunks_index(results, sample_py))
