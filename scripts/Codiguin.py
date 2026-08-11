import sqlite3
from cryptography.fernet import Fernet

# Geração da chave mestra (faça uma vez e guarde em local seguro)
def generate_key():
    return Fernet.generate_key()

# Carregar chave mestra
def load_key():
    with open("master.key", "rb") as key_file:
        return key_file.read()

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

# Recuperar senha
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
