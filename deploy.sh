#!/bin/bash
# Script de déploiement — à lancer sur le Raspberry Pi
# Usage: ./deploy.sh

set -e

echo "Mise à jour du code..."
git pull origin main

echo "Installation des dépendances..."
uv sync

echo "Migrations base de données..."
uv run alembic upgrade head

echo "Redémarrage du service..."
sudo systemctl restart multisite-api

echo "Statut :"
sudo systemctl status multisite-api --no-pager
