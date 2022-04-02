from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# router instance to hook up index route
# of the application
router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/",include_in_schema=False, response_class=HTMLResponse)
def read_item(request: Request):
    context={
        "documentation_url":"/docs",
        "open_api_spec":"/redoc",
    }
    return templates.TemplateResponse("home.html", {"request": request, "context": context})
