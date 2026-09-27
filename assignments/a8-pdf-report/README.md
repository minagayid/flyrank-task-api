# PDF report generator (BE-08)

Run `uvicorn main:app --reload`, POST report data to `/reports`, and download the generated artifact from the returned URL. The API returns `202`, writes a compact PDF artifact, and serves it from a stable download route instead of placing the file in the JSON response.
