import os
import platform
import shutil
import stat
import subprocess
import sys
from typing import Iterable, List, Optional, Tuple


class ToolboxError(RuntimeError):
    pass


class ToolboxCLI:
    """Wrapper for the MCP Toolbox (genai-toolbox) binary.

    - Resolves from env `GUTIL_TOOLBOX_BIN` or PATH as `toolbox`.
    - Can download a platform-appropriate release binary.
    """

    def __init__(self, binary: Optional[str] = None) -> None:
        self.binary = binary or os.environ.get("GUTIL_TOOLBOX_BIN", "toolbox")

    def resolve(self) -> str:
        path = shutil.which(self.binary)
        if not path:
            raise ToolboxError(
                f"Toolbox binary not found: {self.binary}. Set GUTIL_TOOLBOX_BIN or install 'toolbox'."
            )
        return path

    def run(self, args: Iterable[str]) -> Tuple[int, str, str]:
        path = self.resolve()
        cmd: List[str] = [path, *list(args)]
        try:
            proc = subprocess.run(
                cmd,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        except FileNotFoundError as e:
            raise ToolboxError("Failed to execute toolbox binary") from e
        return proc.returncode, proc.stdout, proc.stderr

    @staticmethod
    def _detect_platform() -> Tuple[str, str]:
        sysname = platform.system().lower()
        machine = platform.machine().lower()

        if sysname == "linux":
            os_part = "linux"
            if machine in ("x86_64", "amd64"):
                arch = "amd64"
            elif machine in ("aarch64", "arm64"):
                arch = "arm64"
            else:
                raise ToolboxError(f"Unsupported Linux architecture: {machine}")
        elif sysname == "darwin":
            os_part = "darwin"
            if machine in ("arm64", "aarch64"):
                arch = "arm64"
            elif machine in ("x86_64", "amd64"):
                arch = "amd64"
            else:
                raise ToolboxError(f"Unsupported macOS architecture: {machine}")
        elif sysname == "windows":
            os_part = "windows"
            if machine in ("x86_64", "amd64"):
                arch = "amd64"
            else:
                raise ToolboxError(f"Unsupported Windows architecture: {machine}")
        else:
            raise ToolboxError(f"Unsupported OS: {sysname}")

        return os_part, arch

    @staticmethod
    def _build_download_url(version: str) -> Tuple[str, bool]:
        os_part, arch = ToolboxCLI._detect_platform()
        base = f"https://storage.googleapis.com/genai-toolbox/v{version}/{os_part}/{arch}/toolbox"
        is_windows = os_part == "windows"
        if is_windows:
            base += ".exe"
        return base, is_windows

    def install(self, version: str, dest: str) -> str:
        """Download a Toolbox release binary to `dest` and make it executable.

        Returns the absolute path to the installed binary.
        """
        import urllib.request  # lazy import

        url, is_windows = self._build_download_url(version)
        abspath = os.path.abspath(dest)
        os.makedirs(os.path.dirname(abspath), exist_ok=True)

        try:
            with urllib.request.urlopen(url) as resp, open(abspath, "wb") as out:
                out.write(resp.read())
        except Exception as e:  # noqa: BLE001
            raise ToolboxError(f"Failed to download toolbox from {url}: {e}") from e

        if not is_windows:
            # set +x
            st = os.stat(abspath)
            os.chmod(abspath, st.st_mode | stat.S_IEXEC)

        return abspath

