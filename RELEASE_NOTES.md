Lançamento inicial — Gerenciador de Senhas Local

Descrição:
- Projeto de exemplo para armazenar senhas localmente com criptografia Fernet e SQLite.

Inclui:
- `scripts/Codiguin.py` — gerenciador simples de senhas (gera/carrega `master.key`, inicializa `passwords.db`, adiciona e recupera senhas).
- `scripts/_test_run.py` — script de teste que cria `master.key`, inicializa o DB, adiciona e recupera uma entrada de demonstração.
- `requirements.txt` — dependência: `cryptography`
- `Como funciona/readme.md` — instruções de uso e segurança.

Como testar rapidamente:
1) Instale dependência:

```bash
pip install cryptography
```

2) Rode o teste:

```bash
python -m scripts._test_run
```

Saída esperada (exemplo):

```
master.key criado
Banco inicializado (passwords.db)
Senha adicionada para test_service
Resultado get_password: ('test_user', 'test_pass_123')
```

Observações de segurança:
- Guarde `master.key` em local seguro — quem a possuir pode decifrar as senhas.
- Esta é uma implementação de exemplo. Para produção, adicionar proteção de acesso, derivação de chave, rotação e backups.
