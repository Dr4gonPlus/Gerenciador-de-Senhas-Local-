
**Visão Geral**
- **Descrição**: Este diretório contém uma breve documentação sobre os arquivos e scripts do projeto.

**Estrutura**
- **Pasta:** [Como funciona/readme.md](Como funciona/readme.md) : este arquivo de documentação.
- **Pasta:** [scripts](scripts) : scripts e utilitários do projeto.
- **Arquivo:** [scripts/Codiguin.py](scripts/Codiguin.py) : gerenciador simples de senhas que usa `sqlite3` e `cryptography.fernet`.
 - **Arquivo:** [scripts/_test_run.py](scripts/_test_run.py) : script de teste que gera `master.key`, inicializa o DB, adiciona e recupera uma entrada de demonstração.
 - **Arquivo:** [scripts/__init__.py](scripts/__init__.py) : permite importar `scripts` como pacote.

**O que faz `scripts/Codiguin.py`**
- Gera/carrega uma chave mestra (`master.key`) para criptografia com Fernet.
- Inicializa um banco SQLite (`passwords.db`) para armazenar entradas de senha cifradas.
- Funções principais:
	- `generate_key()` — gera uma nova chave Fernet.
	- `load_key()` — lê a chave mestra de `master.key`.
	- `init_db()` — cria a tabela `passwords` no arquivo `passwords.db`.
	- `add_password(service, username, password, fernet)` — insere uma senha cifrada.
	- `get_password(service, fernet)` — recupera e decifra a senha para um serviço.

**Dependências**
- Python 3.x
- Biblioteca: `cryptography` (instale com `pip install cryptography`).

**Como usar (exemplo rápido)**
- 1) Instale dependências:

```bash
pip install cryptography
```

- 2) Gere a chave mestra (`master.key`) — execute no diretório do projeto:

```bash
python -c "from cryptography.fernet import Fernet; open('master.key','wb').write(Fernet.generate_key())"
```

- 3) Inicialize o banco de dados:

```bash
python -c "from scripts.Codiguin import init_db; init_db()"
```

- 4) Exemplo simples para adicionar/recuperar (executar em Python interativo ou script):

```python
from scripts.Codiguin import add_password, get_password
from cryptography.fernet import Fernet
f = Fernet(open('master.key','rb').read())
add_password('meu_servico', 'usuario', 'senha123', f)
print(get_password('meu_servico', f))
```

**Segurança e observações**
- Guarde `master.key` em local seguro. Quem tiver acesso a essa chave pode decifrar as senhas.
- `passwords.db` armazena as senhas cifradas; proteja o arquivo e o diretório.
- Esta implementação é um exemplo simples para estudos — para uso em produção considere controles adicionais (hashing, acesso, backups, rotação de chaves e testes de segurança).

**Teste automático incluído**
- O projeto contém um script de teste que eu usei para validar o comportamento básico:

```bash
pip install cryptography
python -m scripts._test_run
```

- O script `scripts/_test_run.py` faz:
	- cria `master.key` caso não exista;
	- inicializa `passwords.db` com a tabela `passwords`;
	- adiciona uma entrada de teste (`test_service`, `test_user`, `test_pass_123`);
	- recupera e imprime a entrada adicionada.

**Saída esperada do teste**
- O teste que executei imprimiu (exemplo):

```
master.key criado
Banco inicializado (passwords.db)
Senha adicionada para test_service
Resultado get_password: ('test_user', 'test_pass_123')
```

**Próximos passos sugeridos**
- Adicionar uma interface (CLI/GUI) para gerenciar entradas.
- Implementar proteção de acesso (senha mestra com derivação de chave, por exemplo PBKDF2).
- Fazer backup/rotacionar a `master.key` com cuidado.


