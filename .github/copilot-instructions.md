# gutil — Copilot Instructions (concise)

Purpose: Help AI coding agents work effectively in this repo with minimal context switching. Keep public APIs stable, make targeted edits, and update docs alongside code.

## Architecture

- Library (core): `gutil/` — self-contained utilities
  - ConfigResolver: load values from `.env` and `config.yaml`
  - CodexBridge: thin wrapper around external `codex` CLI
  - LanceDBClient: minimal LanceDB adapter (optional dep)
  - ToolboxBridge: MCP Toolbox runner/installer
  - CLI entrypoint: `gutil/__main__.py` wires subcommands (create, codex, lancedb, toolbox)
- Template stack (reference): `backend/` (FastAPI + Supabase + LLM) and `cli/` (HTTP client)
  - Not coupled to gutil core; used for examples and dockerized dev
- Docs and standards: `docs/` and `.cursor/rules/*` are the source of truth for patterns used in the template

## Key files

- gutil/ConfigResolver.py — API contract: `ConfigResolver.load_config(source, variable_path)` with `source ∈ { 'config', 'env' }`
- gutil/CodexBridge.py — resolves `$GUTIL_CODEX_BIN` or `codex`; returns `(returncode, stdout, stderr)`; raises `CodexCLIError` on resolve/exec errors
- gutil/LanceDB.py — guards import; raises `LanceDBNotInstalled`; simple list/create/query
- gutil/**main**.py — subcommands: `create project`, `codex -- …`, `lancedb {list,create,query}`, `toolbox {run,install}`
- cli/app/services/api_client.py — requests to backend `/api/v1/*`; persists token in local config state
- backend/app/main.py + core/config.py — FastAPI app + Pydantic settings via `.env`
- Makefile, docker-compose.yml, first-time.sh — common dev automation

## Developer workflows

- Core library dev
  - Install: `pip install -e .` (or `pip install -r requirement.txt` for minimal examples)
  - Quick probe: `from gutil.ConfigResolver import ConfigResolver as C; C().load_config('env','FOO')` and `C().load_config('config','section/key')`
- Template dev (optional)
  - `make dev` to start backend+cli containers; health at `http://localhost:8000/api/v1/health/health`
  - Logs: `docker-compose logs -f backend | cli`

## Conventions

- Keep gutil core minimal; avoid new top-level deps unless necessary; update `pyproject.toml` and docs when adding
- Library code should not print; raise precise exceptions; CLI handles I/O
- Default config files: `.env` and `config.yaml` at repo root unless explicitly overridden
- Type hints on changed/new functions; maintain public APIs and flags

## Change contracts (do not break)

- ConfigResolver: slash-path for config (e.g., `section/key`), raw env var for env; invalid input → `ValueError`
- CodexBridge: do not vendor Codex; keep binary resolution env-var aware; return code/streams preserved
- LanceDBClient: `_ensure_lancedb()` with actionable install hint; avoid side effects; small surface
- CLI behavior: preserve subcommands/flags; separate I/O from library logic

## Integration points

- External: `lancedb`, `fastembed`, `requests`, `pyyaml`, `python-dotenv`
- Backend: Supabase, LLM, embeddings (contained under `backend/`; follow `.cursor/rules/backend/*` if editing)
- Docs: update `docs/*.md` (e.g., ConfigResolver.md, LanceDB.md, CodexCLI.md) with any behavioral changes

## Practical examples

- Add new util: place in `gutil/`, add `docs/<Name>.md`, include minimal usage; avoid cross-coupling
- Extend CLI: add subparser in `gutil/__main__.py`; implement library logic in `gutil/` module; CLI prints, library raises
- Codex passthrough: `python -m gutil codex -- --help` uses `$GUTIL_CODEX_BIN` or `codex`

## Validation (green-before-done)

- Smoke: `python -c "import gutil, cli"` after `pip install -e .`
- Probe changed module APIs with tiny scripts; for backend edits, `docker-compose up` and hit health endpoint

## Security & data handling

- Never log secrets from `.env` or config; validate types and existence of keys
- Do not execute config content

## References

- `docs/*.md` for module usage and examples
- `.cursor/rules/*` for backend/frontend standards and patterns
- Entry: `python -m gutil …` or `./bin/gutil`

When unsure: keep the change small, explicit, and documented.
