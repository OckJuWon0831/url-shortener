from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas, keygen
from datetime import datetime, timedelta
from .utils.errors import raise_bad_request, raise_not_found
from pytz import timezone


def create_db_url(db: Session, url: schemas.URL) -> schemas.URLShort:

    key = keygen.create_unique_random_key(db)
    secret_key = f"{key}_{keygen.create_random_key(length=7)}"
    created_at = datetime.now(timezone("Asia/Seoul"))
    expires_at = created_at + timedelta(seconds=url.expires_in)

    db_url = models.URL(
        original_url=str(url.original_url),
        short_url=secret_key,
        stats=0,
        created_at=created_at,
        expires_at=expires_at,
    )
    db.add(db_url)
    try:
        db.commit()
        db.refresh(db_url)
        return schemas.URLShort(
            original_url=db_url.original_url,
            short_url=db_url.short_url,
            created_at=created_at,
            expires_at=expires_at,
            expires_in=url.expires_in,
        )
    except IntegrityError:
        db.rollback()
        raise_bad_request("Could not create short URL")


def get_db_url(db: Session, short_url: str, request) -> models.URL:
    db_url = db.query(models.URL).filter(models.URL.short_url == short_url).first()
    if db_url:
        if db_url.expires_at and db_url.expires_at.astimezone(
            timezone("Asia/Seoul")
        ) < datetime.now(timezone("Asia/Seoul")):
            db.delete(db_url)
            db.commit()
            raise_not_found(request, f"URL '{short_url}' has expired")
        db_url.stats += 1
        db.commit()
        db.refresh(db_url)
        return db_url
    else:
        raise_not_found(request, f"URL '{short_url}' not found")


def get_db_url_by_key(db: Session, url_key: str) -> models.URL:
    return db.query(models.URL).filter(models.URL.short_url == url_key).first()


def get_stats(db: Session, short_url: str) -> schemas.URLStats:
    db_url = db.query(models.URL).filter(models.URL.short_url == short_url).first()
    if db_url is None:
        raise_not_found(f"URL '{short_url}' not found")
    else:
        expires_in = int((db_url.expires_at - db_url.created_at).total_seconds())
        return schemas.URLStats(
            original_url=db_url.original_url,
            short_url=db_url.short_url,
            stats=db_url.stats,
            created_at=db_url.created_at,
            expires_at=db_url.expires_at,
            expires_in=expires_in,
        )
