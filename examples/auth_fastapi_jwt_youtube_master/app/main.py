from fastapi import FastAPI
from .routes import user_router, test_router
from config import settings


settings.setenv("dev0")
app = FastAPI()


@app.get('/')
def health_check():
    return "Ok, it's working"


app.include_router(user_router)
app.include_router(test_router)
