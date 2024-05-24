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
    return """
            <html>
                <head>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 0;
                            display: flex;
                            flex-direction: column;
                            align-items: center;
                            justify-content: flex-start; /* Change this line */
                            height: 100vh;
                            background-color: #f0f0f0;
                        }
                        #searchForm {
                            display: flex;
                            flex-direction: column;
                            align-items: center;
                            margin-top: 20px; /* Add this line */
                        }
                        #searchInput {
                            margin: 10px 0;
                            padding: 10px;
                            width: 300px;
                            border: 1px solid #ccc;
                            border-radius: 5px;
                        }
                        input[type="submit"] {
                            padding: 10px 20px;
                            background-color: #007BFF;
                            color: #fff;
                            border: none;
                            border-radius: 5px;
                            cursor: pointer;
                        }
                        input[type="submit"]:hover {
                            background-color: #0056b3;
                        }
                        a {
                            display: inline-block;
                            margin-top: 20px;
                            color: #007BFF;
                            text-decoration: none;
                        }
                        a:hover {
                            text-decoration: underline;
                        }
                        #searchResult {
                            margin-top: 20px;
                            width: 80%;
                            text-align: center;
                        }
                    </style>
                </head>
                <body>
                    <form id="searchForm" action="/docs" method="get">
                        <input type="text" id="searchInput" name="q" value="Search Docs">
                        <input type="submit" value="Search">
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
    style = """
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                background-color: #f0f0f0;
            }
            h1 {
                color: #333;
            }
            ul {
                list-style-type: none;
                padding: 0;
                text-align: left; /* Add this line */
                width: 80%; /* Add this line */
                margin: 0 auto; /* Add this line */
            }
            li {
                margin: 10px 0;
            }
            a {
                color: #007BFF;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    """
    if q:
        results = create_embeddings.search_documents(q)
        print("query results: ", results)
        result_html = f"<html><head>{style}</head><body><h1>Search Results</h1><ul>"
        for match in results['matches']:
            filename = match['id']
            encoded_filename = urllib.parse.quote(filename)
            result_html += f"<li><a href='/documents/{encoded_filename}'>{filename}</a></li>"
        result_html += "</ul></body></html>"
        return HTMLResponse(content=result_html)
    else:
        return HTMLResponse(content=f"<html><head>{style}</head><body><h1>No query provided</h1></body></html>")

