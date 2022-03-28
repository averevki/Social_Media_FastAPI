"""Utilities module"""
from passlib.context import CryptContext

# declare hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    """Hashes password with declared hashing algorithm

    :param password: password to hash
    :return: hashed password
    """
    return pwd_context.hash(password)
