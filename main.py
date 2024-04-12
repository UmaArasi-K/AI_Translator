from fastapi import FastAPI, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from model.pdf import main as translate_pdf
import os

app = FastAPI()
@app.get("/")
async def read_root():
    return FileResponse("template/html/index.html")
# Serve static files from template and static directories
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/template", StaticFiles(directory="template"), name="template")
app.mount("/model/font", StaticFiles(directory="model"), name="model")

# Function to get the path to the user's "Downloads" directory
def get_downloads_dir():
    return os.path.expanduser("~/Downloads")

@app.post("/uploadpdf/")
async def upload_pdf_and_translate(
    file: UploadFile = File(...),
    source_language: str = Form(...),
    target_language: str = Form(...),
    output_dir: str = Form(...),
):
    # Save the uploaded file to disk
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # # Output PDF path in the "Downloads" directory
    # output_path = os.path.join(output_dir, file.filename)

    # Translate PDF
    translate_pdf(file_path, source_language, target_language)
    return FileResponse('C:/Users/umaar/1.pdf')
     
@app.get("/output1/{file_name}")
async def download_output(file_name: str):
    # Serve the output file for download
    return FileResponse(file_name)
