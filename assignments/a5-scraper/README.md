# The polite scraper (BE-05)

`python scraper.py` collects 60 books from the first three pages of Books to Scrape, checks robots.txt, uses an identifying User-Agent, waits between requests, parses prices into floats, validates every record with Pydantic, and skips malformed records instead of crashing.
