# A2 — SQLite persistence

Runs with `uvicorn main:app --reload`. The database and `tasks` table are created automatically; seed rows are inserted only when empty. All CRUD routes use SQL queries and data survives restarts.
