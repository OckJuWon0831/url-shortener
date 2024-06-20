from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas, keygen
import hashlib
from .utils.errors import raise_bad_request, raise_not_found


def create_db_url(db: Session, url: schemas.URL) -> schemas.URLShort:

    key = keygen.create_unique_random_key(db)
    secret_key = f"{key}_{keygen.create_random_key(length=7)}"
    db_url = models.URL(
        original_url=str(url.original_url), short_url=secret_key, stats=0
    )
    db.add(db_url)
    try:
        db.commit()
        db.refresh(db_url)
        return db_url
    except IntegrityError:
        db.rollback()
        raise_bad_request("Could not create short URL")


def get_db_url(db: Session, short_url: str) -> models.URL:
    db_url = db.query(models.URL).filter(models.URL.short_url == short_url).first()
    if db_url:
        db_url.stats += 1
        db.commit()
        db.refresh(db_url)
        return db_url
    else:
        raise_not_found(f"URL '{short_url}' not found")


def get_db_url_by_key(db: Session, url_key: str) -> models.URL:
    return db.query(models.URL).filter(models.URL.short_url == url_key).first()


def get_stats(db: Session, short_url: str) -> schemas.URLStats:
    db_url = db.query(models.URL).filter(models.URL.short_url == short_url).first()
    if db_url is None:
        raise_not_found(f"URL '{short_url}' not found")
    else:
        db_url_with_stats = schemas.URLStats(
            original_url=db_url.original_url,
            short_url=db_url.short_url,
            stats=db_url.stats,
        )
        return db_url_with_stats
