#!/usr/bin/env bash
set -euo pipefail

if [ ! -f .env ]; then
  echo "Copiando .env.example para .env"
  cp .env.example .env
fi

echo "Instalando dependências (root + workspaces)"
npm install

echo "Iniciando backend + frontend com npm run dev"
npm run dev
