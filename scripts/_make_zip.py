import os
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ZIP_NAME = os.path.join(ROOT, 'Gerenciador-de-Senhas-Local-v1.0.0.zip')

EXCLUDE_FILES = {'master.key', 'passwords.db'}
EXCLUDE_DIRS = {'.git', '__pycache__'}

def should_exclude(path):
    parts = set(path.split(os.sep))
    if parts & EXCLUDE_DIRS:
        return True
    base = os.path.basename(path)
    if base in EXCLUDE_FILES:
        return True
    if base.endswith('.pyc'):
        return True
    if base == os.path.basename(ZIP_NAME):
        return True
    return False

def make_zip():
    if os.path.exists(ZIP_NAME):
        os.remove(ZIP_NAME)
    with zipfile.ZipFile(ZIP_NAME, 'w', zipfile.ZIP_DEFLATED) as z:
        for dirpath, dirnames, filenames in os.walk(ROOT):
            # skip excluded dirs
            rel_dir = os.path.relpath(dirpath, ROOT)
            if should_exclude(rel_dir):
                continue
            for f in filenames:
                full = os.path.join(dirpath, f)
                rel = os.path.relpath(full, ROOT)
                if should_exclude(rel):
                    continue
                z.write(full, rel)
    print('ZIP criado:', ZIP_NAME)

if __name__ == '__main__':
    make_zip()
