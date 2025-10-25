import os
import shutil
import subprocess
from typing import Iterable, List, Optional, Tuple


class CodexCLIError(RuntimeError):
    pass


class CodexCLI:
    """Thin wrapper to invoke the Codex CLI binary.

    Resolves the binary from `GUTIL_CODEX_BIN` or defaults to `codex`.
    """

    def __init__(self, binary: Optional[str] = None) -> None:
        self.binary = binary or os.environ.get("GUTIL_CODEX_BIN", "codex")

    def _resolve(self) -> str:
        path = shutil.which(self.binary)
        if not path:
            raise CodexCLIError(
                f"Codex CLI binary not found: {self.binary}. Set GUTIL_CODEX_BIN or install 'codex'."
            )
        return path

    def run(self, args: Iterable[str]) -> Tuple[int, str, str]:
        bin_path = self._resolve()
        cmd: List[str] = [bin_path, *list(args)]
        try:
            proc = subprocess.run(
                cmd,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        except FileNotFoundError as e:
            raise CodexCLIError("Failed to execute Codex CLI binary") from e

        return proc.returncode, proc.stdout, proc.stderr

