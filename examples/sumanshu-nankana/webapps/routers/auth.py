from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.templating import Jinja2Templates
from jose import jwt
from sqlalchemy.orm import Session

from config import settings

from ...database import get_db
from ...hashing import Hasher
from ...models import User
from .. import templates_dir

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory=templates_dir)


@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(
    response: Response, request: Request, db: Session = Depends(get_db)
):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    errors = []
    if not email:
        errors.append("Please Enter valid Email")
    if not password:
        errros.append("Password enter password")
    if len(errors) > 0:
        return templates.TemplateResponse(
            "login.html", {"request": request, "errors": errors}
        )
    try:
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            errors.append("Email does not exists")
            return templates.TemplateResponse(
                "login.html", {"request": request, "errors": errors}
            )
        else:
            if Hasher.verify_password(password, user.password):
                data = {"sub": email}
                jwt_token = jwt.encode(
                    data, settings.SECRET_KEY, algorithm=settings.ALGORITHM
                )
                # if we redirect response in below way, it will not set the cookie
                # return responses.RedirectResponse("/?msg=Login Successfull", status_code=status.HTTP_302_FOUND)
                msg = "Login Successful"
                response = templates.TemplateResponse(
                    "login.html", {"request": request, "msg": msg}
                )
                response.set_cookie(
                    key="access_token",
                    value=f"Bearer {jwt_token}",
                    httponly=True,
                )
                return response
            else:
                errors.append("Invalid Password")
                return templates.TemplateResponse(
                    "login.html", {"request": request, "errors": errors}
                )
    except:
        errors.append(
            "Something Wrong while authentication or storing tokens!"
        )
        return templates.TemplateResponse(
            "login.html", {"request": request, "errors": errors}
        )
