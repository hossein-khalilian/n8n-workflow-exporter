import os
import shutil
import uuid
from typing import List

import fitz  # PyMuPDF
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/extract-urls")
async def extract_urls(file: UploadFile = File(...)) -> dict[str, List[str]]:
    # Save uploaded file to a temporary location
    temp_filename = f"/tmp/{uuid.uuid4()}_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract URLs using PyMuPDF
    urls = []
    try:
        doc = fitz.open(temp_filename)
        for page in doc:
            links = page.get_links()
            for link in links:
                uri = link.get("uri")
                if uri:
                    urls.append(uri)
        doc.close()
    finally:
        os.remove(temp_filename)

    return {"urls": urls}
