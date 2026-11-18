import pytest

from tools import file_writer
from tools.calculator import calculate
from tools.file_writer import write_file


@pytest.mark.parametrize("expr,expected", [
    ("12*13", 156),
    ("(1234 * 56) / 7 + 89", 9961.0),
    ("2 ** 10", 1024),
    ("-5 + 3", -2),
])
def test_calculate(expr, expected):
    assert calculate(expr) == expected


@pytest.mark.parametrize("expr", [
    "__import__('os').system('ls')",
    "2 ** 1000",
    "1 / 0",
    "abc",
    "1" * 201,
])
def test_calculate_rejects_bad_input(expr):
    with pytest.raises(ValueError):
        calculate(expr)


@pytest.fixture
def out(tmp_path, monkeypatch):
    monkeypatch.setattr(file_writer, "OUTPUT_DIR", tmp_path)
    monkeypatch.setattr(file_writer, "PROJECT_ROOT", tmp_path.parent)
    return tmp_path


def test_write_and_overwrite(out):
    assert write_file("a.md", "one")["overwritten"] is False
    assert write_file("output/a.md", "two")["overwritten"] is True
    assert (out / "a.md").read_text() == "two"


@pytest.mark.parametrize("name", ["../evil.md", "sub/a.md", "a.exe", ""])
def test_write_rejects_bad_names(out, name):
    assert write_file(name, "x")["success"] is False
