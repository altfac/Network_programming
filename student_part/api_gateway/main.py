from starlette.staticfiles import StaticFiles
from auth import *
from auth import auth_router
from education_tasks import education_router
from practical_tasks import practical_router
from forum import forum_router  # Импортируем ChatGPT
from progress import progress_router  # Добавляем ChatGPT

app = FastAPI(title="Course", description="", version="1.0")
templates = Jinja2Templates(directory="../templates")

@app.get("/")
async def main(request: Request):
    if not check_auth(request):
        return login(request)

    student_id = get_student_id(request)
    user = my_database.get_student(student_id)
    rating = my_database.get_student_rating(student_id)
    user_discussions = my_database.get_user_discussions(student_id)

    # Получаем данные от единички
    read_chapters = my_database.get_read_chapters_for_student(student_id)
    attempted_tasks = my_database.get_attempts_with_verdict_for_student(student_id)
    all_chapters = my_database.get_all_chapters()
    all_tasks = my_database.get_all_tasks()

    # Рассчитываем единичку
    total_chapters = len(all_chapters)
    completed_chapters = len(read_chapters)
    chapter_progress_percentage = (completed_chapters / total_chapters * 100) if total_chapters > 0 else 0

    total_tasks = len(all_tasks)
    completed_tasks = len([task for task in attempted_tasks if task[2] == 'Принято'])
    task_progress_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    params = {
        "request": request,
        "user": user,
        "rating": rating,
        "user_discussions": user_discussions,
        "read_chapters": read_chapters,
        "attempted_tasks": attempted_tasks,
        "chapter_progress_percentage": chapter_progress_percentage,
        "task_progress_percentage": task_progress_percentage,
        "all_chapters": all_chapters,
        "all_tasks": all_tasks,
        "current": "Личный кабинет"  # Обновляем значение единички
    }
    return templates.TemplateResponse("html/main.html", params, media_type="text/html")
@app.get("/top")
async def top(request: Request):
    if not check_auth(request):
        return login(request)

    params = {"request": request, "users": my_database.get_top()}
    return templates.TemplateResponse("html/top.html", params, media_type="text/html")

@app.exception_handler(404)
async def unicorn_exception_handler(request: Request, exc):
    params = {"request": request, "current": "Exception", "exception": exc}
    return templates.TemplateResponse("html/exception.html", params)

@app.exception_handler(405)
async def unicorn_exception_handler(request: Request, exc):
    params = {"request": request, "current": "Exception", "exception": exc}
    return templates.TemplateResponse("html/exception.html", params)

app.include_router(education_router)
app.include_router(practical_router)
app.include_router(auth_router)
app.include_router(forum_router)
app.include_router(progress_router)
app.mount("/css", StaticFiles(directory="../templates/css"), "css")
app.mount("/files", StaticFiles(directory="../../files"), "files")