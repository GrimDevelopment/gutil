# Codex CLI Integration

gutil can delegate commands to the Codex CLI, allowing you to use Codex features from the same entrypoint.

## Prerequisites

- Codex CLI installed and available on PATH as `codex`, or set `GUTIL_CODEX_BIN` to its location

## Usage

Pass any Codex command after `--`:

```sh
python -m gutil codex -- --help
python -m gutil codex -- plan open
```

Using the repo shim:

```sh
./bin/gutil codex -- --help
```

## Behavior

- gutil resolves the Codex CLI binary from `$GUTIL_CODEX_BIN` first, then falls back to `codex` on PATH.
- Stdout/stderr and the exit code from Codex are passed through.
- On failure to locate the binary, gutil prints a clear error message and exits with code 2.

