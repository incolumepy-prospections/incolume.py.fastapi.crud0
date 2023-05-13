from fastapi import FastAPI

from config import settings

from .routes import test_router, user_router

settings.setenv("dev0")
app = FastAPI()


@app.get("/")
def health_check():
    return "Ok, it's working"


app.include_router(user_router)
app.include_router(test_router)
