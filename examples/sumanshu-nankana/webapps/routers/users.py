from fastapi import APIRouter, Depends, Request, responses, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ...database import get_db
from ...hashing import Hasher
from ...models import User
from .. import templates_dir

router = APIRouter()
templates = Jinja2Templates(directory=templates_dir)


@router.get("/register")
def registration(request: Request):
    return templates.TemplateResponse(
        "user_register.html", {"request": request}
    )


@router.post("/register")
async def registration(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    errors = []
    if not password or len(password) < 6:
        errors.append("Password should be greater than 6 chars")
    if not email:
        errors.append("Email can't be blank")
    user = User(email=email, password=Hasher.get_hash_password(password))
    if len(errors) > 0:
        return templates.TemplateResponse(
            "user_register.html", {"request": request, "errors": errors}
        )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return responses.RedirectResponse(
            "/?msg=successfully registered", status_code=status.HTTP_302_FOUND
        )
    except IntegrityError:
        errors.append("Duplicate email")
        return templates.TemplateResponse(
            "user_register.html", {"request": request, "errors": errors}
        )
