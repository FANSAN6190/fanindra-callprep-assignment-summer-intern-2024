from fastapi import FastAPI, File, UploadFile
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return  """
            <html>
                <body>
                    <h1>Hello, World</h1>
                </body>
            </html>
            """

@app.get("/upload", response_class=HTMLResponse)
def read_root():
    #upload pdf file only
    return  """
            <html>
                <body>
                    <form action="/upload" method="post" enctype="multipart/form-data">
                        <input type="file" name="file" accept=".pdf">
                        <input type="submit">
                    </form>
                </body>
            </html>
            """


@app.post("/upload", response_class=HTMLResponse)
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