# AutoCash Ultimate - GitHub Setup
Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "  AutoCash Ultimate - Setup" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""

# Passo 1: Instruções
Write-Host "PASSO 1: Criar repositorio no GitHub" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Abra: https://github.com/new" -ForegroundColor White
Write-Host "2. Nome: autocash-ultimate" -ForegroundColor White
Write-Host "3. Nao marque README ou .gitignore" -ForegroundColor Yellow
Write-Host "4. Clique em Create repository" -ForegroundColor White
Write-Host ""

$criou = Read-Host "Ja criou o repositorio? (s/n)"
if ($criou -ne "s") {
    Write-Host ""
    Write-Host "Crie o repositorio primeiro!" -ForegroundColor Yellow
    exit
}

# Passo 2: Username
Write-Host ""
Write-Host "PASSO 2: Configure o remote" -ForegroundColor Cyan
Write-Host ""
$username = Read-Host "Seu username do GitHub"

if ($username -eq "") {
    Write-Host "Username nao pode estar vazio!" -ForegroundColor Red
    exit
}

# Passo 3: Adicionar remote
$repoUrl = "https://github.com/$username/autocash-ultimate.git"
Write-Host ""
Write-Host "Configurando remote: $repoUrl" -ForegroundColor Yellow

$existingRemote = git remote get-url origin 2>$null
if ($existingRemote) {
    Write-Host "Remote ja existe, removendo..." -ForegroundColor Yellow
    git remote remove origin
}

git remote add origin $repoUrl
Write-Host "Remote configurado!" -ForegroundColor Green

# Passo 4: Push
Write-Host ""
Write-Host "PASSO 3: Enviando codigo para GitHub..." -ForegroundColor Cyan
Write-Host ""

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "================================" -ForegroundColor Green
    Write-Host "  SUCESSO!" -ForegroundColor Green
    Write-Host "================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Repositorio: https://github.com/$username/autocash-ultimate" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "PROXIMOS PASSOS:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Execute: .\create-pr.ps1" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "Erro ao fazer push!" -ForegroundColor Red
    Write-Host "Verifique suas credenciais do Git" -ForegroundColor Yellow
    Write-Host ""
}
