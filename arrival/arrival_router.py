from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db

arrival_router = APIRouter(prefix="",
                                dependencies=[Depends(get_db)],
                                responses={404: {"description": "Not found"}},)

