from fastapi import APIRouter

app = APIRouter()


@app.get("/")
def root():
    return {
        "message": "Welcome to AI Resume Intelligence API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "version": "1.0.0"
    }