from aiohttp import ClientSession
from fastapi import FastAPI

from crawler_api.crawlers import COURTS
from crawler_api.models.requests import LegalProcess
from crawler_api.models.response import LegalProcessDetailResponse

app = FastAPI(
    title='Legal Process Crawler',
    description=(
        'It is a simple API to get legal process detail on TJAL or TJMS website '
        'and convert the search result HTML to JSON'
    )
)


@app.post("/legal-process", response_model=LegalProcessDetailResponse, description='Get Legal Process detail')
async def show_legal_process_detail(legal_process: LegalProcess) -> LegalProcessDetailResponse:
    async with ClientSession() as session:
        crawler = COURTS[legal_process.court](session)
        result = await crawler.execute(number=legal_process.number)
    return LegalProcessDetailResponse(degrees=tuple(result))
