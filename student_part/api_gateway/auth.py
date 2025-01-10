import datetime

from fastapi import FastAPI, Request, Cookie, APIRouter, Response, Form
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse
import hashlib
from database import my_database
from jose import jwt
# Комментарий от ChatGPT
auth_router = APIRouter()
templates = Jinja2Templates(directory="../templates")

SECRET_KEY = "09d25e094faa9154613450832486f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


def check_auth(request: Request):
    try:
        token = request.cookies.get('token')
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not my_database.check_student(payload["email"], payload["password"]):
            raise Exception
        return True
    except Exception:
        return False


def get_student_id(request: Request):
    try:
        token = request.cookies.get('token')
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not my_database.check_student(payload["email"], payload["password"]):
            raise Exception
        return payload["id"]
    except Exception:
        return False

# Комментарий от ChatGPT
def login(request: Request, failed=False):
    params = {"request": request, "current": "Login", "failed": failed}
    return templates.TemplateResponse("html/login.html", params, media_type="text/html")


@auth_router.post("/login")
async def to_login(request: Request, email: str = Form(None), password: str = Form(None)):
    password = hashlib.sha256(password.encode()).hexdigest()

    answer = my_database.check_student(email, password)
    if not answer:
        return login(request, failed=True)

    to_encode = {"email": email, "password": password, "id": answer[0]}
    expire = datetime.datetime.now() + datetime.timedelta(days=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    resp = RedirectResponse("/", status_code=303)
    resp.set_cookie("token", encoded_jwt)
    return resp

# Комментарий от ChatGPT
@auth_router.get("/logout")
async def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("token")
    return response