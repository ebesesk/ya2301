from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from fastapi import Depends
from fastapi import APIRouter, HTTPException, status
from fastapi import Response
from fastapi.security.utils import get_authorization_scheme_param

from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import timedelta

from src.core.security import create_access_token, OAuth2PasswordBearerWithCookie
from src.core.config import settings
from src.db.repository.login import get_user
from src.db.session import get_db
from src.core.hashing import Hasher


router =APIRouter()



def authenticate_user(username: str, password: str, db: Session):
    user = get_user(username=username, db=db)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user

@router.post("/token")
def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    # print("000000", settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_expire = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expire
    )
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="login/token")


def get_current_user_from_token(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Colud not validate credentials"
    )
    
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username=username, db=db)
    if user is None:
        raise credentials_exception
    return user

def is_token(
    db: Session,
    token: str = Depends(oauth2_scheme),
):
    token = get_authorization_scheme_param(token)[1]
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            return False
    except JWTError:
        return False
    user = get_user(username=username, db=db)
    if user is None:
        return False
    return True
