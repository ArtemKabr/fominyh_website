from fastapi import FastAPI

app = FastAPI(title="FOMINYH_WEBSITE")

@app.get("/health")
def health():
    return {"status": "ok"}
