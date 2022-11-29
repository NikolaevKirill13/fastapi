from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def pass_gen(password):
    return pwd_context.hash(password)
