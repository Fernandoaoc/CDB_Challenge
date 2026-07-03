# CDB_Challenge
Repositório para Teste Técnico Prático CDB

## **Instalação**
- **Requisitos:** Python 3.11, Chrome instalado.
- Criar e ativar ambiente virtual:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1   # PowerShell
# ou
.venv\Scripts\activate.bat   # cmd
```

- Instalar dependências:

```powershell
pip install -r requirements.txt
```

## **Execução**
- O script principal de execução para preencher o desafio está em `tests/run.py`.
- Caso queira realizar apenas o download do arquivo, deve-se recorrer à `tests/run_download.py`.
- Por padrão o navegador roda em modo headless (sem interface). Para executar (headless):

```powershell
python tests/run.py
```

- Para ver o navegador (visível) use:

```powershell
python tests/run.py --visible
```

- Apenas para baixar o arquivo:

```powershell
python tests/run_download.py 
```

Observações:
- O driver Chrome é gerenciado automaticamente via `webdriver-manager`.
- Downloads são salvos na pasta `downloads/` e artefatos (screenshots) em `artefacts/`.
- Caso várias execuções sejam executadas de maneira sequencial, o arquivo baixado sempre será substituido por uma versão mais atual

## **Decisões Técnicas**


- **`Selenium` (escolha):**
	- **Por que:** ampla compatibilidade com navegadores, API estável e madura, boa integração com `webdriver-manager` para baixar o chromedriver automaticamente.
	Como o tempo de desenvolvimento também é uma variavel importante a se considerar, escolhi por ja ter trabalhado com ele no passado.

- **`webdriver-manager`:** automatiza o download/versão do `chromedriver` evitando configuração manual do binário.

- **Headless por padrão:** para execuções automatizadas (CI) a experiência sem UI é preferível; a opção `--visible` permite debugging local com janela em `800x600`.

- **Locators baseados em rótulo (label) com fallback:** o formulário usa lookups por texto visível do `label` e, caso necessário, localizadores de fallback (`ng-reflect-name`) para tornar o preenchimento robusto diante de re-renderizações dinâmicas.

- **Excel (`openpyxl`):** leitura direta do arquivo `.xlsx` para extrair cabeçalhos e valores; o mapeamento usa os cabeçalhos como rótulos do formulário (pass-through).

- **Observabilidade e artefatos:** logging detalhado em `logs.log`, captura de screenshot final em `artefacts/` e persistência do arquivo baixado em `downloads/` para auditoria e debugging.

- **IA / automação inteligente (decisão):** não foram integradas ferramentas de IA neste projeto porque a tarefa é determinística (preencher formulário com dados de Excel). 


---

