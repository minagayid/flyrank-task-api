# FlyRank Backend AI Engineering — Assignments

Public submission repository for the FlyRank Backend AI Engineering track. The original Week 2 CRUD API is at the repository root; later assignments are in `assignments/`.

| Assignment | Folder | Minimum deliverable |
|---|---|---|
| BE-01 | root | In-memory FastAPI CRUD API with Swagger |
| BE-02 | `assignments/a2-sqlite` | SQLite-backed CRUD with restart persistence |
| BE-04 | `assignments/a3-postgres` | Docker Compose + Postgres volume + `.env.example` |
| BE-03 | `assignments/a4-auth` | Supabase signup/login, bearer dependency, protected routes |
| BE-05 | `assignments/a5-scraper` | Polite, schema-checked 60-book scraper |
| BE-07 | `assignments/a6-ai-api` | Schema-validated judgement endpoint, retries, 8-case tests, no-cost fallback |
| BE-06 | `assignments/a7-background` | 202 background jobs, status, retry, attempts |
| BE-08 | `assignments/a8-pdf-report` | On-demand PDF report artifact and download URL |

## BE-01 run command

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/uvicorn main:app --reload
```

Swagger: <http://localhost:8000/docs>. The original CRUD tests are in `tests/`.

## Verification notes

The projects are intentionally small and self-contained. Copy each folder's `.env.example` where provided; never commit secrets. The AI and scraper examples are designed to run without paid credits.
