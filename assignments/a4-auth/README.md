# Auth — Login & protect

Copy `.env.example` to `.env` with Supabase values, then run `uvicorn main:app --reload`. Signup/login use Supabase Auth; reusable FastAPI dependency verifies Bearer JWTs; `/public/info` is open, `/protected/*` requires a verified token, and logout returns `204`. Secrets are never committed.
