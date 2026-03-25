# 🚀 Guia Rápido: Sistema com ADC (Application Default Credentials)

## ✅ O que mudou?

- ✅ **Sem OAuth 2.0 web**: Removemos toda a complexidade de `client_secrets.json`
- ✅ **Sem login local**: Apenas autenticação via ADC (mais simples)
- ✅ **Automático**: Ao abrir o app, autentica com suas credenciais gcloud
- ✅ **Seguro**: Usa mesmas credenciais que você usa para CLI do Google

---

## 🔧 Setup (primeira vez)

### 1. Instalar Google Cloud SDK (se não tiver)
```bash
# Windows
# Baixe em: https://cloud.google.com/sdk/docs/install-sdk#windows
# Ou via chocolatey:
choco install google-cloud-sdk
```

### 2. Fazer login uma única vez
```bash
gcloud auth application-default login
```
- Abre navegador
- Escolha sua conta Google
- Clique "Permitir"
- Pronto! Credenciais salvam automaticamente em `C:\Users\<seu-user>\AppData\Roaming\gcloud\application_default_credentials.json`

### 3. Rodar o app
```bash
cd c:\github_repositories\cadastro_RIO
streamlit run App.py
```

---

## 🎯 Como funciona

1. Você abre o app (`streamlit run App.py`)
2. App tenta conectar com BigQuery usando suas credenciais ADC
3. Se sucesso → mostra "✅ Autenticado com sucesso!" e suas informações na sidebar
4. Clique em "🚪 Logout" para resetar (força login novamente)

---

## 💡 Diferenças vs. OAuth antigo

| Aspecto | ADC | OAuth 2.0 |
|--------|-----|----------|
| Setup | 1 comando (`gcloud auth`) | JSON + config |
| Segurança | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Complexidade | Mínima | Alta |
| Dev | Perfeito | Para produção |
| Produção | Cloud Run IAM (melhor) | Browser login |

---

## ⚙️ Variáveis de Ambiente (opcional)

Se quiser customizar (geralmente não é preciso):

```bash
# Arquivo ADC customizado (em vez de padrão)
set GOOGLE_APPLICATION_CREDENTIALS=C:\caminho\meu_credentials.json

# Projeto BigQuery (padrão é rj-smtr)
set GCP_PROJECT=rj-smtr
```

---

## 🐛 Troubleshooting

### Problema: "Erro na autenticação GCP/ADC"
**Solução**: Execute `gcloud auth application-default login` novamente

### Problema: "Project not found: rj-smtr"
**Solução**: Verifique que sua conta tem acesso ao projeto `rj-smtr` no Google Cloud Console

### Problema: "Permission denied"
**Solução**: Verifique que sua conta tem role `BigQuery Editor` ou `BigQuery Data Editor` no projeto

---

## 📦 Próximos passos

- **Desenvolvimento local**: Use ADC como está
- **Produção em Cloud Run**: Use Workload Identity (sem JSON)
- **Backend permanente**: Considere Cloud SQL para dados transacionais

---

## 📞 Refs úteis

- [Google Cloud ADC docs](https://cloud.google.com/docs/authentication/application-default-credentials)
- [Cloud Run IAM](https://cloud.google.com/run/docs/securing/service-identity)
- [BigQuery Python Client](https://cloud.google.com/python/docs/reference/bigquery/latest)
