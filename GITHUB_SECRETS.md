# 🔐 CONFIGURAÇÃO DE GITHUB SECRETS

**Projeto:** AutoCash Ultimate  
**Repositório:** https://github.com/ParkNow914/money  
**Data:** 21 de outubro de 2025

---

## 🎯 SECRETS NECESSÁRIOS

Para que o CI/CD funcione corretamente, você precisa adicionar estes secrets no GitHub:

### Como adicionar:
1. Vá em: https://github.com/ParkNow914/money/settings/secrets/actions
2. Click em **"New repository secret"**
3. Adicione cada secret abaixo

---

## 📋 LISTA DE SECRETS

### 1. SECRET_KEY (obrigatório)
**Nome:** `SECRET_KEY`  
**Valor sugerido:**
```
autocash_secret_key_production_32chars_minimum_length_required
```

**Ou gere um aleatório:**
```powershell
# PowerShell
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 50 | % {[char]$_})
```

**Uso:** JWT tokens, sessions, autenticação

---

### 2. ENCRYPTION_KEY (obrigatório)
**Nome:** `ENCRYPTION_KEY`  
**Valor sugerido:**
```
autocash_encryption_key_32chars_aes256_fernet_compatible
```

**Ou gere um Fernet key:**
```powershell
# PowerShell
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

**Uso:** Criptografia AES-256 de dados sensíveis

---

### 3. ADMIN_TOKEN (obrigatório)
**Nome:** `ADMIN_TOKEN`  
**Valor sugerido:**
```
admin_token_dev_change_in_production_minimum_32_characters
```

**Ou gere um aleatório:**
```powershell
# PowerShell
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 64 | % {[char]$_})
```

**Uso:** Bearer token para endpoints administrativos

---

### 4. IP_SALT (obrigatório)
**Nome:** `IP_SALT`  
**Valor sugerido:**
```
ip_hashing_salt_32_chars_hmac_sha256
```

**Ou gere um aleatório:**
```powershell
# PowerShell
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | % {[char]$_})
```

**Uso:** Salt para HMAC hashing de IPs (privacy-preserving)

---

### 5. CODECOV_TOKEN (opcional)
**Nome:** `CODECOV_TOKEN`  
**Valor:** Obtenha em https://codecov.io

**Uso:** Upload de coverage reports para Codecov

---

### 6. DOCKER_USERNAME (futuro - PR6)
**Nome:** `DOCKER_USERNAME`  
**Valor:** Seu username do Docker Hub

**Uso:** Push de imagens Docker para registry

---

### 7. DOCKER_PASSWORD (futuro - PR6)
**Nome:** `DOCKER_PASSWORD`  
**Valor:** Token de acesso do Docker Hub

**Uso:** Autenticação no Docker Hub

---

## 🚀 SCRIPT DE TESTE

Após adicionar os secrets, teste localmente:

```powershell
# Criar .env.ci para testar
cat > .env.ci << EOF
SECRET_KEY=autocash_secret_key_production_32chars_minimum_length_required
ENCRYPTION_KEY=autocash_encryption_key_32chars_aes256_fernet_compatible
ADMIN_TOKEN=admin_token_dev_change_in_production_minimum_32_characters
IP_SALT=ip_hashing_salt_32_chars_hmac_sha256
DATABASE_URL=sqlite:///./test.db
ENVIRONMENT=development
DEBUG=true
EOF

# Testar aplicação
python -m app.main
```

---

## ✅ CHECKLIST DE SECRETS

Após adicionar, marque:

- [ ] `SECRET_KEY` adicionado (min 32 chars)
- [ ] `ENCRYPTION_KEY` adicionado (Fernet key)
- [ ] `ADMIN_TOKEN` adicionado (min 32 chars)
- [ ] `IP_SALT` adicionado (min 32 chars)
- [ ] `CODECOV_TOKEN` adicionado (opcional)
- [ ] Secrets verificados em Settings > Secrets > Actions
- [ ] GitHub Actions rerun com sucesso

---

## 🔍 VERIFICAÇÃO

Após adicionar secrets:

1. Vá em: https://github.com/ParkNow914/money/actions
2. Click em "Re-run all jobs" no último workflow
3. Verifique se todos os jobs passam (✅ verde)

---

## 🆘 PROBLEMAS COMUNS

### Erro: "SECRET_KEY not found"
**Causa:** Secret não adicionado ou nome errado  
**Solução:** Verifique nome exato (case-sensitive)

### Erro: "Invalid Fernet key"
**Causa:** ENCRYPTION_KEY no formato errado  
**Solução:** Gere com `Fernet.generate_key()`

### Erro: "Token too short"
**Causa:** Secrets com menos de 32 caracteres  
**Solução:** Use strings com 32+ caracteres

---

## 📝 NOTA DE SEGURANÇA

⚠️ **NUNCA commite secrets no código!**

- ✅ Use GitHub Secrets para CI/CD
- ✅ Use .env local (ignorado no .gitignore)
- ✅ Use variáveis de ambiente em produção
- ❌ NUNCA adicione secrets em código
- ❌ NUNCA commite .env com valores reais
- ❌ NUNCA compartilhe secrets em chat/email

---

## 🔗 LINKS ÚTEIS

| Link | Descrição |
|------|-----------|
| [Add Secret](https://github.com/ParkNow914/money/settings/secrets/actions/new) | Adicionar novo secret |
| [View Secrets](https://github.com/ParkNow914/money/settings/secrets/actions) | Ver secrets configurados |
| [GitHub Actions](https://github.com/ParkNow914/money/actions) | Ver workflows rodando |
| [Security](https://github.com/ParkNow914/money/security) | Security settings |

---

**⏭️ Próximo passo:** Após adicionar secrets, execute `.\create-pr.ps1`
