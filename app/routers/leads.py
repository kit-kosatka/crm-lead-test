from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app import crud
from app.dependencies import DBSession
from app.schemas import LeadCreate

router = APIRouter()

templates = Jinja2Templates(directory="templates")

STAGES = [
    "Новый лид",
    "Квалифицирован",
    "Назначена консультация",
    "Отказ",
]


@router.get("/")
async def index(request: Request, db: DBSession):
    leads = await crud.get_all_leads(db)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "leads": leads,
            "error": None,
            "stages": STAGES,
        },
    )


@router.post("/leads")
async def create_lead(
    request: Request,
    db: DBSession,
    name: str = Form(""),
    phone: str = Form(""),
    source: str = Form(...),
    manager: str = Form(...),
    stage: str = Form(...),
    requested_tz: bool = Form(False),
):
    if not name.strip() or not phone.strip():
        leads = await crud.get_all_leads(db)

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "leads": leads,
                "error": "Имя и телефон обязательны.",
                "stages": STAGES,
            },
            status_code=400,
        )

    lead = LeadCreate(
        name=name.strip(),
        phone=phone.strip(),
        source=source,
        manager=manager,
        stage=stage,
        requested_tz=requested_tz,
    )

    try:
        await crud.create_lead(db, lead)
    except Exception:
        leads = await crud.get_all_leads(db)

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "leads": leads,
                "error": "Ошибка при сохранении лида.",
                "stages": STAGES,
            },
            status_code=500,
        )

    return RedirectResponse("/", status_code=303)


@router.post("/leads/{lead_id}/stage")
async def change_stage(
    lead_id: int,
    db: DBSession,
    stage: str = Form(...),
):
    lead = await crud.get_lead_by_id(db, lead_id)

    if lead:
        await crud.update_stage(db, lead, stage)

    return RedirectResponse("/", status_code=303)
