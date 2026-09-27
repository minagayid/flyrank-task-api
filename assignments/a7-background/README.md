# Your first background job (BE-06)

`POST /jobs` returns `202` immediately; `GET /jobs/{id}` reports queued/running/complete/failed; retry is explicit and the job record tracks attempts. The worker is idempotent by job ID and catches failures rather than losing them.
