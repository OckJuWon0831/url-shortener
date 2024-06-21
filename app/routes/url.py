from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.datastructures import URL

from app import crud, models, schemas
from app.database import get_db
from app.utils.errors import raise_bad_request, raise_not_found
import redis

router = APIRouter(tags=["URL Shortener API 명세서"])
r = redis.Redis(host="cache", port=6379, db=0)


@router.post("/shorten", response_model=schemas.URLShort)
def create_url(url: schemas.URL, db: Session = Depends(get_db)):
    db_url = crud.create_db_url(db=db, url=url)
    return db_url


@router.get("/stats/{short_url}", response_model=schemas.URLStats)
def show_url_stats(short_url: str, request: Request, db: Session = Depends(get_db)):
    if db_url_stats := crud.get_stats(db, short_url):
        return db_url_stats
    else:
        raise_not_found(request)


@router.get("/{short_url}", status_code=301)
def redirect_url(short_url: str, request: Request, db: Session = Depends(get_db)):
    # Check Redis cache first
    cached_url = r.get(short_url)
    if cached_url:
        db_url = crud.get_db_url(db, short_url, request)
        return RedirectResponse(cached_url.decode("utf-8"))

    db_url = crud.get_db_url(db, short_url, request)
    if db_url is None:
        raise_not_found(request)

    r.set(short_url, db_url.original_url)
    return RedirectResponse(db_url.original_url)
