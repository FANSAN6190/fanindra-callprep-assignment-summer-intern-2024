from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from src.routes.upload import uploadRouter
from src.routes.docs import docsRouter

app = FastAPI()
app = FastAPI(docs_url="/api-docs")

@app.get("/", response_class=HTMLResponse)
def diplay_home():
    return  """
            <html>
                <body>
                    <h1>Hello, World</h1>
                    <a href="/upload">Upload a PDF</a>
                    <a href="/search-doc">Search Docs</a>
                </body>
            </html>
            """

app.include_router(uploadRouter)
app.include_router(docsRouter)


