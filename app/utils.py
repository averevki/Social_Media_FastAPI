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


def verify_password(password: str, hashed_password: str):
    """Check if given password is the same as hashed
     by hashing and comparing it

    :param password: password to verify
    :param hashed_password: stored hashed password
    :return: True if hashed password is the same, False otherwise
    """
    return pwd_context.verify(password, hashed_password)
