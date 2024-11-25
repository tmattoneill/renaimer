from fastapi import FastAPI
from renaimer import renaimer_function  # assuming renaimer_function is your main CLI logic

app = FastAPI()

@app.post("/rename")
async def rename_files(data: dict):
    # Call your renaimer CLI logic here with the provided input
    results = renaimer_function(data)
    return {"status": "success", "results": results}
