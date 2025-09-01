import pathlib as Path

def tail(self, path: Path, lines: int = 5, _buffer: int = 4098) -> list[str]:
    """Tail a file and get X lines from the end efficiently."""
    lines_found = []
    block_counter = -1

    with path.open("rb") as f:  # open in binary mode for precise seek
        while len(lines_found) < lines:
            try:
                f.seek(block_counter * _buffer, io.SEEK_END)
            except OSError:  # reached start of file
                f.seek(0)
                chunk = f.read().decode(errors="ignore")
                lines_found = chunk.splitlines()
                break

            chunk = f.read().decode(errors="ignore")
            lines_found = chunk.splitlines()
            block_counter -= 1

    return lines_found[-lines:]