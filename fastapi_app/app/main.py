from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"hello" : "fmb"}

@app.get("/testend/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}