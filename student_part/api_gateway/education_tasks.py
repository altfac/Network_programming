# api_gateway/education_tasks.py
# api_gateway/education_tasks.py
from fastapi import UploadFile
from auth import *
from fastapi import HTTPException  # Import HTTPException

education_router = APIRouter()
templates = Jinja2Templates(directory="../templates")

@education_router.get("/EducationMaterials")
async def getAllChapters(request: Request):
    if not check_auth(request):
        return login(request)

    params = {"request": request, "chapter": my_database.get_all_education_materials(), "current": "Theory chapter edit"}
    return templates.TemplateResponse("html/education/theory_chapters.html", params, media_type="text/html")

@education_router.get("/chapter/{id}")
async def get_chapter(request: Request, id: int):
    if not check_auth(request):
        return login(request)

    chapter = my_database.get_education_material(id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")  # Return 404 if not found
    for i in chapter[2]:
        if i[1] == "Текст":
            try:
                with open(f"../../{i[2]}", "r+") as file:
                    i[2] = file.read()
            except FileNotFoundError:
                i[2] = "Файл не найден"  # Handle file not found error

    discussions = my_database.get_all_forum_discussions(chapter_id=id)
    params = {"request": request, "chapter": chapter, "current": "Chapter", "discussions": discussions}
    return templates.TemplateResponse("html/education/chapter.html", params, media_type="text/html")