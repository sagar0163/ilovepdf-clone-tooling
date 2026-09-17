"""FastAPI Wrapper - REST API for PDF Tools"""
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from pathlib import Path

import file_ops

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


def _flush_uploads(files, dest_dir):
    """Persist uploads to ``dest_dir`` under sanitized per-request names."""
    paths = []
    try:
        for f in files:
            paths.append(str(file_ops.save_upload(f.filename, f.file, dest_dir)))
    finally:
        for f in files:
            try:
                f.file.close()
            except OSError:
                pass
    return paths


def _handle(background_tasks, upload_dir, output_dir, on_success):
    """Run ``on_success`` with request-scoped dirs; clean up in all outcomes.

    On success the cleanup is deferred to ``background_tasks`` so it runs after
    the response is sent; on failure the temp dirs are removed immediately.
    """
    try:
        result = on_success()
    except ValueError as e:
        file_ops.cleanup_path(upload_dir)
        file_ops.cleanup_path(output_dir)
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        file_ops.cleanup_path(upload_dir)
        file_ops.cleanup_path(output_dir)
        raise
    except Exception:
        file_ops.cleanup_path(upload_dir)
        file_ops.cleanup_path(output_dir)
        raise
    background_tasks.add_task(file_ops.cleanup_path, upload_dir)
    background_tasks.add_task(file_ops.cleanup_path, output_dir)
    return result


@app.post("/merge")
async def merge_pdfs(files: list[UploadFile] = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    """Merge multiple PDFs into one."""
    from merge import merge_pdfs as do_merge

    upload_dir = file_ops.new_request_dir(UPLOAD_DIR)
    output_path = file_ops.unique_output_path(OUTPUT_DIR, "merged.pdf")

    def run():
        input_paths = _flush_uploads(files, upload_dir)
        ok = do_merge(input_paths, str(output_path))
        if not ok:
            raise HTTPException(status_code=500, detail="Merge failed")
        return FileResponse(str(output_path), filename="merged.pdf")

    return _handle(background_tasks, upload_dir, output_path.parent, run)


@app.post("/split")
async def split_pdf(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    """Split PDF into pages."""
    from split import split_pdf as do_split

    upload_dir = file_ops.new_request_dir(UPLOAD_DIR)
    output_dir = file_ops.new_request_dir(OUTPUT_DIR)

    def run():
        input_path = str(file_ops.save_upload(file.filename, file.file, upload_dir))
        result = do_split(input_path, str(output_dir))
        if not result:
            raise HTTPException(status_code=500, detail="Split failed")
        return {"message": "PDF split successfully", "output_dir": str(output_dir), "pages": len(result)}

    return _handle(background_tasks, upload_dir, output_dir, run)


@app.post("/compress")
async def compress_pdf(
    file: UploadFile = File(...),
    quality: str = Form("medium"),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Compress PDF."""
    from compress import compress_pdf as do_compress

    upload_dir = file_ops.new_request_dir(UPLOAD_DIR)
    output_path = file_ops.unique_output_path(OUTPUT_DIR, "compressed.pdf")

    def run():
        input_path = str(file_ops.save_upload(file.filename, file.file, upload_dir))
        ok = do_compress(input_path, str(output_path), quality=quality)
        if not ok:
            raise HTTPException(status_code=500, detail="Compression failed")
        return FileResponse(str(output_path), filename="compressed.pdf")

    return _handle(background_tasks, upload_dir, output_path.parent, run)


@app.post("/watermark")
async def add_watermark(
    file: UploadFile = File(...),
    text: str = Form(None),
    opacity: float = Form(0.3),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Add watermark to PDF."""
    from watermark import add_watermark as do_watermark

    upload_dir = file_ops.new_request_dir(UPLOAD_DIR)
    output_path = file_ops.unique_output_path(OUTPUT_DIR, "watermarked.pdf")

    def run():
        input_path = str(file_ops.save_upload(file.filename, file.file, upload_dir))
        ok = do_watermark(input_path, str(output_path), text=text, opacity=opacity)
        if not ok:
            raise HTTPException(status_code=500, detail="Watermark failed")
        return FileResponse(str(output_path), filename="watermarked.pdf")

    return _handle(background_tasks, upload_dir, output_path.parent, run)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)