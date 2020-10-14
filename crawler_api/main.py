from aiohttp import ClientSession
from fastapi import FastAPI, HTTPException

from crawler_api.crawlers import COURTS
from crawler_api.models.requests import LegalProcess
from crawler_api.models.response import LegalProcessDetailResponse, Message

app = FastAPI(
    title='Legal Process Crawler',
    description=(
        'It is a simple API to get legal process detail on TJAL or TJMS website '
        'and convert the search result HTML to JSON'
    )
)


@app.post(
    "/legal-process",
    response_model=LegalProcessDetailResponse,
    description='Get Legal Process detail',
    responses={404: {"model": Message}}
)
async def show_legal_process_detail(legal_process: LegalProcess) -> LegalProcessDetailResponse:
    async with ClientSession() as session:
        try:
            crawler = COURTS[legal_process.court](session)
        except KeyError:
            raise HTTPException(status_code=422, detail="Crawler not implemented")
        result = tuple(await crawler.execute(number=legal_process.number))
    if not result:
        raise HTTPException(status_code=404, detail="Legal Process not found")
    return LegalProcessDetailResponse(degrees=tuple(result))
