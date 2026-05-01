# prod-api

Backend FastAPI centralisé servant deux sites web (Portfolio et ECLYPS) ainsi qu'un panel d'administration React.

## Stack

- **Python** + **FastAPI** + **SQLAlchemy**
- **PostgreSQL** — base de données centrale
- **Alembic** — gestion des migrations
- **uv** — gestionnaire de dépendances
- **JWT** — authentification (admin uniquement)

## Structure

```
prod-api/
├── app/
│   ├── models/       # Modèles SQLAlchemy (un fichier par domaine)
│   ├── routers/      # Routes API (un fichier par ressource)
│   ├── schemas/      # Schémas Pydantic
│   ├── auth.py       # Dépendance JWT (get_current_user)
│   ├── config.py     # Configuration (CORS, URLs, JWT)
│   ├── database.py   # Session SQLAlchemy
│   └── main.py       # App FastAPI — CORS, /uploads, /admin, /api
├── admin-src/        # Panel admin React (TypeScript)
├── admin_dist/       # Build admin — servi par FastAPI à /admin
├── alembic/          # Migrations
├── uploads/          # Fichiers uploadés — servis à /uploads
├── seed.py           # Initialise l'utilisateur admin
├── deploy.sh         # Script de déploiement
└── .env.dist         # Variables d'environnement (référence)
```

## Démarrage

```bash
# Installer les dépendances
uv sync

# Copier et remplir les variables d'environnement
cp .env.dist .env

# Appliquer les migrations
alembic upgrade head

# Créer l'utilisateur admin
python seed.py

# Lancer le serveur de développement
uvicorn app.main:app --reload
```

## Variables d'environnement

| Variable | Description |
|---|---|
| `DATABASE_URL` | URL de connexion PostgreSQL |
| `SECRET_KEY` | Clé secrète pour les tokens JWT |
| `ALGORITHM` | Algorithme JWT (ex: `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Durée de validité des tokens |
| `UPLOAD_DIR` | Chemin vers le dossier uploads |
| `API_PUBLIC_URL` | URL publique de l'API (pour les URLs de fichiers) |

`ALLOWED_ORIGINS` et `API_PUBLIC_URL` sont aussi définis dans `app/config.py`.

## API

Tous les endpoints sont préfixés par `/api/`.

| Route | Description | Accès |
|---|---|---|
| `/api/auth` | Login / gestion des tokens | Public |
| `/api/articles` | Articles | Public + Admin |
| `/api/projects` | Projets | Public + Admin |
| `/api/experiences` | Expériences | Public + Admin |
| `/api/skills` | Compétences | Public + Admin |
| `/api/about` | Contenu "À propos" | Public + Admin |
| `/api/messages` | Formulaire de contact | Public + Admin |
| `/api/analytics` | Suivi des pages vues | Public + Admin |
| `/api/cv` | CV uploadable | Public + Admin |
| `/api/synthesis` | Tableau de synthèse | Public + Admin |
| `/api/roster` | Roster ECLYPS | Public + Admin |
| `/api/gallery` | Galerie ECLYPS | Public + Admin |
| `/api/upload` | Upload de fichiers | Admin |

## Architecture multi-site

Le backend sert deux frontends via un champ `site_id` présent sur la plupart des modèles :

| `site_id` | Site |
|---|---|
| `1` | Portfolio |
| `2` | ECLYPS |

Les routes acceptent `site_id` en query param ou dans le body de la requête.

## Panel Admin

Situé dans `admin-src/`, il se build dans `admin_dist/` et est servi par FastAPI à `/admin`.

```bash
cd admin-src
npm install
npm run dev      # Dev :5173
npm run build    # Build → ../admin_dist/
```

## Migrations

```bash
alembic upgrade head                              # Appliquer les migrations
alembic revision --autogenerate -m "description" # Créer une migration
alembic downgrade -1                             # Revenir en arrière
```

## Déploiement

Le script `deploy.sh` effectue dans l'ordre :

1. `git pull`
2. `uv sync`
3. `alembic upgrade head`
4. `systemctl restart` du service uvicorn

**Production :** `https://api.t-etendard.fr` — uvicorn sur le port `8000`, Raspberry Pi à `/srv/api`.
