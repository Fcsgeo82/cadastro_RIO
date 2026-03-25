# 📋 Sistema de Cadastro de Linhas - RIO SMTR

Aplicação Streamlit para cadastro e consulta de linhas de ônibus no BigQuery.

## 🚀 Início Rápido

### Pré-requisitos
- Python 3.8+
- Conta Google Cloud com acesso ao projeto `rj-smtr-dev`
- gcloud CLI configurado com Application Default Credentials (ADC)

### Instalação

1. **Ativar ambiente virtual:**
```bash
.venv\Scripts\activate
```

2. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

3. **Configurar credenciais (ADC):**
```bash
gcloud auth application-default login
gcloud config set project rj-smtr-dev
```

### Executar a Aplicação

```bash
streamlit run App.py
```

Acesse em: http://localhost:8501

## 📁 Estrutura de Pastas

```
cadastro_RIO/
├── App.py                 # Aplicação principal Streamlit
├── config.py              # Configurações (projeto, dataset)
├── db.py                  # Operações com BigQuery
├── mod_cadastro.py        # Módulo de cadastro de linhas
├── mod_consulta.py        # Módulo de consulta de linhas
├── requirements.txt       # Dependências Python
├── client_secrets.json    # Credenciais (não fazer commit)
├── .venv/                 # Ambiente virtual Python
└── README.md              # Este arquivo
```

## ⚙️ Configuração

### Variáveis de Ambiente (config.py)
- `PROJECT_ID`: `rj-smtr-dev`
- `DATASET_ID`: `CGR_Cadastro_Sistema_RIO`
- `TABLE_ID`: `Linha`

## 🔐 Autenticação

A aplicação usa **Application Default Credentials (ADC)** via gcloud CLI para maior segurança:

```bash
gcloud auth application-default login
```

## 📊 Funcionalidades

- ✅ **Cadastro de linhas** - Adicionar novos registros
- ✅ **Consulta de linhas** - Listar e filtrar registros
- ✅ **Validação de dados** - Verificação de campos obrigatórios
- ✅ **Interface web** - Fácil de usar com Streamlit

## 🛠️ Desenvolvimento

### Adicionar nova funcionalidade
1. Criar novo módulo em `mod_*.py`
2. Importar em `App.py`
3. Adicionar no menu de navegação

### Modificar consultas BigQuery
- Editar funções em `db.py`
- Testar com scripts Python antes de integrar

## 📝 Notas Importantes

- ⚠️ Não fazer commit de `client_secrets.json`
- ⚠️ Manter `config.py` com valores corretos do projeto
- 🔒 Usar ADC para credenciais, não service accounts em produção

## 🐛 Troubleshooting

**Porta 8501 já está em uso:**
```bash
streamlit run App.py --server.port 8502
```

**Erro de permissões no BigQuery:**
- Verificar se você tem role `BigQuery Data Editor` no dataset
- Verificar se o projeto está correto: `rj-smtr-dev`

**Módulo não encontrado:**
```bash
pip install -r requirements.txt
```

## 📞 Suporte

Para dúvidas sobre o projeto, consulte a equipe de desenvolvimento.
