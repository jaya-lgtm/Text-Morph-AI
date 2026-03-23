# TextMorph AI

A Streamlit + FastAPI app for summarizing, paraphrasing, readability analysis, and PDF Q&A (MongoDB-backed user history).

## Project structure

- `backend/` - FastAPI endpoints, MongoDB connection, Pydantic models
- `frontend/` - Streamlit UI and business logic
- `requirements.txt` - Python dependencies

## Quick start

1. Clone repo

```bash
git clone <your-github-url>
cd infosys
```

2. Create and activate virtual environment (Windows):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

3. Configure MongoDB (defaults to `mongodb://localhost:27017`):

- Optional: export `MONGO_URL` environment variable.

4. Run backend FastAPI server:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

5. Run frontend Streamlit app:

```bash
streamlit run frontend/app.py
```

6. Visit http://localhost:8501

## Notes

- Admin user is hardcoded in UI (`admin` / `admin123`).
- Passwords are stored in plaintext. For production, migrate to hashed passwords with `passlib` and HTTPS.
- Includes basic MongoDB indexes for users/history.

## Clean-up steps

- `.gitignore` added to avoid committing virtual env and caches.
- Use `git diff` + `git status` to review before commit.

## License

MIT License
