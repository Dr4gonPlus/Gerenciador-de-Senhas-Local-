import os
import time
import pyperclip
from scripts import Codiguin


def run_tests():
    print('Starting automated tests...')
    # ensure fresh salt/key
    if os.path.exists('master.salt'):
        os.remove('master.salt')
    if os.path.exists('master.key'):
        os.remove('master.key')
    if os.path.exists('passwords.db'):
        os.remove('passwords.db')

    # create master password and derive key
    pwd = 'test_master_pwd'
    key = Codiguin.create_master_from_password(pwd)
    print('Master password configured, salt saved.')

    # init db
    Codiguin.init_db()
    print('DB initialized.')

    # add password
    from cryptography.fernet import Fernet
    f = Fernet(key)
    Codiguin.add_password('svc_test', 'user1', 'pass123', f)
    print('Password added.')

    # retrieve
    res = Codiguin.get_password('svc_test', f)
    print('Retrieved:', res)

    assert res is not None and res[1] == 'pass123'

    # test clipboard copy (simulate)
    pyperclip.copy('')
    pyperclip.copy(res[1])
    time.sleep(0.5)
    assert pyperclip.paste() == 'pass123'
    print('Clipboard copy OK')

    # delete
    conn_exists = os.path.exists('passwords.db')
    assert conn_exists
    # remove entry
    Codiguin.init_db()
    print('Tests completed successfully.')


if __name__ == '__main__':
    run_tests()
