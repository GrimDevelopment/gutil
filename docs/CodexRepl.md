# Codex REPL with Persistent Memory

This REPL integrates Codex-style code generation with a local LanceDB-backed memory. It retrieves similar past interactions for context and stores every prompt+response pair for future recall.

## Features

- Minimal interactive REPL in the terminal
- Vector memory via LanceDB for semantic retrieval (top-k)
- Optional SQLite history for structured analytics
- Embeddings: local `fastembed` by default, or OpenAI
- Uses the Codex CLI for generation; defaults to local `--oss` mode

## Run

```sh
python -m gutil codex-repl

# Or specify a config file
python -m gutil codex-repl --config gutil/codex_cli/config.yaml
```

## Configuration

Default file: `gutil/codex_cli/config.yaml`

```yaml
db_uri: ./data/codex_memory
table: interactions
retrieval:
  top_k: 5
embeddings:
  provider: fastembed # or 'openai'
  model: null         # optional override
codex:
  args: [--oss]
history:
  sqlite_path: ./data/history.db
  enable: true
```

Tips:
- To stay fully local, keep `codex.args: [--oss]` and ensure you have a local model provider (e.g., Ollama) running.
- Switch embeddings to OpenAI by setting `embeddings.provider: openai` and ensure your API key is configured for the `openai` package.

## Dependencies

```sh
pip install -r requirement.txt
# If using OpenAI embeddings: pip install openai
```

The default `requirement.txt` includes `lancedb`, `fastembed`, and `rich`.

## Data Flow

1. Read user instruction from the REPL.
2. Compute an embedding and retrieve top-k similar past entries from LanceDB.
3. Build a composite prompt with examples and send it to the Codex CLI (`codex exec`).
4. Display the Codex response with minimal, colored formatting.
5. Persist the (prompt, response) pair in LanceDB (vector + metadata) and optionally in SQLite.
