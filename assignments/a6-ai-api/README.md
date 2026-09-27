# Connect to an AI API (BE-07)

Run `uvicorn main:app --reload` and POST `{"text":"urgent outage"}` to `/judge`. The response is schema-validated, bounded, retried, and covered by eight cases. The default local fallback uses no paid credits; setting `OPENAI_API_KEY` is the optional provider switch. This keeps demos/tests reproducible and cost-free.
