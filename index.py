import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
PY_SCHOOL_DIR = PROJECT_ROOT / "py_school"

if str(PY_SCHOOL_DIR) not in sys.path:
    sys.path.insert(0, str(PY_SCHOOL_DIR))

from main import app
