"""Cross-cutting rule: only repository.py files may import app.sample_data."""

import ast
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent / "app"
SAMPLE_DATA_FILE = "sample_data.py"
REPOSITORY_FILE = "repository.py"


def imports_sample_data(source: str) -> bool:
    """Return True if the source imports the sample_data module in any form."""
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            if any(a.name.split(".")[-1] == "sample_data" for a in node.names):
                return True
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[-1] == "sample_data":
                return True
            if any(a.name == "sample_data" for a in node.names):
                return True
    return False


def test_scanner_detects_every_import_form():
    assert imports_sample_data("import app.sample_data")
    assert imports_sample_data("from app import sample_data")
    assert imports_sample_data("from app.sample_data import COMPLAINTS")
    assert imports_sample_data("from .. import sample_data")
    assert not imports_sample_data("from app import config")


def test_only_repository_files_import_sample_data():
    importers = {
        path
        for path in APP_DIR.rglob("*.py")
        if path.name != SAMPLE_DATA_FILE
        and imports_sample_data(path.read_text(encoding="utf-8"))
    }
    assert importers, "scan found no importers; the scanner may be broken"
    offenders = sorted(
        str(p.relative_to(APP_DIR)) for p in importers if p.name != REPOSITORY_FILE
    )
    assert offenders == []
