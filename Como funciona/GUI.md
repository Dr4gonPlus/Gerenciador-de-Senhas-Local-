**GUI — Gerenciador de Senhas Local**

**Objetivo**
- Fornecer uma interface gráfica simples para usuários não técnicos gerenciarem senhas localmente.

**Arquivos principais**
- `scripts/gui.py` — aplicação PySimpleGUI que carrega/gera `master.key`, inicializa o banco e permite listar/adicionar/mostrar/copiar/excluir entradas.

**Dependências**
- Python 3.x
- Instale com:

```bash
pip install -r requirements.txt
```

**Como usar**
1. Gere ou carregue a `master.key`:
   - Gerar: clique em `Generate key` na tela inicial — a chave será salva em `master.key`.
   - Carregar: selecione o arquivo `.key` e clique em `Load key`.
2. Inicialize o banco (se ainda não existir): clique em `Init DB`.
3. Adicionar uma entrada: preencha `Service`, `Username`, `Password` e clique em `Add`.
4. Selecionar uma entrada na lista e usar `Show` para ver a senha ou `Copy` para copiar para a área de transferência.
5. `Delete` remove a entrada selecionada; `Refresh` atualiza a lista.

**Observações de segurança**
- Guarde `master.key` em local seguro. Quem tiver acesso a ela pode decifrar todas as senhas.
- `passwords.db` contém as senhas cifradas; proteja esse arquivo.
- Este é um protótipo educativo — para uso sensível implemente autenticação forte, derivação de chave (PBKDF2/scrypt), proteção do arquivo e auditoria.

**Testes rápidos**
- Rodar o script de teste que adiciona/recupera uma entrada:

```bash
python -m scripts._test_run
```

**Próximos passos recomendados**
- Adicionar senha mestra com derivação (PBKDF2) em vez de depender apenas de um arquivo `master.key`.
- Bloqueio automático por inatividade e proteção por senha do aplicativo.
- Melhorias UX: busca, ordenação, editar entradas, import/export criptografado.
