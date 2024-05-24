from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, File, UploadFile
from src.service.create_embeddings import create_embeddings
from typing import List
from src.service.create_embeddings import create_embeddings

uploadRouter = APIRouter()

@uploadRouter.get("/upload", response_class=HTMLResponse)
def display_upload():
    #upload pdf file only
    return  """
            <html>
                <head>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            background-color: #f0f0f0;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 20vh;
                        }
                        form {
                            margin-top: 20px;
                        }
                        input[type="file"] {
                            margin: 10px 0;
                        }
                        input[type="submit"] {
                            padding: 10px 20px;
                            background-color: #007BFF;
                            color: #fff;
                            border: none;
                            cursor: pointer;
                        }
                    </style>
                </head>
                <body>
                    <form action="/upload" method="post" enctype="multipart/form-data">
                        <input type="file" name="file" accept=".pdf,.txt,.html" multiple required>
                        <input type="submit" value="Upload">
                    </form>
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
                <head>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 0;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                            background-color: #f0f0f0;
                        }
                        h1 {
                            color: #333;
                        }
                        a {
                            display: inline-block;
                            margin: 10px;
                            padding: 10px 20px;
                            color: #fff;
                            background-color: #007BFF;
                            text-decoration: none;
                            border-radius: 5px;
                        }
                        a:hover {
                            background-color: #0056b3;
                        }
                    </style>
                </head>
                <body>
                    <div>
                        <h1>File Uploaded Successfully</h1>
                        <a href="/">Back to Home</a>
                    </div>
                </body>
            </html>    
        """