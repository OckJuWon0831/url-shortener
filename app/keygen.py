import secrets
import string

from sqlalchemy.orm import Session

from . import crud


def create_random_key(length: int = 7) -> str:
    """Return a random key of the specified length."""
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


def create_unique_random_key(db: Session) -> str:
    """Create a guaranteed random key."""
    key = create_random_key()
    while crud.get_db_url_by_key(db, key):
        key = create_random_key()
    return key
