from typing import List

def chunk_lines(
    lines: List[str],
    max_lines: int = 20,
    overlap: int = 5
) -> List[str]:
    """
    Convert a list of log lines into overlapping text chunks.

    Example:
      lines = ["Step 0", "Step 1", ..., "Step 100"]
      max_lines = 20
      overlap = 5
    """
    chunks = []
    start = 0
    n = len(lines)

    while start < n:
        end = min(n, start + max_lines)
        chunk = "\n".join(lines[start:end])
        chunks.append(chunk)

        # next window starts earlier (overlap)
        start = end - overlap
        if start < 0:
            start = 0

        if end == n:
            break

    return chunks
