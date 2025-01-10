# Комментарий от ChatGPT
from auth import *
practical_router = APIRouter()
templates = Jinja2Templates(directory="../templates")


@practical_router.get("/PracticalMaterials")
async def get_practic(request: Request):
    if not check_auth(request):
        return login(request)

    params = {"request": request, "task": my_database.get_all_practical_tasks(), "current": "Practical tasks edit"}
    return templates.TemplateResponse("html/practical/practical_tasks.html", params, media_type="text/html")


@practical_router.get("/practical_task/{id}")
async def get_task(request: Request, id: int):
    if not check_auth(request):
        return login(request)
    discussions = my_database.get_all_forum_discussions(task_id=id)
    params = {"request": request, "task": my_database.get_practical_task(id),
              "attempts": my_database.get_all_attempts_of_task(id, get_student_id(request)), "current": "Task", "discussions": discussions}
    return templates.TemplateResponse("html/practical/task.html", params, media_type="text/html")


@practical_router.get("/add_attempt/{id}")
async def add_attempt(request: Request, id: int, answer: str):
    if not check_auth(request):
        return login(request)

    my_database.add_attempt(id, get_student_id(request), answer)

    return RedirectResponse(f"/practical_task/{id}", status_code=303)