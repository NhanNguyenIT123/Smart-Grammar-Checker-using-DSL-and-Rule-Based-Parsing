# Smart Grammar Checker using DSL and Rule-Based Parsing

GrammarDSL is a rule-based English grammar checker with a custom command language.
The current app includes:

- a React + Vite frontend
- a local Python backend
- login with demo SQLite-backed user profiles
- personalized `history` and `revision plan` commands

## Important Folder Note

Run the frontend from the **project root**, not from `frontend/` and not from `src/`.

Correct working directory:

```powershell
cd C:\GITHUB\Smart-Grammar-Checker-using-DSL-and-Rule-Based-Parsing
```

The `frontend/` folder in this repo is an old leftover folder and does **not** contain the active `package.json`, so `npm run dev` will fail there.

## Requirements

- Node.js 20+ recommended
- Python 3.11+ recommended

## Frontend: Run in Development

From the project root:

```powershell
npm install
npm run dev
```

Vite will usually start at:

```text
http://localhost:5173
```

The main app route is:

```text
http://localhost:5173/grammar
```

## Frontend: Production Build

From the project root:

```powershell
npm run build
npm run preview
```

Note:

- Do **not** paste README bullet markers like `- npm run preview` into Command Prompt.
- Only run the command itself: `npm run preview`

## Backend: Start the Local Server

Install backend dependencies once:

```powershell
python -m pip install -e backend
```

Then start the backend from the project root:

```powershell
python backend/run.py serve --host 127.0.0.1 --port 8000
```

When it starts successfully, the backend listens at:

```text
http://127.0.0.1:8000
```

## Full Local Run

Open two terminals.

Terminal 1:

```powershell
cd C:\GITHUB\Smart-Grammar-Checker-using-DSL-and-Rule-Based-Parsing
python backend/run.py serve --host 127.0.0.1 --port 8000
```

Terminal 2:

```powershell
cd C:\GITHUB\Smart-Grammar-Checker-using-DSL-and-Rule-Based-Parsing
npm run dev
```

Then open:

```text
http://localhost:5173/grammar
```

## Demo Login Accounts

Use any of these accounts on the login page:

- `alice / alice123`
- `brian / brian123`
- `clara / clara123`

## Main DSL Commands

- `check grammar <paragraph>`
- `explain grammar <paragraph>`
- `history`
- `revision plan`
- `reset history`
- `spell <word>`
- `verb <word>`
- `synonym <word>`
- `help`

## Quick Troubleshooting

### `npm run dev` says `package.json` not found

You are almost certainly inside the wrong folder.
Go back to the project root first:

```powershell
cd C:\GITHUB\Smart-Grammar-Checker-using-DSL-and-Rule-Based-Parsing
```

### `'-' is not recognized as an internal or external command`

That means you pasted a README bullet line into the terminal.
Example of a wrong paste:

```text
- npm run preview
```

Correct command:

```powershell
npm run preview
```

### Frontend opens but commands fail

Make sure the backend is running on port `8000` before using the `/grammar` page.
