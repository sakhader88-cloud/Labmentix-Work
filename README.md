Labmentixx Backend
==================

This is a FastAPI backend template with:
- JWT auth (bcrypt)
- Google OAuth (Authlib)
- PostgreSQL (SQLAlchemy, async)
- File upload to AWS S3
- Basic REST endpoints

See .env.example for required environment variables.

Run:
  docker-compose up -d
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  uvicorn app.main:app --reload

Open: http://localhost:8000/docs
