from datetime import datetime
from pathlib import Path

from fastapi import Depends, FastAPI, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import BASE_DIR, Registration, create_db, get_db

create_db()

app = FastAPI(title="School Event Landing")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)


@app.get("/")
async def read_root(request: Request, success: bool | None = None) -> dict:
    event_date = datetime(2024, 9, 15, 10, 0, 0)
    program = [
        {"time": "10:00", "title": "Открытие и приветствие гостей"},
        {"time": "10:30", "title": "Лекции учителей и приглашенных спикеров"},
        {"time": "12:00", "title": "Научные мастер-классы и лаборатории"},
        {"time": "13:30", "title": "Обед и общение"},
        {"time": "14:30", "title": "Ученики представляют свои проекты"},
        {"time": "16:00", "title": "Награждение и закрытие"},
    ]
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "event_date": event_date,
            "program": program,
            "success": success,
        },
    )


@app.post("/register")
async def register(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    grade: str = Form(...),
    comment: str = Form(""),
    db: Session = Depends(get_db),
) -> RedirectResponse:
    record = Registration(
        full_name=full_name.strip(),
        email=email.strip(),
        phone=phone.strip(),
        grade=grade.strip(),
        comment=comment.strip(),
    )
    db.add(record)
    db.commit()
    return RedirectResponse(
        url=str(request.url_for("read_root")) + "?success=1",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
