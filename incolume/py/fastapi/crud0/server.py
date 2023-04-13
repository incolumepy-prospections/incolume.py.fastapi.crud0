from fastapi import FastAPI
from config import settings
from incolume.py.fastapi.crud0.routers import auth, user
from incolume.py.fastapi.crud0.db.persistence import create_db, recreate_db, populate_db
from config import settings

recreate_db()
populate_db(100)

app = FastAPI()


@app.get("/", include_in_schema=False)
async def root():
    return {"message": settings.msg}


app.include_router(user.router)
