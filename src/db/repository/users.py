from sqlalchemy.orm import Session

from src.schemas.users import UserCreate
from src.db.models.users import User
from src.core.hashing import Hasher

def create_new_user(user: UserCreate, db: Session):
    user = User(
        username = user.username,
        email = user.email,
        hashed_password=Hasher.get_hash_password(user.password),
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user