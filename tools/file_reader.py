
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

ALLOWED_EXTENSIONS = {
    ".txt", ".md", ".csv", ".json", ".log"
}


def read_file(path: str):

    file_path = (PROJECT_ROOT / path).resolve()

    # Prevent reading files outside the project
    if not file_path.is_relative_to(PROJECT_ROOT):
        raise ValueError("Access outside project is not allowed.")

    if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file type.")

    if file_path.name.lower() == ".env":
        raise ValueError("Access to environment files is forbidden.")

    if not file_path.is_file():
        raise FileNotFoundError("File does not exist.")

    if file_path.stat().st_size > 2_000_000:
        raise ValueError("File is too large.")

    content = file_path.read_text(
        encoding="utf-8",
        errors="replace"
    )

    return {
        "file": str(file_path.relative_to(PROJECT_ROOT)),
        "content": content[:20000],
        "truncated": len(content) > 20000
    }
