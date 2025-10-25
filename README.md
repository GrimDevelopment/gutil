# gutil

gutil is a small set of Python utilities by GrimDevelopment (MrGrim). It focuses on configuration and environment handling for simple scripts and services. The current primary module is `ConfigResolver`, which loads values from YAML (`config.yaml`) and environment files (`.env`).

## Features

- Load nested configuration values from a YAML file.
- Access environment variables from a `.env` file.
- Simple, explicit errors for missing keys and invalid inputs.
- Create a new project from a template via a small CLI.
- LanceDB integration for simple local data workflows (list/create/query).

## Installation

Requirements: Python 3.8+

Option A — install dependencies listed by the project:

```sh
pip install -r requirement.txt
```

Option B — install only what the examples need:

```sh
pip install pyyaml python-dotenv
```

Option C — install as a package (recommended for template-based projects):

```sh
# Install editable for development
pip install -e .

# Or build a wheel and install
python -m pip install hatchling && hatch build
pip install dist/gutil-*.whl
```

## Quick Start

1. Create a `.env` file:

```sh
DATABASE_URL=mysql://user:password@localhost/dbname
```

2. Create a `config.yaml` file:

```yaml
database:
  url: mysql://user:password@localhost/dbname
```

3. Read values with `ConfigResolver`:

```python
from gutil.ConfigResolver import ConfigResolver

resolver = ConfigResolver()

# From environment
database_url_env = resolver.load_config('env', 'DATABASE_URL')
print('Env:', database_url_env)

# From YAML config
database_url_cfg = resolver.load_config('config', 'database/url')
print('Config:', database_url_cfg)
```

More examples are available in `docs/ConfigResolver.md`.

## CLI

gutil includes a small CLI with several capabilities:

1. Create a new project by cloning a template repo
2. Delegate to the Codex CLI for advanced workflows
3. Integrate with MCP Toolbox (genai-toolbox) to run a database tools server
4. Run a local Codex-style REPL with LanceDB-backed memory
5. Integrate a template repository into the current project
6. App commands to talk to the backend (auth, generate, config)

- Default template: `git@github.com:0x7C2f/vibe-coding-template.git`

Usage:

```sh
# Using module entrypoint
python -m gutil create project my-new-app

# Optional: pick a specific branch or override the template URL
python -m gutil create project my-new-app --branch main
python -m gutil create project my-new-app --template https://github.com/0x7C2f/vibe-coding-template.git
```

Notes:

- Requires `git` to be installed and available on PATH.
- SSH URL assumes your SSH keys are configured for GitHub. Use `--template` with HTTPS if preferred.

## Documentation

- ConfigResolver usage and examples: `docs/ConfigResolver.md`
- Project creation CLI details: `docs/ProjectCreator.md`
- Codex integration details: `docs/CodexCLI.md`
- LanceDB integration: `docs/LanceDB.md`
- Codex REPL (self-improving assistant): `docs/CodexRepl.md`

### Codex CLI integration

You can forward any command to the Codex CLI via `gutil codex`:

```sh
# Show codex help
python -m gutil codex -- --help

# Run a codex command in the current repo
python -m gutil codex -- plan open

# Using the repo shim
./bin/gutil codex -- --help
```

Notes:

- The binary is resolved from `$GUTIL_CODEX_BIN` or defaults to `codex` on PATH.
- Outputs and exit code are passed through.

### LanceDB integration

LanceDB commands are available via `gutil lancedb`:

```sh
# List tables in a LanceDB directory or URI
python -m gutil lancedb list ./data/mydb

# Create a table from a JSON file (object or array)
python -m gutil lancedb create ./data/mydb events ./seed/events.json

# Query rows (prints JSON lines)
python -m gutil lancedb query ./data/mydb events --limit 5
```

To use LanceDB, install the optional dependency:

```sh
pip install lancedb
```

You can also add it from `requirement.txt` if you prefer a single install step.

### MCP Toolbox (genai-toolbox) integration

gutil can help you manage and run the Toolbox server:

```sh
# Install a toolbox binary for your platform (e.g., v0.18.0) into bin/toolbox
python -m gutil toolbox install --version 0.18.0 --dest bin/toolbox

# Verify availability and print version
python -m gutil toolbox check

# Run the server with your tools.yaml
python -m gutil toolbox run --tools-file tools.yaml
```

Notes:

- Binary resolution uses `$GUTIL_TOOLBOX_BIN` or `toolbox` on PATH.
- The installer downloads from the official release bucket based on your OS/arch.
- For full docs, see the upstream project: https://github.com/googleapis/genai-toolbox

### Codex REPL with memory

Run a minimal terminal REPL that routes prompts to Codex (via the `codex` binary) while retrieving similar past interactions from LanceDB and storing new results for future recall.

```sh
# Default config at gutil/codex_cli/config.yaml
python -m gutil codex-repl

# Or point to a custom config
python -m gutil codex-repl --config /path/to/config.yaml
```

Notes:

- Requires the Codex CLI (`codex`) on PATH; you can also use the integrated `gutil codex -- ...` for direct pass-through.
- By default, the REPL tells Codex to use local OSS models (`--oss`) so you can stay fully local if you have a provider like Ollama running.
- Stores vector memory in LanceDB under `./data/codex_memory` (configurable), and optionally a lightweight SQLite history.
- Embeddings: defaults to local `fastembed` (BAAI/bge-small-en-v1.5). You can switch to OpenAI embeddings in `config.yaml`.

### Using with vibe-coding-template

This repo includes packaging (`pyproject.toml`) and a console entrypoint `gutil`. In a project created from the `vibe-coding-template`, you can install and use `gutil` directly:

```sh
pip install -e .
gutil --help
gutil codex-repl
```

If you prefer not to install, you can still use the shim:

```sh
./bin/gutil --help
```

### Template integration

Integrate the vibe-coding-template (or any repo) into your current project, then remove the temporary clone. By default, merging is performed via `rsync -a --exclude='.git' --ignore-existing` so existing files are left untouched; `--overwrite` drops the `--ignore-existing` flag. You can exclude additional paths with `--exclude`.

```sh
# Integrate the default vibe-coding-template into the current directory
python -m gutil template integrate

# Specify a branch and overwrite conflicting files
python -m gutil template integrate --branch main --overwrite

# Use a different template and exclude extra paths
python -m gutil template integrate \
  --template https://github.com/0x7C2f/vibe-coding-template.git \
  --exclude .github LICENSE
```

### App (backend) commands

Use gutil to interact with the backend instead of the separate cli/ app.

```sh
# Configure API URL (stored in ~/.gutil/app.json)
python -m gutil app config set api_url http://localhost:8000
python -m gutil app config show

# Login (stores access_token in ~/.gutil/app.json)
python -m gutil app auth login --email you@example.com --password 'secret'

# Generate via backend Codex endpoint
python -m gutil app generate --prompt "Write a Python function" --max-tokens 150

# Logout (clears token)
python -m gutil app auth logout
```

### Environment bootstrap

Create a local `.env` from `.env.example`:

```sh
python -m gutil env bootstrap
# Overwrite if it already exists
python -m gutil env bootstrap --force
```

### Docker and Make targets

Use Docker Compose to run the backend (and optional CLI container). The backend has a healthcheck and the CLI service waits until it’s healthy.

### CLI project structure (applied template)

The CLI has been organized to mirror the vibe-coding-template layout, adapted for CLI programs:

```
cli/
├── Makefile
├── Dockerfile
├── Dockerfile.dev
├── requirements.txt
├── main.py                     # legacy entry (kept); prefer `gutil` entrypoint
├── commands/                   # high-level CLI commands (legacy)
├── services/                   # legacy client helpers
├── codex_cli/                  # Codex REPL + memory
│   ├── cli.py
│   ├── config.yaml
│   ├── embeddings.py
│   ├── lancedb_store.py
│   └── utils/
│       ├── context_manager.py
│       └── logger.py
└── app/
    ├── core/
    │   └── config.py           # CLI settings
    ├── models/
    │   ├── auth.py
    │   ├── llm.py
    │   └── vectordb.py
    └── services/
        ├── llm/
        │   ├── embedding_service.py
        │   └── llm_service.py
        ├── supabase/
        │   ├── auth.py
        │   ├── database.py
        │   └── storage.py
        └── vectordb/
            ├── __init__.py
            └── qdrant_service.py
```

We can flesh out these modules as functionality grows. For now, they serve as placeholders to apply the template structure to the CLI domain.

```sh
# Bring up services and rebuild as needed
make up

# Tail logs or inspect processes
make logs
make ps

# Stop services
make down
```

## Development

- Code style: PEP 8; keep changes minimal and explicit.
- Python: 3.8+.
- Install deps: `pip install -r requirement.txt`.
- Project layout:
  - `gutil/ConfigResolver.py` — library code
  - `docs/ConfigResolver.md` — usage docs & examples

## Notes

- gutil is evolving; APIs may grow over time. Check the docs for the latest examples.
- Created by GrimDevelopment (MrGrim).

# Vibe Coding Template

## Overview

The Vibe Coding Template is a modern full-stack application template that integrates a Next.js frontend with a Python FastAPI backend. It utilizes Supabase for authentication, database management, and storage, and includes a command-line interface (CLI) tool that leverages Codex as the backend for generating content.

## Project Structure

```
vibe-coding-template
├── backend
│   ├── app
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api
│   │   │   ├── __init__.py
│   │   │   ├── v1
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py
│   │   │   │   └── endpoints
│   │   │   │       ├── __init__.py
│   │   │   │       ├── auth.py
│   │   │   │       ├── codex.py
│   │   │   │       └── health.py
│   │   ├── core
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   └── codex.py
│   │   └── services
│   │       ├── __init__.py
│   │       ├── supabase_auth.py
│   │       ├── supabase_database.py
│   │       ├── llm_service.py
│   │       └── embedding_service.py
│   ├── requirements.txt
│   └── Dockerfile
├── cli
│   ├── __init__.py
│   ├── main.py
│   ├── commands
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── generate.py
│   │   └── config.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── api_client.py
│   │   └── local_config.py
│   ├── utils
│   │   ├── __init__.py
│   │   ├── output.py
│   │   └── prompts.py
│   └── requirements.txt
├── supabase
│   └── migrations
│       └── 20240101000000_initial_schema.sql
├── .env.example
├── .gitignore
├── Makefile
├── docker-compose.yml
├── first-time.sh
└── README.md
```

## Features

- **Backend**: Built with Python FastAPI, providing a robust API for frontend interaction and CLI commands.
- **Frontend**: Developed using Next.js with Tailwind CSS and TypeScript for a responsive user interface.
- **Database**: Utilizes Supabase PostgreSQL for data storage and management.
- **CLI Tool**: A command-line interface for interacting with the application, including user authentication and content generation using Codex.
- **Vector Database**: Integrates Qdrant for semantic search capabilities.
- **LLM Integration**: Supports OpenAI and Anthropic for advanced text generation.

## Getting Started

1. **Clone the Repository**:

   ```
   git clone <repository-url>
   cd vibe-coding-template
   ```

2. **Setup Environment**:
   Copy the `.env.example` to `.env` and fill in the required environment variables.

3. **Install Dependencies**:
   For the backend:

   ```
   cd backend
   pip install -r requirements.txt
   ```

   For the CLI:

   ```
   cd cli
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   Start the backend server:

   ```
   cd backend
   uvicorn app.main:app --reload
   ```

   Start the CLI tool:

   ```
   cd cli
   python main.py
   ```

5. **Database Migrations**:
   Run migrations using Supabase CLI or your preferred method.

## Usage

### CLI Commands

- **Authenticate**: Use the CLI to authenticate users.
- **Generate Content**: Utilize the Codex backend to generate content based on prompts.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
