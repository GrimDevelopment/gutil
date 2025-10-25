# gutil

gutil is a small set of Python utilities by GrimDevelopment (MrGrim). It focuses on configuration and environment handling for simple scripts and services. The current primary module is `ConfigResolver`, which loads values from YAML (`config.yaml`) and environment files (`.env`).

## Features

- Load nested configuration values from a YAML file.
- Access environment variables from a `.env` file.
- Simple, explicit errors for missing keys and invalid inputs.

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

## Quick Start

1) Create a `.env` file:

```sh
DATABASE_URL=mysql://user:password@localhost/dbname
```

2) Create a `config.yaml` file:

```yaml
database:
  url: mysql://user:password@localhost/dbname
```

3) Read values with `ConfigResolver`:

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

## Documentation

- ConfigResolver usage and examples: `docs/ConfigResolver.md`

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

