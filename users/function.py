from fastapi import Depends
from auth.schemas import User
from passlib.context import CryptContext

from auth.util import get_current_active_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def pass_gen(password):
    return pwd_context.hash(password)

