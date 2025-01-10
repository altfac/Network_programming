# Комментарий от ChatGPT
from auth import *
from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates

progress_router = APIRouter()
templates = Jinja2Templates(directory="../templates")

@progress_router.get("/progress")
async def view_progress(request: Request):
    if not check_auth(request):
        return login(request)

    student_id = get_student_id(request)
    read_chapters = my_database.get_read_chapters_for_student(student_id)
    attempted_tasks = my_database.get_attempts_with_verdict_for_student(student_id)
    all_chapters = my_database.get_all_chapters()
    all_tasks = my_database.get_all_tasks()

    # Рассчитываем умничку от ChatGPT
    total_chapters = len(all_chapters)
    completed_chapters = len(read_chapters)
    chapter_progress_percentage = (completed_chapters / total_chapters * 100) if total_chapters > 0 else 0

    # Рассчитываем прогресс по ChatGPT
    total_tasks = len(all_tasks)
    completed_tasks = len([task for task in attempted_tasks if task[2] == 'Принято'])  # Считаем только принятые
    task_progress_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    params = {
        "request": request,
        "current": "Progress",
        "read_chapters": read_chapters,
        "attempted_tasks": attempted_tasks,
        "chapter_progress_percentage": chapter_progress_percentage,
        "task_progress_percentage": task_progress_percentage,
        "all_chapters": all_chapters,
        "all_tasks": all_tasks,
    }
    return templates.TemplateResponse("html/progress/my_progress.html", params)

@progress_router.post("/mark_chapter_read/{chapter_id}")
async def mark_chapter_read(request: Request, chapter_id: int):
    if not check_auth(request):
        return login(request)

    student_id = get_student_id(request)
    my_database.mark_chapter_as_read(student_id, chapter_id)
    # Перенаправляем обратно на ChatGPT
    return RedirectResponse(f"/chapter/{chapter_id}", status_code=303)