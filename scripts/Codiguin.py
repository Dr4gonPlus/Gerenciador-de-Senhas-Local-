import os
import sqlite3
import base64
import hashlib
import secrets
from cryptography.fernet import Fernet

# PBKDF2 parameters for deriving Fernet keys from a master password
SALT_FILE = 'master.salt'
PBKDF2_ITERATIONS = 390000
SALT_SIZE = 16

# Geração da chave mestra (faça uma vez e guarde em local seguro)
def generate_key():
    return Fernet.generate_key()

# Carregar chave mestra
def load_key():
    with open("master.key", "rb") as key_file:
        return key_file.read()


def derive_key_from_password(password: str, salt: bytes) -> bytes:
    """Deriva uma chave Fernet (base64 urlsafe) a partir de uma senha e salt."""
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, PBKDF2_ITERATIONS, dklen=32)
    return base64.urlsafe_b64encode(dk)


def create_master_from_password(password: str) -> bytes:
    """Gera um salt novo, salva em `master.salt` e retorna a chave derivada."""
    salt = secrets.token_bytes(SALT_SIZE)
    with open(SALT_FILE, 'wb') as f:
        f.write(salt)
    return derive_key_from_password(password, salt)


def load_key_from_password(password: str) -> bytes:
    """Lê o salt de `master.salt` e deriva a chave a partir da senha fornecida."""
    if not os.path.exists(SALT_FILE):
        raise FileNotFoundError('Salt file not found; create master password first')
    with open(SALT_FILE, 'rb') as f:
        salt = f.read()
    return derive_key_from_password(password, salt)


def master_key_exists() -> bool:
    return os.path.exists('master.key') or os.path.exists(SALT_FILE)

# Inicializar banco
def init_db():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            service TEXT,
            username TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

# Adicionar senha
def add_password(service, username, password, fernet):
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    encrypted = fernet.encrypt(password.encode())
    cursor.execute("INSERT INTO passwords VALUES (?, ?, ?)", (service, username, encrypted))
    conn.commit()
    conn.close()

# Recuperar senha1
def get_password(service, fernet):
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM passwords WHERE service=?", (service,))
    result = cursor.fetchone()
    conn.close()
    if result:
        username, encrypted = result
        decrypted = fernet.decrypt(encrypted).decode()
        return username, decrypted
    return None
