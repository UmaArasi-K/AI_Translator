from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse


app = FastAPI()

@app.get("/")
async def read_root():
    return FileResponse("template/html/index.html")

app.mount("/static", StaticFiles(directory="static"), name="static")
