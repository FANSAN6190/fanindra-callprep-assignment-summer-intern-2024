from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, File, UploadFile
from src.service.create_embeddings import create_embeddings
from typing import List

uploadRouter = APIRouter()
create_embeddings = create_embeddings()

@uploadRouter.get("/upload", response_class=HTMLResponse)
def display_upload():
    #upload pdf file only
    return  """
            <html>
                <body>
                    <form action="/upload" method="post" enctype="multipart/form-data">
                        <input type="file" name="file" accept=".pdf,.txt" multiple>
                        <input type="submit">
                    </form>
                    <a href="/">Back to Home</a>
                </body>
            </html>
            """

@uploadRouter.post("/upload", response_class=HTMLResponse)
async def upload_file(file: List[UploadFile] = File(...)):
    for f in file:
        # save file to a folder
        file_path = f"UploadedDocuments/{f.filename}"
        with open(file_path, "wb") as file_object:
            file_object.write(f.file.read())
        try:
            create_embeddings.create_and_save_embeddings(file_path, f.filename)
        except Exception as e:
            print(f"Error creating embeddings for {f.filename}: {e}")
            return f"Error creating embeddings for {f.filename}: {e}"

    return """
            <html>
                <body>
                    <h1>File Uploaded Successfully</h1>
                    <a href="/">Back to Home</a>
                </body>
            </html>    
        """