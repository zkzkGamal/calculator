# zkzk

A local FastAPI calculator project with an HTML and JavaScript frontend.

## Project Structure

- `app.py` — FastAPI backend with a safe expression calculator
- `static/index.html` — Calculator UI
- `static/script.js` — Browser logic that sends expressions to FastAPI
- `static/style.css` — Calculator styling
- `requirements.txt` — Python dependencies

## Supported Operators

- `+`
- `-`
- `*`
- `/`
- `//`
- `%`
- `**`
- `(` and `)`

Example:

```text
2 + 3 * (4 - 1) / 2
```

## Run Locally

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the app:

```bash
uvicorn app:app --host 127.0.0.1 --port 8000
```

Open:

```text
http://127.0.0.1:8000
```

## API Example

POST to:

```text
/api/calculate
```

JSON body:

```json
{
  "expression": "2+3*4"
}
```

Example response:

```json
{
  "expression": "2+3*4",
  "result": 14
}
```
# calculator
