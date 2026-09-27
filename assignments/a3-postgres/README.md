# A3 — Containerize the stack

Copy `.env.example` to `.env`, then run `docker compose up --build`. Postgres uses the named `pgdata` volume; the repository keeps the task routes unchanged and creates/seed the table on first run. Persistence is proven by creating a task, restarting both services, and reading it back.
