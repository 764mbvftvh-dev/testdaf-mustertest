"""Student system configuration."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
QUESTION_BANK_DIR = PROJECT_ROOT / "question_bank"
STUDENT_ATTEMPTS_DIR = PROJECT_ROOT / "student_attempts"
