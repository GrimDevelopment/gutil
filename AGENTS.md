# gutil — Agent Guide (AGENTS.md)

This file guides coding agents contributing to the gutil project by GrimDevelopment (MrGrim). It defines scope, code conventions, structure, and expectations for changes. Its scope applies to the entire repository.

## Project Overview

- Name: gutil (personal CLI/utilities by GrimDevelopment / MrGrim)
- Language: Python 3.8+
- Purpose: Small utilities for configuration and environment handling. Current primary module: `ConfigResolver`.
- Dependencies: `pyyaml`, `python-dotenv` (pinned in `requirement.txt`).

## Repo Map

- `gutil/ConfigResolver.py`: `ConfigResolver` class for loading values from `config.yaml` and `.env`.
- `gutil/__init__.py`: Package marker (keep imports lightweight).
- `docs/ConfigResolver.md`: User-facing docs and examples for `ConfigResolver`.
- `README.md`: Project overview (may still reference GDUtilities; prefer the name “gutil” going forward).
- `requirement.txt`: Runtime deps for examples/docs. Do not rename without updating docs.

## General Rules

- Keep changes minimal, focused, and Pythonic. Prefer clarity over cleverness.
- Maintain backward compatibility for public interfaces (imports and class/method names).
- Do not introduce new top-level dependencies without a clear need and documentation.
- Update docs for any behavioral change or new feature (see Documentation section).
- Prefer exceptions over silent failures. Return values should be simple and explicit.
- If adding CLI entry points later, separate CLI I/O from library logic.

## Code Conventions

- Style: Follow standard Python style (PEP 8). Use descriptive names (no one-letter vars).
- Errors: Raise precise exceptions. Compose clear error messages; avoid swallowing stack traces.
- Logging/Output: Library code should avoid noisy `print`. If you must report, use Python `logging` with reasonable defaults. Preserve existing behavior in `ConfigResolver`.
- Types: Add type hints for new or modified functions when practical.
- Imports: Standard → third-party → local, with blank lines between groups.
- I/O paths: Treat `config.yaml` and `.env` as repository-root defaults unless a path parameter is explicitly added.

## Module-Specific Guidance

### ConfigResolver (`gutil/ConfigResolver.py`)

- Keep the current API stable:
  - Class: `ConfigResolver`
  - Method: `load_config(source, variable_path)`
- Supported `source` values remain `'config'` and `'env'`.
- For `'config'`, keys are a slash-delimited path (e.g., `section/key/subkey`).
- For `'env'`, `variable_path` is the raw env var name.
- If you add features (e.g., custom file paths, different loaders, defaults):
  - Add parameters in a backward-compatible way (keyword-only with sensible defaults).
  - Validate inputs and raise `ValueError` for invalid combinations.
  - Update examples in `docs/ConfigResolver.md` and mention changes in `README.md`.

## Documentation

- Update `docs/` with concrete examples for any new capability.
- Keep `README.md` concise; link to detailed docs in `docs/`.
- Code examples should be runnable with only the listed dependencies and sample files.
- If you rename or add files expected by the library (e.g., `config.yaml`), reflect that in docs.
- When adding or removing features or important behavior, update both `docs/` and `README.md` in the same change so they stay in sync.

### MCP Docs Sync

- When docs are updated (either `docs/` or `README.md`), also update the `docs-mcp-server` so its resources reflect the latest content.
- Typical actions: sync or mirror changed markdown, regenerate indexes/manifests, and run the server’s publish/release workflow.
- If `docs-mcp-server` lives in a separate repo, open a companion PR referencing the change here and link them together.

## Testing & Validation

- There is no formal test suite. When changing behavior, add a minimal, self-contained example to `docs/` and verify locally with Python 3.8+.
- Prefer writing small probes (e.g., `python -c "..."`) to validate changes.
- Do not add test frameworks unless requested; keep validation lightweight.

## Dependency Management

- Runtime dependencies are listed in `requirement.txt`.
- Keep versions flexible unless pinning is required for correctness.
- If you add a dependency, explain why in the PR/commit description and update installation instructions in `README.md`.

## Adding New Utilities

- Place new modules under `gutil/` with clear names (e.g., `PathTools.py`).
- Provide a dedicated `docs/<ModuleName>.md` describing purpose, API, and examples.
- Keep modules single-responsibility and small. Avoid cross-coupling between utilities; compose via imports when needed.

## Backward Compatibility

- Do not rename files or classes that form part of the import path without adding shims in `gutil/__init__.py` and clearly documenting the deprecation path.
- Treat printed output as part of observable behavior; changes should be deliberate and documented.

## Security & Safety

- Treat configuration files as untrusted input. Validate types and presence of keys before use.
- Avoid executing or evaluating configuration content.
- Do not log secrets from `.env` or configuration files.

## Release & Versioning

- No explicit versioning policy yet. If introducing breaking changes, surface them clearly in `README.md` and docs with upgrade notes.

## Quick Local Checks

- Install deps: `pip install -r requirement.txt`
- Probe env read:
  - `python -c "from gutil.ConfigResolver import ConfigResolver as C; print(C().load_config('env','EXAMPLE') if True else '')"`
- Probe config read (requires `config.yaml`):
  - `python -c "from gutil.ConfigResolver import ConfigResolver as C; print(C().load_config('config','section/key'))"`

## When In Doubt

- Prefer minimal surface area and explicit behavior.
- Update documentation alongside code changes.
- Ask before introducing new patterns or dependencies.
