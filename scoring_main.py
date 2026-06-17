import uvicorn

if __name__ == "__main__":
    uvicorn.run("scoring_platform.web:app", host="127.0.0.1", port=8003, reload=True)
