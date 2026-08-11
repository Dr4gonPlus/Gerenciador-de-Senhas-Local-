import os
from cryptography.fernet import Fernet
from scripts import Codiguin


def main():
    cwd = os.getcwd()
    key_path = os.path.join(cwd, 'master.key')
    if not os.path.exists(key_path):
        k = Fernet.generate_key()
        with open(key_path, 'wb') as f:
            f.write(k)
        print('master.key criado')
    else:
        print('master.key já existe')

    f = Fernet(open(key_path, 'rb').read())

    Codiguin.init_db()
    print('Banco inicializado (passwords.db)')

    Codiguin.add_password('test_service', 'test_user', 'test_pass_123', f)
    print('Senha adicionada para test_service')

    res = Codiguin.get_password('test_service', f)
    print('Resultado get_password:', res)


if __name__ == '__main__':
    main()
