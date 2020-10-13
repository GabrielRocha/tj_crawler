from fastapi import FastAPI

from crawler_api.models.requests import LegalProcess

app = FastAPI(
    title='Legal Process Crawler',
    description=(
        'It is a simple API to get legal process detail on TJAL or TJMS website '
        'and convert the search result HTML to JSON'
    )
)


@app.post("/legal-process")
async def show_legal_process_detail(legal_process: LegalProcess):
    return {"message": "Hello World"}
