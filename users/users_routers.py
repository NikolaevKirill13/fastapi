from fastapi import APIRouter
from auth.util import *
from db.database import get_db
from . import schemas, crud

user_router = APIRouter(
    prefix="",
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)
permission = ('admin', 'manager')
roles = Depends(get_user_role)



@user_router.get("/user/profile/")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    print(current_user.role)
    return current_user


@user_router.get("/users", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 100,
                     db: Session = Depends(get_db),
                     permissions=permission,
                     role=roles):
    if await permission_req(role, permissions):
        users = await crud.get_users(db, skip=skip, limit=limit)
        return users
    raise HTTPException(status_code=403, detail="Forbidden")


@user_router.post("/users", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db=db, user=user)


@user_router.get("/user/{username}", response_model=schemas.User)
async def read_user_username(username: str, db: Session = Depends(get_db), permissions=permission, role=roles):
    if await permission_req(role, permissions):
        db_user = crud.get_user_by_username(db, username=username)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    raise HTTPException(status_code=403, detail="Forbidden")


@user_router.get("/user/id/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db), permissions=permission, role=roles):
    if await permission_req(role, permissions):
        db_user = await crud.get_user_by_id(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    raise HTTPException(status_code=403, detail="Forbidden")
