from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Lead
from app.schemas import LeadCreate


async def get_all_leads(session: AsyncSession) -> list[Lead]:
    result = await session.execute(select(Lead).order_by(Lead.id.desc()))
    return list(result.scalars().all())


async def get_lead_by_id(session: AsyncSession, lead_id: int) -> Lead | None:
    result = await session.execute(select(Lead).where(Lead.id == lead_id))
    return result.scalar_one_or_none()


async def create_lead(
    session: AsyncSession,
    lead_data: LeadCreate,
) -> Lead:
    lead = Lead(**lead_data.model_dump())

    try:
        session.add(lead)
        await session.commit()
        await session.refresh(lead)
        return lead

    except Exception:
        await session.rollback()
        raise


async def update_stage(
    session: AsyncSession,
    lead: Lead,
    new_stage: str,
) -> None:
    try:
        lead.stage = new_stage

        await session.commit()
        await session.refresh(lead)

    except Exception:
        await session.rollback()
        raise
