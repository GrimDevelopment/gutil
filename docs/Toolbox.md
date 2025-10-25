# MCP Toolbox Integration (genai-toolbox)

gutil provides a lightweight wrapper for the MCP Toolbox (genai-toolbox) binary.

## Install the binary

```sh
python -m gutil toolbox install --version 0.18.0 --dest bin/toolbox
```

The installer detects your OS and CPU and downloads the matching binary from the
official release bucket. On UNIX-like systems, it marks the file as executable.

You can also install Toolbox with Homebrew or manually from the releases, then
ensure the `toolbox` binary is on PATH or set `GUTIL_TOOLBOX_BIN` to its path.

## Run the server

```sh
python -m gutil toolbox run --tools-file tools.yaml
```

This starts the Toolbox server with your `tools.yaml`. Use `--disable-reload`
to turn off dynamic reloading.

## Check availability

```sh
python -m gutil toolbox check
```

Prints the resolved binary path and attempts to run `toolbox version`.

## Notes

- gutil does not bundle Toolbox; it provides a convenience installer and runner.
- See upstream docs for full usage: https://github.com/googleapis/genai-toolbox

