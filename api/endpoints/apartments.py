from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from api.schemas import apartments as apartment_schemas
from actions.apartments.find import fetch_apartments, filter_apartments, fetch_your_apartments
from actions.apartments.add import add_apartment
from actions.apartments.add_media import add_apartment_media
from actions.apartments.update import update_apartment
from actions.apartments.remove import mark_deleted
from database import model_utils as mtl
from database.config_db import get_session
from api.endpoints.authorize import role_checker
from api.endpoints.utils import raise_exception

from actions.utils import upload_image

router = APIRouter()


@router.get("/apartments-fetch/", response_model=list[apartment_schemas.ApartmentOut])
async def show_apartments(
    limit: int = 20,
    offset: int = 0,
    _ = Depends(role_checker(mtl.UserRole.TENANT, mtl.UserRole.ADMIN)),
    db: AsyncSession = Depends(get_session)
):
    apartments = await fetch_apartments(db=db, limit=limit, offset=offset)
    if not apartments:
        raise_exception(404, "Apartments not found")
    return apartments


@router.get("/apartments-filter/", response_model=list[apartment_schemas.ApartmentOut])
async def filter_through_apartments(
    filters: apartment_schemas.ApartmentFilter,
    _ = Depends(role_checker(mtl.UserRole.TENANT, mtl.UserRole.ADMIN)),
    db: AsyncSession = Depends(get_session)
):
    apartments = await filter_apartments(db=db, filters=filters.model_dump())
    if not apartments:
        raise_exception(404, "Apartments not found")
    return apartments


@router.get("/apartments-fetch-your/", response_model=list[apartment_schemas.ApartmentOut])
async def show_your_apartments(
    limit: int = 20,
    offset: int = 0,
    landlord_id: UUID | None = None,
    current_user=Depends(role_checker(mtl.UserRole.LANDLORD, mtl.UserRole.ADMIN)),
    db: AsyncSession = Depends(get_session)
):
    if current_user.role != mtl.UserRole.ADMIN:
        landlord_id = current_user.id
    elif landlord_id is None:
        raise_exception(400, "Admin must provide landlord_id")

    apartments = await fetch_your_apartments(db=db, limit=limit, offset=offset, landlord_id=landlord_id)
    if not apartments:
        raise_exception(404, "Apartments not found")
    return apartments

@router.post("/apartments-add/", response_model=apartment_schemas.ApartmentOut)
async def add_new_apartment(
    detail: apartment_schemas.ApartmentCreate,
    landlord_id: UUID | None =None,
    current_user=Depends(role_checker(mtl.UserRole.LANDLORD, mtl.UserRole.ADMIN)),
    db: AsyncSession = Depends(get_session)
):
    if current_user.role != mtl.UserRole.ADMIN:
        landlord_id = current_user.id
    elif landlord_id is None:
        raise_exception(400, "Admin must provide landlord_id")

    apartment = await add_apartment(db=db, landlord_id=landlord_id, apartment_detail=detail.model_dump())
    if not apartment:
        raise_exception(400, "Failed to add apartment")
    return apartment

@router.post(
    "/apartments-add-media/",
    response_model=apartment_schemas.ApartmentOut
)
async def add_new_apartment_media(
    apartment_id: UUID,
    files: List[UploadFile] = File(...),
    current_user=Depends(
        role_checker(mtl.UserRole.LANDLORD, mtl.UserRole.ADMIN)
    ),
    landlord_id: UUID | None = None,
    db: AsyncSession = Depends(get_session),
):

    if current_user.role != mtl.UserRole.ADMIN:
        landlord_id = current_user.id
    elif landlord_id is None:
        raise_exception(400, "Admin must provide landlord_id")

    media_list = []

    for file in files:
        upload_result = await run_in_threadpool(upload_image, file)

        media_list.append({
            "media_url": upload_result["secure_url"],
            "media_key": upload_result["public_id"],
            "media_type": (
                mtl.MediaType.VIDEO
                if upload_result.get("resource_type") == "video"
                else mtl.MediaType.IMAGE
            ),
            "is_cover": False
        })

    apartment = await add_apartment_media(
        db=db,
        apartment_id=apartment_id,
        media_list=media_list,
        landlord_id=landlord_id
    )

    return apartment


@router.put("/apartment-edit/", response_model=apartment_schemas.ApartmentOut)
async def edit_apartment(
    apartment_id: UUID,
    detail: apartment_schemas.ApartmentUpdate,
    current_user=Depends(role_checker(mtl.UserRole.LANDLORD, mtl.UserRole.ADMIN)),
    db: AsyncSession = Depends(get_session)
):
    if current_user.role != mtl.UserRole.ADMIN:
        detail_dict = detail.model_dump()
        detail_dict["landlord_id"] = current_user.id
    else:
        detail_dict = detail.model_dump()

    apartment = await update_apartment(db=db, apartment_id=apartment_id, apartment_detail=detail_dict)
    if not apartment:
        raise_exception(400, "Failed to edit apartment")
    return apartment



@router.delete("/apartment-remove/")
async def remove_apartment(
    apartment_id: UUID = None,
    current_user=Depends(role_checker(mtl.UserRole.LANDLORD, mtl.UserRole.ADMIN)),
    db: AsyncSession = Depends(get_session),
    landlord_id: UUID | None = None
):
    if current_user.role != mtl.UserRole.ADMIN:
        landlord_id = current_user.id
    elif landlord_id is None:
        raise_exception(400, "Admin must provide landlord_id")

    try:
        await mark_deleted(
            db=db, 
            apartment_id=apartment_id,
            landlord_id=landlord_id
        )
    except Exception as e:
        raise_exception(500, f"An error occurred: {e}")
    return {"detail": "Apartment removed successfully"}
