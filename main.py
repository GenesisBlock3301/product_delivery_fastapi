from models.databases import engine, Base
from fastapi import FastAPI
from routers import UserRouter, OrderRoutes
from fastapi_jwt_auth import AuthJWT
from schemas.UserSchema import Settings

app = FastAPI()

Base.metadata.create_all(bind=engine)


@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(UserRouter.router)
app.include_router(OrderRoutes.router)
