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
                <body>
                    <h1>Hello, World</h1>
                    <a href="/upload">Upload Documents</a>
                    <a href="/search-doc">Search Docs</a>
                </body>
            </html>
            """

app.include_router(uploadRouter)
app.include_router(docsRouter)


if __name__ == "__main__":
    if not os.path.exists("UploadedDocuments"):
        os.makedirs("UploadedDocuments")
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)   