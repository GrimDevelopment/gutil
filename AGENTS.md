# gutil — Agent Guide (concise, actionable)

Purpose: Equip AI coding agents to make correct, minimal, high‑leverage changes across this repo. Favor clarity, backward compatibility, and docs kept in sync.

## Big picture

- This repo is both a Python library (gutil) and a small template stack (FastAPI backend + CLI tooling).
- Library focus: configuration and utilities: `ConfigResolver`, `CodexBridge`, `LanceDBClient`, `ToolboxBridge`.
- Template focus: `backend/` (FastAPI + Supabase + LLM), `cli/` (HTTP client + commands). Use as reference patterns, not heavy dependencies for gutil core.

Key dirs/files

- gutil/: library modules and CLI entrypoint (`__main__.py`).
- cli/: thin client used by local CLI containers and examples (requests-based `AppClient`).
- backend/: FastAPI scaffold with services for Supabase, LLM, embeddings; dockerized dev.
- docs/: user docs for utilities (ConfigResolver, LanceDB, Codex CLI, etc.).
- .cursor/rules/: authoritative project standards for backend/frontend workflows (use when touching template code).
- Makefile, docker-compose.yml, first-time.sh: dev automation.
- pyproject.toml: package metadata and deps for gutil + included cli.

## Developer workflows (high-signal)

- Local library work

  - Install: pip install -e . (or pip install -r requirement.txt for minimal examples)
  - Quick probes:
    - Env read: from gutil.ConfigResolver import ConfigResolver as C; C().load_config('env','FOO')
    - YAML read: C().load_config('config','section/key') with repo-root config.yaml

- Template dev (optional)
  - make dev (docker-compose up --build) to start backend and CLI containers
  - Backend health: http://localhost:8000/api/v1/health/health
  - Logs: docker-compose logs -f backend | cli

## Project conventions

- Minimalism: keep public APIs stable; avoid new top‑level deps without clear need. If added, document in README.md and pyproject.
- Errors as signals: raise precise exceptions; avoid print in library code. CLI handles I/O.
- Types: add type hints on changed/new functions.
- Paths/config: default to repo‑root `.env` and `config.yaml` unless new opt‑in args are provided.

## Critical module contracts

- ConfigResolver (gutil/ConfigResolver.py)

  - API must remain: class ConfigResolver; method load_config(source, variable_path)
  - source ∈ { 'config', 'env' }
  - 'config' uses slash path (e.g., section/key/subkey); 'env' uses raw env var
  - Input validation → ValueError; do not print; update docs/ConfigResolver.md if behavior changes

- CodexBridge (gutil/CodexBridge.py)

  - Thin wrapper to invoke external Codex CLI binary from $GUTIL_CODEX_BIN or 'codex'
  - Don’t vendor Codex; capture returncode/stdout/stderr; raise CodexCLIError on resolution issues

- LanceDB (gutil/LanceDB.py)

  - \_ensure_lancedb() guards optional dependency; raise LanceDBNotInstalled with actionable hint
  - Keep list/create/query minimal; avoid side effects; CLI layer parses/prints

- gutil CLI (gutil/**main**.py)

  - Subcommands: create project, codex passthrough, lancedb (list/create/query), toolbox run/install
  - Preserve flags/behavior; separate user I/O from library logic

- CLI App client (cli/app/services/api_client.py)
  - HTTP to backend with simple config state; endpoints under /api/v1; handle auth token persistence

## Backend patterns (template)

- FastAPI app with CORSMiddleware; Pydantic BaseSettings in backend/app/core/config.py (env via .env)
- Services: SupabaseAuthService, SupabaseDatabaseService, EmbeddingService, CodexService (LLM)
- Follow .cursor/rules/backend/\* standards if modifying backend scaffold

## Integration points and external deps

- pyproject.toml deps (library scope): pyyaml, python-dotenv, lancedb, fastembed, rich, requests
- Backend/container deps are isolated to backend/ and docker-compose; avoid coupling into gutil core

## When changing behavior

- Update docs under docs/ relevant module (and README.md summary). Keep examples runnable with listed deps.
- If you touch template standards, also review .cursor/rules/\* for alignment.
- Maintain backward compatibility; if a breaking change is unavoidable, document clear upgrade notes.

## Validation: green-before-done

- Build/import smoke: python -c "import gutil, cli" (after pip install -e .)
- Probes for changed modules (see “Local library work” above)
- Optional: docker-compose up for backend health if touching cli/backend integration

## Security and data handling

- Treat config input as untrusted; never log secrets from .env/config
- Avoid executing config content; validate expected types/keys

## Adding new utilities

- Place under gutil/ with a focused purpose; add docs/<Module>.md + minimal usage example
- Avoid cross-coupling; compose via imports only where necessary

## Quick references

- Docs: docs/\*.md (ConfigResolver.md, LanceDB.md, CodexCLI.md)
- Entry: python -m gutil … or bin/gutil
- Dev automation: Makefile targets (dev/up/down/logs); first-time.sh for initial bootstrap

When unsure: prefer the smallest, explicit change; keep APIs stable; update docs alongside code.
