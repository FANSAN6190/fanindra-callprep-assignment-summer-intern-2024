from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, File, UploadFile
from src.service.create_embeddings import create_embeddings

uploadRouter = APIRouter()
create_embeddings = create_embeddings()

@uploadRouter.get("/upload", response_class=HTMLResponse)
def display_upload():
    #upload pdf file only
    return  """
            <html>
                <body>
                    <form action="/upload" method="post" enctype="multipart/form-data">
                        <input type="file" name="file" accept=".pdf">
                        <input type="submit">
                    </form>
                    <a href="/">Back to Home</a>
                </body>
            </html>
            """

@uploadRouter.post("/upload", response_class=HTMLResponse)
async def upload_file(file: UploadFile = File(...)):
    # save file to a folder
    file_path = f"UploadedDocuments/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    try:
        create_embeddings.create_and_save_embeddings(file_path, file.filename)
    except Exception as e:
        print(f"Error creating embeddings for {file.filename}: {e}")
        return f"Error creating embeddings for {file.filename}: {e}"

    return """
            <html>
                <body>
                    <h1>File Uploaded Successfully</h1>
                    <a href="/">Back to Home</a>
                </body>
            </html>    
        """