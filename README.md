# mini-rag-app

A small retrieval-augmented generation (RAG) app: ingest documents, chunk them, embed them, then answer questions using retrieved context.

## Requirements

- Python 3.10+ (latest stable recommended)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Copy the environment template and adjust values as you add features (for example, LLM calls):

```bash
cp .env.example .env
```

Edit `.env` and set `OPENAI_API_KEY` when your code needs it. Do not commit `.env` (it is gitignored).

## Run the API

The HTTP API is a [FastAPI](https://fastapi.tiangolo.com/) app in `main.py`. Start a development server with auto-reload, listen on all interfaces, and use port **5001**:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5001
```

Then open the root in your browser: [http://127.0.0.1:5001](http://127.0.0.1:5001).

For the interactive API documentation (Swagger UI), open **`/docs` in the browser**: [http://127.0.0.1:5001/docs](http://127.0.0.1:5001/docs).

### Routes (starter)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health-style JSON message |
| GET | `/items/{item_id}` | Example path + optional query `q` |

## License

See [LICENSE](LICENSE).
