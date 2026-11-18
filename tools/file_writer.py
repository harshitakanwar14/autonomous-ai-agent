
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"

ALLOWED_EXTENSIONS = {
    ".txt", ".md", ".json", ".csv"
}


def write_file(filename: str, content: str):

    if not filename or not filename.strip():
        raise ValueError("Filename cannot be empty.")

    if len(content) > 500_000:
        raise ValueError("Content is too large.")

    # Only allow saving inside output/
    OUTPUT_DIR.mkdir(exist_ok=True)

    file_path = (OUTPUT_DIR / filename).resolve()

    if not file_path.is_relative_to(OUTPUT_DIR.resolve()):
        raise ValueError("Writing outside output is forbidden.")

    if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file extension.")

    
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"


def write_file(filename: str, content: str):

    try:

        OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        # Only allow filenames, not arbitrary paths
        safe_name = Path(filename).name

        if safe_name != filename or safe_name in ("", ".", ".."):
            raise ValueError("Invalid filename.")

        file_path = (OUTPUT_DIR / safe_name).resolve()

        if file_path.parent != OUTPUT_DIR.resolve():
            raise ValueError("Invalid output path.")

        if not isinstance(content, str):
            raise ValueError("Content must be text.")

        # Write to a temporary file first
        temp_path = file_path.with_name(
            file_path.name + ".tmp"
        )

        temp_path.write_text(
            content,
            encoding="utf-8"
        )

        # Replace existing file atomically
        temp_path.replace(file_path)

        return {
            "success": True,
            "filename": safe_name,
            "location": str(file_path.relative_to(PROJECT_ROOT)),
            "overwritten": file_path.exists()
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }


    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_path.write_text(
        content,
        encoding="utf-8"
    )

    return {
        "success": True,
        "filename": file_path.name,
        "location": str(file_path.relative_to(PROJECT_ROOT))
    }
