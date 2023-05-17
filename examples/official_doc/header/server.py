from typing import Annotated, Any

from fastapi import FastAPI, Header, Response
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get('/')
async def root(q: bool = False):
    if q:
        return RedirectResponse(url='/docs')
    return {'message': 'Running..'}


@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}
