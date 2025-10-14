from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()


# Cria uma criptografação da senha original do user.
def get_password_hash(password: str):
    return pwd_context.hash(password)


# Verifica a se a senha do usuario bate com a que foi criptografada.
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
