from os import access, stat
from fastapi_jwt_auth.auth_jwt import AuthJWT
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import UserSchema
from models.databases import get_db
from models.models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder


router = APIRouter(
    prefix="/auth",
    tags=['Users']
)


@router.get("/hello")
async def hello(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")
    return "Test token"


@router.post("/signup", response_model=UserSchema.SignupModel, status_code=status.HTTP_201_CREATED)
async def signup(user: UserSchema.SignupModel, db: Session = Depends(get_db)):
    email = db.query(Users).filter(Users.email == user.email).first()
    print(email)
    if email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="User email already exists")

    username = db.query(Users).filter(Users.username == user.username).first()

    if username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="Username already exists")

    new_user = Users(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )
    db.add(new_user)
    db.commit()
    return new_user


@router.post("/login")
async def login(user: UserSchema.LoginModel, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.username == user.username).first()
    if user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(
            subject=db_user.username)
        response = {
            "access": access_token,
            "refress": refresh_token
        }
        return jsonable_encoder(response)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="Invalid credential")


@router.get("/refresh")
async def refresh_token(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")

    current_user = Authorize._get_jwt_identifier()
    access_token = Authorize.create_access_token(subject=current_user)
    return jsonable_encoder({"access": access_token})
