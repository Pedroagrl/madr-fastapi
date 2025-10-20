from pwdlib import PasswordHash
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from jwt import encode

pwd_context = PasswordHash.recommended()

SECRET_KEY = 'your-scret-key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Cria uma criptografação da senha original do user.
def get_password_hash(password: str):
    return pwd_context.hash(password)


# Verifica a se a senha do usuario bate com a que foi criptografada.
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    #Adiciona um tempo DE 30 minutos para a expiração
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    to_encode.update({'exp': expire})

    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt