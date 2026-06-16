"""FastAPI entry for the student practice system."""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from shared.question_bank import QuestionBankReader
from student_platform.config import QUESTION_BANK_DIR, STUDENT_ATTEMPTS_DIR

PACKAGE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="TestDaF 学生答题系统", version="0.1.0")
app.mount("/static", StaticFiles(directory=PACKAGE_DIR / "static"), name="static")
app.mount("/question-bank", StaticFiles(directory=QUESTION_BANK_DIR), name="question_bank")

templates = Jinja2Templates(directory=PACKAGE_DIR / "templates")
question_reader = QuestionBankReader(QUESTION_BANK_DIR)


@app.on_event("startup")
def startup() -> None:
    STUDENT_ATTEMPTS_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    questions = question_reader.list_questions()
    return templates.TemplateResponse(
        request=request,
        name="student_index.html",
        context={
            "request": request,
            "questions": questions,
            "question_count": len(questions),
        },
    )


@app.get("/practice/{section}/{task_type}/{question_id}", response_class=HTMLResponse)
def practice_question(request: Request, section: str, task_type: str, question_id: str) -> HTMLResponse:
    question = question_reader.find_by_id(question_id)
    if not question:
        return templates.TemplateResponse(
            request=request,
            name="practice_not_found.html",
            context={"request": request, "question_id": question_id},
            status_code=404,
        )
    bundle = question_reader.load_question_bundle(question["_path"])
    return templates.TemplateResponse(
        request=request,
        name="practice_question.html",
        context={
            "request": request,
            "question": question,
            "bundle": bundle,
            "section": section,
            "task_type": task_type,
        },
    )


@app.get("/attempts", response_class=HTMLResponse)
def attempts(request: Request) -> HTMLResponse:
    attempt_dirs = sorted(STUDENT_ATTEMPTS_DIR.glob("attempt_*"), reverse=True)
    return templates.TemplateResponse(
        request=request,
        name="attempts.html",
        context={
            "request": request,
            "attempt_count": len(attempt_dirs),
            "attempts": [path.name for path in attempt_dirs],
        },
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "system": "student"}
