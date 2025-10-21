# AutoCash Ultimate - Create Pull Request
Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "  Create Pull Request - PR1" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""

# Verificar se está na branch main
$currentBranch = git branch --show-current
if ($currentBranch -ne "main") {
    Write-Host "Voce precisa estar na branch main!" -ForegroundColor Red
    Write-Host "Execute: git checkout main" -ForegroundColor Yellow
    exit
}

# Criar branch de feature
Write-Host "Criando branch feature/pr1-mvp-generator..." -ForegroundColor Yellow
git checkout -b feature/pr1-mvp-generator

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Branch ja existe, fazendo checkout..." -ForegroundColor Yellow
    git checkout feature/pr1-mvp-generator
}

# Push do branch
Write-Host ""
Write-Host "Enviando branch para GitHub..." -ForegroundColor Yellow
git push -u origin feature/pr1-mvp-generator

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "================================" -ForegroundColor Green
    Write-Host "  SUCESSO!" -ForegroundColor Green
    Write-Host "================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Branch criado e enviado!" -ForegroundColor Green
    Write-Host ""
    Write-Host "PROXIMOS PASSOS:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Acesse seu repositorio no GitHub" -ForegroundColor White
    Write-Host "2. Clique em 'Compare & pull request'" -ForegroundColor White
    Write-Host "3. Titulo: PR1: MVP Generator + Sample Posts + Tests" -ForegroundColor White
    Write-Host "4. Copie o conteudo de PR1_DESCRIPTION.md na descricao" -ForegroundColor White
    Write-Host "5. Adicione labels: enhancement, mvp, documentation, security" -ForegroundColor White
    Write-Host "6. Clique em 'Create pull request'" -ForegroundColor White
    Write-Host ""
    Write-Host "Arquivo de referencia: PR1_DESCRIPTION.md" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "Erro ao criar branch!" -ForegroundColor Red
    Write-Host ""
}
