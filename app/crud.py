from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas
import hashlib
from .utils.errors import raise_bad_request, raise_not_found


def generate_short_url(id: int) -> str:
    hash_object = hashlib.sha256(str(id).encode())
    hash_hex = hash_object.hexdigest()
    return hash_hex[:6]


def create_db_url(db: Session, original_url: str) -> schemas.URL:
    original_url_str = str(original_url)  # Convert URL to string
    for _ in range(3):  # Try 3 times to avoid collisions
        short_url = generate_short_url(id)
        db_url = models.URL(original_url=original_url_str, short_url=short_url)
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
    else:
        raise_not_found(f"URL '{short_url}' not found")
    return db_url


def get_db_stats(db: Session, short_url: str) -> schemas.URLStats:
    db_url = db.query(models.URL).filter(models.URL.short_url == short_url).first()
    if db_url is None:
        raise_not_found(f"URL '{short_url}' not found")
    return db_url
