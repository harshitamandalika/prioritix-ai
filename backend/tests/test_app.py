import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from backend.app import app


def test_app_exists():
    assert app is not None