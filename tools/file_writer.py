from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"

ALLOWED_EXTENSIONS = {".txt", ".md", ".json", ".csv"}
MAX_CONTENT_CHARS = 500_000


def write_file(filename: str, content: str):
    """Write a text file into output/. Returns a result dict; never raises."""
    try:
        if not isinstance(content, str):
            raise ValueError("Content must be text.")
        if len(content) > MAX_CONTENT_CHARS:
            raise ValueError("Content is too large.")

        # Models often pass "output/report.md"; only the bare name is allowed.
        name = filename.strip().removeprefix("output/")
        if not name or Path(name).name != name or name in (".", ".."):
            raise ValueError("Invalid filename.")
        if Path(name).suffix.lower() not in ALLOWED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file extension. Allowed: {sorted(ALLOWED_EXTENSIONS)}"
            )

        OUTPUT_DIR.mkdir(exist_ok=True)
        path = OUTPUT_DIR / name
        overwritten = path.exists()

        # Write to a temp file first so a failed write can't corrupt the original.
        tmp = path.with_name(path.name + ".tmp")
        tmp.write_text(content, encoding="utf-8")
        tmp.replace(path)

        return {
            "success": True,
            "filename": name,
            "location": str(path.relative_to(PROJECT_ROOT)),
            "overwritten": overwritten,
        }
    except Exception as error:
        return {"success": False, "error": str(error)}
