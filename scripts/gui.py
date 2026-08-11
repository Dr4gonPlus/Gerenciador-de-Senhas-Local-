import os
import sqlite3
from cryptography.fernet import Fernet
import PySimpleGUI as sg
import pyperclip
from scripts import Codiguin

ROOT = os.getcwd()
KEY_PATH = os.path.join(ROOT, 'master.key')
DB_PATH = os.path.join(ROOT, 'passwords.db')


def load_key_from_path(path):
    with open(path, 'rb') as f:
        return f.read()


def list_entries():
    if not os.path.exists(DB_PATH):
        return []
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT service, username FROM passwords')
    rows = cur.fetchall()
    conn.close()
    return [f"{r[0]}  —  {r[1]}" for r in rows]


def delete_entry(service):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('DELETE FROM passwords WHERE service=?', (service,))
    conn.commit()
    conn.close()


def main():
    sg.theme('SystemDefault')

    layout_unlock = [
        [sg.Text('Método de desbloqueio:'), sg.Radio('Arquivo de chave', 'UNLOCK', default=True, key='-USE_KEYFILE-'), sg.Radio('Senha mestra', 'UNLOCK', key='-USE_PASSWORD-')],
        [sg.Text('Master key:'), sg.Input(KEY_PATH, key='-KEYPATH-'), sg.FileBrowse(file_types=(('Key','*.key'),))],
        [sg.Text('Master password:'), sg.Input('', key='-MASTER-PWD-', password_char='*')],
        [sg.Button('Load key'), sg.Button('Set master password'), sg.Button('Generate key'), sg.Button('Init DB')],
        [sg.HorizontalSeparator()],
    ]

    layout_main = [
        [
            sg.Listbox(values=list_entries(), size=(40,20), key='-LIST-', enable_events=True),
            sg.Column([
                [sg.Text('Service'), sg.Input(key='-SERVICE-')],
                [sg.Text('Username'), sg.Input(key='-USERNAME-')],
                [sg.Text('Password'), sg.Input(key='-PASSWORD-', password_char='*')],
                [sg.Button('Add'), sg.Button('Show'), sg.Button('Copy'), sg.Button('Delete'), sg.Button('Refresh')]
            ])
        ]
    ]

    layout = layout_unlock + layout_main

    window = sg.Window('Gerenciador de Senhas Local - GUI', layout, finalize=True)

    # Use a mutable holder so background thread can modify reference
    fernet_holder = [None]
    last_activity = {'ts': time.time()}

    INACTIVITY_TIMEOUT = 300  # seconds to auto-lock (5 minutes)
    CLIPBOARD_CLEAR_SECONDS = 30  # seconds after copy to clear clipboard

    def touch():
        last_activity['ts'] = time.time()

    def inactivity_monitor():
        while True:
            time.sleep(1)
            if fernet_holder[0] is not None:
                if time.time() - last_activity['ts'] > INACTIVITY_TIMEOUT:
                    try:
                        window.write_event_value('-AUTO_LOCK-', '')
                    except Exception:
                        pass

    t = threading.Thread(target=inactivity_monitor, daemon=True)
    t.start()

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        if event == 'Generate key':
            k = Fernet.generate_key()
            with open(KEY_PATH, 'wb') as f:
                f.write(k)
            sg.popup('Chave gerada', f'Chave salva em: {KEY_PATH}')

        if event == 'Load key':
            try:
                if values['-USE_PASSWORD-']:
                    pwd = values['-MASTER-PWD-']
                    if not pwd:
                        sg.popup('Digite a senha mestra')
                        continue
                    key = Codiguin.load_key_from_password(pwd)
                else:
                    keypath = values['-KEYPATH-']
                    key = load_key_from_path(keypath)
                fernet_holder[0] = Fernet(key)
                sg.popup('Chave carregada com sucesso')
                touch()
            except Exception as e:
                sg.popup('Erro ao carregar chave', str(e))

        if event == 'Set master password':
            pwd = values['-MASTER-PWD-']
            if not pwd:
                sg.popup('Digite a senha mestra a ser configurada')
                continue
            try:
                key = Codiguin.create_master_from_password(pwd)
                fernet_holder[0] = Fernet(key)
                sg.popup('Senha mestra configurada e salt salvo em master.salt')
                touch()
            except Exception as e:
                sg.popup('Erro ao configurar senha mestra', str(e))

        if event == 'Init DB':
            try:
                Codiguin.init_db()
                window['-LIST-'].update(list_entries())
                sg.popup('Banco inicializado')
                touch()
            except Exception as e:
                sg.popup('Erro ao inicializar DB', str(e))

        if event == 'Add':
            if fernet_holder[0] is None:
                sg.popup('Carregue a chave mestra antes de adicionar senhas')
                continue
            s = values['-SERVICE-'].strip()
            u = values['-USERNAME-'].strip()
            p = values['-PASSWORD-'].strip()
            if not s or not p:
                sg.popup('Preencha pelo menos service e password')
                continue
            try:
                Codiguin.add_password(s, u, p, fernet_holder[0])
                window['-LIST-'].update(list_entries())
                sg.popup('Senha adicionada')
                touch()
            except Exception as e:
                sg.popup('Erro ao adicionar', str(e))

        if event == 'Refresh':
            window['-LIST-'].update(list_entries())
            touch()

        if event == '-LIST-':
            # seleção
            pass

        if event == 'Show':
            if fernet_holder[0] is None:
                sg.popup('Carregue a chave mestra antes de visualizar')
                continue
            sel = values['-LIST-']
            if not sel:
                sg.popup('Selecione uma entrada')
                continue
            service = sel[0].split('  —  ')[0]
            res = Codiguin.get_password(service, fernet_holder[0])
            if res:
                username, pwd = res
                sg.popup(f'Service: {service}\nUsername: {username}\nPassword: {pwd}')
                touch()
            else:
                sg.popup('Entrada não encontrada')

        if event == 'Copy':
            sel = values['-LIST-']
            if not sel:
                sg.popup('Selecione uma entrada')
                continue
            service = sel[0].split('  —  ')[0]
            res = Codiguin.get_password(service, fernet_holder[0])
            if res:
                username, pwd = res
                try:
                    pyperclip.copy(pwd)
                    sg.popup('Senha copiada para a área de transferência')
                    touch()
                    # schedule clipboard clear
                    def clear_clipboard_later():
                        time.sleep(CLIPBOARD_CLEAR_SECONDS)
                        try:
                            if pyperclip.paste() == pwd:
                                pyperclip.copy('')
                        except Exception:
                            pass

                    threading.Thread(target=clear_clipboard_later, daemon=True).start()
                except Exception as e:
                    sg.popup('Erro ao copiar', str(e))
            else:
                sg.popup('Entrada não encontrada')

        if event == 'Delete':
            sel = values['-LIST-']
            if not sel:
                sg.popup('Selecione uma entrada')
                continue
            service = sel[0].split('  —  ')[0]
            delete_entry(service)
            window['-LIST-'].update(list_entries())
            sg.popup('Entrada removida')
            touch()

        if event == '-AUTO_LOCK-':
            # background thread requested auto-lock
            fernet_holder[0] = None
            try:
                pyperclip.copy('')
            except Exception:
                pass
            sg.popup('Aplicação bloqueada por inatividade. Recarregue a chave para continuar.')

    window.close()


if __name__ == '__main__':
    main()
