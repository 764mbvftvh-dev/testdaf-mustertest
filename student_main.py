"""Command-line entry for the student practice system."""

import uvicorn


if __name__ == "__main__":
    uvicorn.run("student_platform.web:app", host="127.0.0.1", port=8001, reload=True)
