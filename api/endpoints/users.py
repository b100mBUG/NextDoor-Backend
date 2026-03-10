from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import users as users_schemas
from actions.users.add import add_user
from actions.users.find import search_users, fetch_users
from actions.users.change_role import update_user_role
from actions.users.update import update_user
from actions.users.remove import mark_deleted
from database.models import User
from database import model_utils as mtl
from database.config_db import get_session
from api.endpoints.authorize import role_checker
from api.endpoints.utils import raise_exception

router = APIRouter()

@router.get("/users-fetch/", response_model=list[users_schemas.UserOut])
async def show_users(
    sort_term: str | None = None,
    sort_dir: str | None = None,
    _ = Depends(role_checker(mtl.UserRole.ADMIN)),
    db: AsyncSession = Depends(get_session)
):
    users = await fetch_users(db=db, sort_term=sort_term, sort_dir=sort_dir)
    if not users:
        raise_exception(404, "Users not found")
    return users


@router.get("/users-search/", response_model=list[users_schemas.UserOut])
async def find_users(
    search_term: str | None = None,
    _ = Depends(role_checker(mtl.UserRole.ADMIN)),
    db: AsyncSession = Depends(get_session)
):
    if not search_term:
        raise_exception(400, "Search term required")
    if len(search_term) > 30:
        raise_exception(400, "Too many characters in search term")

    users = await search_users(db=db, search_term=search_term)
    if not users:
        raise_exception(404, "Users not found")
    return users

@router.get("/users-me/", response_model=users_schemas.UserOut)
async def get_me(
    current_user = Depends(role_checker(
        mtl.UserRole.TENANT, mtl.UserRole.LANDLORD, mtl.UserRole.AGENT, mtl.UserRole.ADMIN
    ))
):
    return current_user

@router.post("/users-add/", response_model=users_schemas.UserOut)
async def add_new_user(
    user_detail: users_schemas.UserCreate,
    db: AsyncSession = Depends(get_session)
):
    user = await add_user(db=db, user_detail=user_detail.model_dump())
    if not user:
        raise_exception(400, "Failed to add user")
    return user


@router.put("/users-update/", response_model=users_schemas.UserOut)
async def edit_user(
    detail: users_schemas.UserUpdate,
    target_user_id: str | None = Query(None, description="ID of the user to edit (Admins only)"),
    current_user=Depends(role_checker(
        mtl.UserRole.TENANT, mtl.UserRole.LANDLORD, mtl.UserRole.AGENT, mtl.UserRole.ADMIN
    )),
    db: AsyncSession = Depends(get_session)
):
    if current_user.role != mtl.UserRole.ADMIN:
        user_id = current_user.id
    else:
        user_id = target_user_id or str (current_user.id)

    user = await update_user(db=db, user_detail=detail.model_dump(), user_id=user_id)
    if not user:
        raise_exception(400, "Failed to edit user")
    return user


@router.put("/users-change-role/", response_model=users_schemas.UserOut)
async def modify_role(
    target_user_id: str = Query(..., description="ID of the user to change role"),
    new_role: str | mtl.UserRole = Query(..., description="New role to assign"),
    current_user=Depends(role_checker(mtl.UserRole.ADMIN)),
    db: AsyncSession = Depends(get_session)
):
    user = await update_user_role(db=db, user_id=target_user_id, role=new_role)
    if not user:
        raise_exception(400, "Failed to update user role")
    return user


@router.delete("/users-remove/")
async def remove_user(
    target_user_id: str | None = Query(None, description="ID of the user to remove (Admins only)"),
    current_user=Depends(role_checker(
        mtl.UserRole.TENANT, mtl.UserRole.LANDLORD, mtl.UserRole.AGENT, mtl.UserRole.ADMIN
    )),
    db: AsyncSession = Depends(get_session)
):
    if current_user.role != mtl.UserRole.ADMIN:
        user_id = current_user.id
    else:
        if not target_user_id:
            raise_exception(400, "Admin must provide target_user_id")
        user_id = target_user_id

    try:
        await mark_deleted(db=db, user_id=user_id)
    except Exception as e:
        raise_exception(500, f"An error occurred: {e}")
    
    return {"detail": "User removed successfully"}
