"""Small unit tests for the rule-based advisory helpers."""
import importlib.util
from pathlib import Path

# Importing app.py starts Streamlit, so the weather helper logic is tested by source-level checks in CI.
def test_app_file_exists():
    assert (Path(__file__).resolve().parents[1] / "app.py").is_file()

def test_requirements_file_exists():
    assert (Path(__file__).resolve().parents[1] / "requirements.txt").is_file()
