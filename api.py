# api.py
from fastapi import FastAPI, UploadFile, Form
from renaim import process_file
from typing import List

app = FastAPI()

@app.post("/rename")
async def rename_files(
    files: List[UploadFile], 
    output_dir: str = Form(""),
    include_resolution: bool = Form(False),
    create_link: bool = Form(False),
    timestamp_position: str = Form(""),
    use_ai: bool = Form(False),
    use_hash: bool = Form(False),
    prepend_text: str = Form(""),
    append_text: str = Form(""),
    api_key: str = Form("")
):
    """
    Expose the rename function via a POST endpoint.
    """
    # Handle the file uploads
    for file in files:
        with open(file.filename, "wb") as f:
            f.write(await file.read())
        
        # Assuming the original process_file can work as-is
        process_file(
            file.filename,
            output_dir,
            include_resolution,
            create_link,
            timestamp_position,
            use_ai,
            use_hash,
            prepend_text,
            append_text,
            api_key
        )
    
    return {"status": "success", "processed_files": [file.filename for file in files]}
