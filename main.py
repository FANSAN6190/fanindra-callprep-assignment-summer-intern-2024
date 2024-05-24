from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from src.routes.upload import uploadRouter
from src.routes.docs import docsRouter
import os

app = FastAPI()
app = FastAPI(docs_url="/api-docs")

@app.get("/", response_class=HTMLResponse)
def diplay_home():
    return  """
            <html>
                <head>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 0;
                            display: flex;
                            flex-direction: column; /* Add this line */
                            justify-content: flex-start; /* Change this line */
                            align-items: center; 
                            height: 100vh;
                            background-color: #f0f0f0;
                        }
                        h1 {
                            color: #333;
                            margin-top: 20px;
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
                        <h1>Document Search</h1>
                        <a href="/upload">Upload Documents</a>
                        <a href="/search-doc">Search Docs</a>
                    </div>
                </body>
            </html>
            """

app.include_router(uploadRouter)
app.include_router(docsRouter)


if __name__ == "__main__":
    if not os.path.exists("UploadedDocuments"):
        os.makedirs("UploadedDocuments")
    import uvicorn
    uvicorn.run(app, host="localhost", port=8040)   