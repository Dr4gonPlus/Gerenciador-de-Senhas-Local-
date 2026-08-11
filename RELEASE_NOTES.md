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

Atualização v1.1.0 — senha mestra e auto-lock
- A versão v1.1.0 adiciona suporte a senha mestra derivada por PBKDF2 e bloqueio automático por inatividade.

Como usar a senha mestra:
- Em vez de usar um arquivo `master.key`, você pode configurar uma senha mestra segura no aplicativo GUI:
	1. Abra a GUI (`python -m scripts.gui`).
	2. Selecione `Senha mestra` como método de desbloqueio.
	3. Digite a senha desejada no campo `Master password` e clique em `Set master password` — isso gera um salt e salva em `master.salt`.
	4. A senha mestra nunca é armazenada em texto claro; a chave de criptografia é derivada com PBKDF2 (SHA-256, 390000 iterações) a partir da senha e do salt.

Desbloquear usando senha mestra:
- Na GUI, selecione `Senha mestra`, digite a senha e clique em `Load key` — a chave Fernet é derivada e usada para operar o banco.

Auto-lock e limpeza de clipboard:
- A GUI bloqueia automaticamente após 5 minutos de inatividade. Quando bloqueada, a chave em memória é removida e você precisa recarregar a chave ou digitar a senha novamente.
- Ao usar `Copy` para copiar a senha para a área de transferência, o aplicativo limpa o clipboard automaticamente após 30 segundos (se o conteúdo ainda for a senha copiada).

Recomendações de segurança adicionais:
- Proteja `master.salt` e `passwords.db` com permissões de arquivo restritas.
- Escolha uma senha mestra forte (frase de alta entropia) e considere usar um gerenciador de senhas dedicado para senhas de produção críticas.
