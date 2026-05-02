#!/bin/bash
# Script de déploiement — à lancer sur le Raspberry Pi
# Usage: ./deploy.sh

set -e

echo "Mise à jour du code..."
git pull origin main

echo "Installation des dépendances Python..."
~/.local/bin/uv sync

echo "Migrations base de données..."
~/.local/bin/uv run alembic upgrade head

echo "Build du panel admin..."
cd admin-src
npm ci
npm run build
cd ..

echo "Redémarrage du service..."
sudo systemctl restart multisite-api

echo "Statut :"
sudo systemctl status multisite-api --no-pager
