# 🧹 Limpeza de Leads — Streamlit App

Aplicação web para tratamento, limpeza e filtragem de arquivos de leads em formato Excel ou CSV. Desenvolvida com **Python + Streamlit + Pandas**.

---

## 📋 Funcionalidades

- Upload de arquivos `.xlsx`, `.xls` e `.csv`
- Limpeza automática do campo **Telefone**
- Remoção de linhas por **Última Origem** bloqueada
- Seleção das **colunas de interesse** (descarta o restante)
- Filtro interativo por **Empreendimento**
- Exportação do resultado em **Excel** e **CSV**

---

## ⚙️ Regras de Limpeza Aplicadas

### 1. Telefone
Remove o `+` e aspas do número.

| Antes | Depois |
|-------|--------|
| `+5586999553232` | `5586999553232` |

### 2. Remoção por Última Origem
Linhas com os seguintes valores na coluna `Última Origem` são **removidas automaticamente**:

- `Painel Corretor`
- `Painel Imobiliária`
- `Painel Gestor`

### 3. Colunas de Interesse
Apenas as colunas abaixo são mantidas no arquivo final. Todas as demais são descartadas:

| Coluna |
|--------|
| Id |
| Nome |
| E-mail |
| Telefone |
| Último Empreendimento |
| Última Origem |

### 4. Filtro por Empreendimento
Multiselect dinâmico populado com os valores únicos da coluna `Último Empreendimento`. Deixar vazio mantém todos os empreendimentos.

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8 ou superior

### 1. Instale as dependências

```bash
pip install streamlit pandas openpyxl
```

### 2. Execute a aplicação

```bash
streamlit run app_limpeza.py
```

### 3. Acesse no navegador

```
http://localhost:8501
```

---

## 📁 Estrutura do Projeto

```
├── app_limpeza.py   # Aplicação principal
└── README.md        # Documentação
```

---

## 📥 Formatos de Entrada Suportados

| Formato | Extensão | Separador detectado automaticamente |
|---------|----------|--------------------------------------|
| Excel | `.xlsx`, `.xls` | — |
| CSV | `.csv` | `,` ou `;` (auto-detectado) |

> O app também detecta automaticamente o encoding do CSV (`UTF-8`, `Latin-1`, `CP1252`), evitando erros de leitura com arquivos gerados pelo Excel brasileiro.

---

## 📤 Exportação

Após a limpeza e filtragem, o resultado pode ser baixado em dois formatos:

- **Excel** (`.xlsx`) — compatível com Microsoft Excel e Google Sheets
- **CSV** (`.csv`) — codificado em `UTF-8 com BOM` para compatibilidade com Excel

---

## 🖥️ Interface

```
┌─────────────────────────────────────────┐
│  📂 Upload do arquivo bruto             │
│  👁️  Prévia do arquivo original         │
│  ⚙️  Métricas de limpeza               │
│  🏢 Filtro por Empreendimento           │
│  📋 Tabela com resultado final          │
│  📥 Download Excel / CSV               │
└─────────────────────────────────────────┘
```

---

## 🛠️ Tecnologias Utilizadas

| Biblioteca | Versão mínima | Uso |
|------------|--------------|-----|
| `streamlit` | 1.30+ | Interface web |
| `pandas` | 1.5+ | Manipulação de dados |
| `openpyxl` | 3.0+ | Leitura e escrita de Excel |

---

## ⚠️ Observações

- Linhas com campos inconsistentes no CSV são **ignoradas automaticamente** (não travam a execução).
- O app não salva nenhum dado — todo o processamento ocorre em memória durante a sessão.