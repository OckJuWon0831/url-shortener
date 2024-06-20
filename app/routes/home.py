from typing import Union

from fastapi import APIRouter, Header, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", include_in_schema=False)
def root_path(request: Request, accept: Union[str, None] = Header(default="text/html")):
    if accept.split(",")[0] == "text/html":
        return templates.TemplateResponse("index.html", {"request": request})
