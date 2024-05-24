import os
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi import Response
from starlette.responses import FileResponse

from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
import urllib.parse
from src.service.create_embeddings import create_embeddings

docsRouter = APIRouter()

embedding_creator = create_embeddings()

@docsRouter.get("/documents/{filename}", response_class=Response)
async def read_document(filename: str):
    decoded_filename = urllib.parse.unquote(filename)
    file_path = os.path.join("UploadedDocuments", decoded_filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, headers={"Content-Disposition": "attachment;"})
    else:
        raise HTTPException(status_code=404, detail="File not found")
    
@docsRouter.get("/search-doc", response_class=HTMLResponse)
def display_search():
    return  """
            <html>
                <body>
                    <form id="searchForm" action="/docs" method="get">
                        <input type="text" id="searchInput" name="q" value="Search Docs">
                        <input type="submit">
                    </form>
                    <a href="/">Back to Home</a>
                    <hr>
                    <div id="searchResult"></div>
                    <script>
                        document.getElementById('searchForm').addEventListener('submit', function(event) {
                            event.preventDefault();
                            var searchQuery = document.getElementById('searchInput').value;
                            fetch('/docs?q=' + searchQuery)
                                .then(response => response.text())
                                .then(data => {
                                    document.getElementById('searchResult').innerHTML = data;
                                });
                        });
                    </script>
                </body>
            </html>
            """

@docsRouter.get("/docs", response_class=HTMLResponse)
def read_docs(q: str = None):
    if q:
        results = embedding_creator.search_documents(q)
        print("query results: ", results)
        result_html = "<html><body><h1>Search Results</h1><ul>"
        for match in results['matches']:
            filename = match['id']
            encoded_filename = urllib.parse.quote(filename)
            result_html += f"<li><a href='/documents/{encoded_filename}'>{filename}</a></li>"
        result_html += "</ul><a href='/'>Back to Home</a></body></html>"
        return HTMLResponse(content=result_html)
    else:
        return HTMLResponse(content="<html><body><h1>No query provided</h1><a href='/'>Back to Home</a></body></html>")


