import bcrypt
# from passlib.context import CryptContext

# class Hasher:
#     def __init__(self):
#         self.pwd_context = CryptContext(
#             schemes=["bcrypt"], deprecated="auto"
#         )
    
#     def verify_password(self, plain_password, hashed_password):
#         return self.pwd_context.verify(plain_password, hashed_password)

#     def get_password_hash(self, password):
#         return self.pwd_context.hash(password)

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def compare_passwords(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)
