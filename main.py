"""FastAPI Wrapper - REST API for PDF Tools"""
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from pathlib import Path

app = FastAPI(title="iLovePDF API", description="REST API for PDF manipulation tools")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create temp directories
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("output")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


@app.get("/")
async def root():
    return {"message": "iLovePDF API - PDF Tools REST API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/merge")
async def merge_pdfs(files: list[UploadFile] = File(...)):
    """Merge multiple PDFs into one."""
    from merge import merge_pdfs
    
    input_paths = []
    for f in files:
        path = UPLOAD_DIR / f.filename
        with open(path, "wb") as buffer:
            shutil.copyfileobj(f.file, buffer)
        input_paths.append(str(path))
    
    output_path = OUTPUT_DIR / "merged.pdf"
    result = merge_pdfs(input_paths, str(output_path))
    
    if result:
        return FileResponse(str(output_path), filename="merged.pdf")
    raise HTTPException(status_code=500, detail="Merge failed")


@app.post("/split")
async def split_pdf(file: UploadFile = File(...)):
    """Split PDF into pages."""
    from split import split_pdf
    
    input_path = UPLOAD_DIR / file.filename
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(f.file, buffer)
    
    output_dir = OUTPUT_DIR / "split_pages"
    output_dir.mkdir(exist_ok=True)
    
    result = split_pdf(str(input_path), str(output_dir))
    
    if result:
        return {"message": "PDF split successfully", "output_dir": str(output_dir)}
    raise HTTPException(status_code=500, detail="Split failed")


@app.post("/compress")
async def compress_pdf(
    file: UploadFile = File(...),
    quality: str = Form("medium")
):
    """Compress PDF."""
    from compress import compress_pdf
    
    input_path = UPLOAD_DIR / file.filename
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(f.file, buffer)
    
    output_path = OUTPUT_DIR / "compressed.pdf"
    result = compress_pdf(str(input_path), str(output_path), quality=quality)
    
    if result:
        return FileResponse(str(output_path), filename="compressed.pdf")
    raise HTTPException(status_code=500, detail="Compression failed")


@app.post("/watermark")
async def add_watermark(
    file: UploadFile = File(...),
    text: str = Form(None),
    opacity: float = Form(0.3)
):
    """Add watermark to PDF."""
    from watermark import add_watermark
    
    input_path = UPLOAD_DIR / file.filename
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(f.file, buffer)
    
    output_path = OUTPUT_DIR / "watermarked.pdf"
    result = add_watermark(str(input_path), str(output_path), text=text, opacity=opacity)
    
    if result:
        return FileResponse(str(output_path), filename="watermarked.pdf")
    raise HTTPException(status_code=500, detail="Watermark failed")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

