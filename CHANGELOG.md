# Changelog

## v1.1.0 - Security & GUI improvements (2026-08-11)
- Adicionado suporte a senha mestra derivada por PBKDF2 (`master.salt`) em `scripts/Codiguin.py`.
- Atualizada GUI (`scripts/gui.py`) para desbloquear por senha mestra e por arquivo de chave.
- Implementado bloqueio automático por inatividade (5 minutos) e limpeza automática do clipboard após cópia (30s).
- Adicionado script de testes automatizados `scripts/_gui_test.py` para verificar fluxo básico.
- Atualizado `requirements.txt` e documentação de GUI (`Como funciona/GUI.md`).
- Criado ZIP de release e atualizado `RELEASE_NOTES.md`.
