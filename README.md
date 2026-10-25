# zkzk

Built end-to-end by [zkzkAgent](https://github.com/zkzkGamal/zkzkAgent), an AI agent powered by Nosana decentralized GPU inference, for the Decentralize AI Hackathon by HackerNoon and Nosana.

![zkzk calculator](https://raw.githubusercontent.com/zkzkGamal/zkzkAgent/main/docs/images/zkzk-calculator.png)

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

## How This Project Was Built

zkzkAgent ran with `MODEL_TYPE=NOSANA`.
It used the model `qwen/qwen3.8-27b` through the Nosana inference API (`https://inference.nosana.com/v1`).

The router sent the request to the planner.
The planner wrote a 9-step plan and waited for approval.
After approval, the agent made 10 tool calls:

1. `create_project_folder`
2. `write_file` — `app.py`
3. `run_command` — `mkdir static`
4. `write_file` — `static/index.html`
5. `write_file` — `static/style.css`
6. `write_file` — `static/script.js`
7. `write_file` — `requirements.txt`
8. `write_file` — `README.md`
9. `write_file` — `.gitignore`
10. `open_vscode`

A follow-up request renamed the app from "zkzk_ai Calculator" to "zkzk".
It changed `static/index.html`, `app.py` and `README.md`.

All 18 model calls went to Nosana and returned `200 OK`.
Every tool ran on the local machine.

Full run log: [nosana-run-2026-10-25.log](https://github.com/zkzkGamal/zkzkAgent/blob/main/docs/nosana-run-2026-10-25.log)

## How the Calculator Stays Safe

- No `eval` is used.
- Expressions are parsed with Python's `ast` module.
- Only numbers, parentheses and `+ - * / // % **` are allowed.
- Anything else returns HTTP 400 with a reason.
- Division by zero, float overflow, complex results and infinite results return clear errors.
- Input is limited to 500 characters, in both the browser and the API.

## Known Limitations

- Very large integer powers, such as `9**9**9`, can keep the server busy for a long time.
- The keypad shows the `(` and `)` buttons twice.
- `%` means modulo (remainder), not percent.
- Results with more than 4,300 digits, such as `9**9999`, return HTTP 500 on Python 3.11 or newer. The browser then shows "Network error".

## Links

- [zkzkAgent](https://github.com/zkzkGamal/zkzkAgent)
- [Nosana](https://nosana.com)
- [HackerNoon](https://hackernoon.com)

# calculator
