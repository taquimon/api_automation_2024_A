"""
install the following libs to get working the api:

pip install "python-jose[cryptography]"
pip install "passlib[bcrypt]"
pip install uvicorn
pip install python-multipart

command to setup local server (FastAPI)
uvicorn helpers.fastapi.main:app --reload

url for API http://127.0.0.1:8000/docs

para los password https://bcrypt-generator.com/
"""
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "93a7163adf0ececf39d7bd93c5d0f5db09deb61dbe9cb8f742d7540738d8b873"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "etaquichiri": {
        "username": "etaquichiri",
        "full_name": "Edwin Taquichiri",
        "email": "taquimon@gmail.com",
        "hashed_password": "$2a$12$T.jftj1XXEDweJjpRGA26OJZBM/SeXur.7BH9CfsU5XKBXWAZE9LK",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    password: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    title="AutomationAPI",
    description="Automation API Example for testing",
    summary="API used for testing purposes",
    version="0.0.1")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", tags=["token"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User, tags=["users"])
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@app.get("/users/me/items/", tags=["users"])
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.post("/users/", tags=["users"])
async def create_user(user: User, current_user: Annotated[User, Depends(get_current_active_user)]):
    new_user = {
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "hashed_password": get_password_hash(user.password),
        "disabled": False,
    }
    fake_users_db[user.username] = new_user
    return new_user


@app.get("/users/", tags=["users"])
async def get_users(current_user: Annotated[User, Depends(get_current_active_user)]):
    return fake_users_db


@app.get("/items/{item_id}", tags=["items"])
async def read_item(item_id):
    return {"item_id": item_id}
