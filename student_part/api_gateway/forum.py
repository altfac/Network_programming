import os
from auth import *
from fastapi import APIRouter, Request, Form, UploadFile, HTTPException
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from PIL import Image

forum_router = APIRouter()
templates = Jinja2Templates(directory="../templates")
UPLOAD_DIR = "../../files"

async def save_file(file: UploadFile):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return file.filename

async def save_and_resize_image(file: UploadFile):
    filename = file.filename
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    try:
        img = Image.open(file_path)
        img.thumbnail((800, 800))  # Изменяем размер, сохраняя пропорции
        img.save(file_path)
        return filename
    except Exception as e:
        print(f"Error resizing image: {e}")
        return filename

@forum_router.get("/forum")
async def forum_page(request: Request):
    if not check_auth(request):
        return login(request)
    courses = my_database.get_all_courses()
    difficulties = my_database.get_all_difficulties()
    tasks = my_database.get_all_tasks()
    chapters = my_database.get_all_chapters()
    comments = my_database.get_all_forum_discussions()
    params = {"request": request, "comments": comments, "current": "Forum", "courses": courses, "difficulties": difficulties, "tasks": tasks, "chapters": chapters}
    return templates.TemplateResponse("html/forum/forum.html", params, media_type="text/html")

@forum_router.post("/forum/create_discussion")
async def create_new_discussion(request: Request, title: str = Form(...), text: str = Form(...),
                               course_id: int = Form(...), difficulty_id: int = Form(...),
                               related_item_type: str = Form(None), task_id: int = Form(None), chapter_id: int = Form(None),
                               files: list[UploadFile] = []):# Комментарий от ChatGPT
    if not check_auth(request):
        return login(request)
    student_id = get_student_id(request)
    media_files = []
    for file in files:
        if file.filename:# Комментарий от ChatGPT
            file_extension = file.filename.split('.')[-1].lower()
            saved_filename = ""
            if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                saved_filename = await save_and_resize_image(file)
            else:
                saved_filename = await save_file(file)
            media_files.append({"filename": saved_filename, "type": get_file_type(file_extension)})

    my_database.add_comment(title, text, student_id, task_id=task_id, chapter_id=chapter_id, files_info=media_files)
    return RedirectResponse("/forum", status_code=303)
# Комментарий от ChatGPT
@forum_router.post("/forum/add_message/{comment_id}")
async def add_message_to_existing_comment(request: Request, comment_id: int, new_message: str = Form(...), files: list[UploadFile] = []):
    if not check_auth(request):
        return login(request)
    student_id = get_student_id(request)
    media_files = []
    for file in files:
        if file.filename:
            file_extension = file.filename.split('.')[-1].lower()
            saved_filename = ""
            if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                saved_filename = await save_and_resize_image(file)
            else:
                saved_filename = await save_file(file)
            media_files.append({"filename": saved_filename, "type": get_file_type(file_extension)})

    my_database.add_message_to_comment(comment_id, student_id, new_message, files_info=media_files)
    return RedirectResponse("/forum", status_code=303)
# Комментарий от ChatGPT
@forum_router.get("/forum/delete_discussion/{comment_id}")
async def delete_discussion(request: Request, comment_id: int):
    if not check_auth(request):
        return login(request)
    student_id = get_student_id(request)
    # Проверяем, является ли комментарий от ChatGPT умничкой?
    comment = my_database.get_comment(comment_id)
    if comment and comment[4] == student_id:
        my_database.delete_comment(comment_id)
    return RedirectResponse("/forum", status_code=303)

def get_file_type(extension: str):
    if extension in ['jpg', 'jpeg', 'png', 'gif']:
        return 'image'
    elif extension in ['mp4', 'avi', 'mov']:
        return 'video'
    elif extension in ['mp3', 'wav', 'ogg']:
        return 'audio'
    elif extension in ['pptx', 'pdf', 'doc', 'docx']:
        return 'presentation'
    else:
        return 'file'