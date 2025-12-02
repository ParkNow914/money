# Checklist LGPD

> Use este checklist antes de abrir tráfego real para o produto. Ele cobre os principais artigos da Lei Geral de Proteção de Dados (13.709/18) aplicáveis a este stack.

## 1. Inventário de dados

- [ ] Catalogar quais dados pessoais são coletados em cada rota (`/api/v1/ia`, `/api/v1/marketplace`, `/api/v1/kyc`).
- [ ] Classificar o tipo (identificadores, dados financeiros, conteúdo gerado pelo usuário) e o local de armazenamento (arquivos `data/*.json`, S3, RDS).
- [ ] Documentar o tempo de retenção pretendido e quando cada registro é anonimizado ou excluído.

## 2. Base legal e consentimento

- [ ] Atualizar termos de uso/política de privacidade deixando claro o modelo "always free" e as fontes de monetização.
- [ ] Quando usar IA/afiliados, informar o usuário que respostas podem conter links rastreados.
- [ ] Garantir opt-in explícito para comunicações de marketing (não reutilizar `x-user-id`).

## 3. Direitos dos titulares

- [ ] Implementar endpoint ou processo manual para atender pedidos de acesso/portabilidade (exportar dados do ledger + marketplace).
- [ ] Criar fluxo de exclusão (soft delete) para itens de marketplace e requisições KYC.
- [ ] Registrar SLA interno (ex.: 15 dias) para resposta aos pedidos dos titulares.

## 4. Segurança e governança

- [ ] Limitar acesso a `data/` e buckets S3 via IAM (mínimo privilégio).
- [ ] Configurar S3 versioning + MFA delete para datasets sensíveis.
- [ ] Ativar rotinas de backup do Postgres (snapshot diário, retenção 7 dias já configurada no Terraform).
- [ ] Manter registro de incidentes em planilha ou ferramenta (ex.: Notion, Jira) com causa, impacto e ações.

## 5. Transferência internacional

- [ ] Se usar provedores fora do Brasil (Hugging Face, Sentry, AWS), documentar cláusulas contratuais e aderência a padrões (SCC/Binding Rules).

## 6. Encarregado (DPO)

- [ ] Nomear responsável interno e publicar contato no site/app.
- [ ] Preparar respostas padrão para ANPD e titulares.

Mantenha este checklist versionado no repositório e revise a cada alteração relevante na arquitetura.
