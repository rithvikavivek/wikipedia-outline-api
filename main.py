from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/api/outline")
async def get_country_outline(country: str = Query(..., description="Country name")):
    """Fetch Wikipedia headings and generate Markdown outline"""
    
    # Format Wikipedia URL
    wiki_url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
    
    # Fetch Wikipedia page
    response = requests.get(wiki_url)
    if response.status_code != 200:
        return {"error": "Wikipedia page not found"}

    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

    # Generate Markdown Outline
    markdown_outline = "## Contents\n\n"
    markdown_outline += f"# {country}\n\n"
    
    for heading in headings:
        level = int(heading.name[1])  # Extract the heading level
        markdown_outline += f"{'#' * level} {heading.text.strip()}\n\n"

    return {"markdown": markdown_outline}

# Run the server with: uvicorn main:app --reload
