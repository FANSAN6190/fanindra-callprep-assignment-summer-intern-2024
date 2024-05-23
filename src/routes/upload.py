from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, File, UploadFile

uploadRouter = APIRouter()

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
    with open(f"UploadedDocuments/{file.filename}", "wb") as f:
        f.write(file.file.read())
    #return f"File '{file.filename}' uploaded successfully"
    return """
            <html>
                <body>
                    <h1>File Uploaded Successfully</h1>
                    <a href="/">Back to Home</a>
                </body>
            </html>    
        """