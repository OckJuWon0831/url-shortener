import validators
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.datastructures import URL

from app import crud, models, schemas
from app.database import get_db
from app.utils.errors import raise_bad_request, raise_not_found

router = APIRouter(tags=["URL Functionality"])


@router.post("/shorten", response_model=schemas.URL)
def create_url(url: schemas.URL, db: Session = Depends(get_db)):
    """Create a URL shortener entry."""
    if not validators.url(url.original_url):
        raise_bad_request(message="URL is not Valid")
    crud.create_db_url(db=db, url=url)


@router.get("/stats/{short_url}", response_model=schemas.URLStats)
def show_url_stats(short_url: str, request: Request, db: Session = Depends(get_db)):
    """
    Return only the target URL, do not redirect.

    This allows users to check the URL before visiting.
    """
    if db_url := crud.get_db_stats(db=db, short_url=short_url):
        return db_url.stats
    else:
        raise_not_found(request)


@router.get("/{short_url}")
def forward_to_original_url(
    short_url: str, request: Request, db: Session = Depends(get_db)
):
    """Forward to the correct full URL."""
    if db_url := crud.get_db_url(db=db, short_url=short_url):
        # crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.original_url)
    else:
        raise_not_found(request)
