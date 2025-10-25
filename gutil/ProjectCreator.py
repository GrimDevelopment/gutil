import os
import shutil
import subprocess
import tempfile
from typing import Iterable, Optional, Set


class ProjectCreator:
    """Library for creating new projects from a template repo.

    Keeps I/O minimal; raises exceptions on error.
    """

    DEFAULT_TEMPLATE = "git@github.com:0x7C2f/vibe-coding-template.git"

    def create_project(
        self,
        name: str,
        template_url: str = DEFAULT_TEMPLATE,
        branch: Optional[str] = None,
    ) -> str:
        """Clone a template repository into a new directory named `name`.

        Returns the absolute path to the created project directory.

        Raises ValueError for invalid inputs and RuntimeError for clone failures.
        """
        if not name or not name.strip():
            raise ValueError("Project name must be a non-empty string")

        # Basic guardrails: avoid path traversal; keep it to a single folder name
        if any(sep in name for sep in (os.sep, os.altsep) if sep):
            raise ValueError("Project name must not contain path separators")

        target_dir = os.path.abspath(name)

        if os.path.exists(target_dir):
            raise ValueError(f"Target directory already exists: {target_dir}")

        # Build git clone command
        cmd = ["git", "clone", template_url, name]
        if branch:
            cmd = ["git", "clone", "--branch", branch, "--single-branch", template_url, name]

        try:
            result = subprocess.run(
                cmd,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        except FileNotFoundError as e:
            raise RuntimeError(
                "git is not installed or not found in PATH"
            ) from e

        if result.returncode != 0:
            raise RuntimeError(
                f"Failed to clone template repo (exit {result.returncode}).\n"
                f"Command: {' '.join(cmd)}\n"
                f"stderr: {result.stderr.strip()}"
            )

        # Return absolute path to the new project directory
        return target_dir

    def integrate_template(
        self,
        template_url: str = DEFAULT_TEMPLATE,
        branch: Optional[str] = None,
        destination: str = ".",
        overwrite: bool = False,
        exclude: Optional[Iterable[str]] = None,
    ) -> str:
        """Clone a template repo and merge its files into `destination`.

        - Skips VCS metadata (e.g., .git) and any names in `exclude`.
        - By default, refuses to overwrite existing files unless `overwrite=True`.

        Returns the absolute path to the destination directory.
        """
        dest_dir = os.path.abspath(destination)
        if not os.path.isdir(dest_dir):
            raise ValueError(f"Destination must be an existing directory: {dest_dir}")

        # Clone to a temp directory
        tmpdir = tempfile.mkdtemp(prefix="gutil-template-")
        try:
            cmd = ["git", "clone", template_url, tmpdir]
            if branch:
                cmd = ["git", "clone", "--branch", branch, "--single-branch", template_url, tmpdir]

            try:
                result = subprocess.run(
                    cmd,
                    check=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
            except FileNotFoundError as e:
                raise RuntimeError("git is not installed or not found in PATH") from e

            if result.returncode != 0:
                raise RuntimeError(
                    f"Failed to clone template repo (exit {result.returncode}).\n"
                    f"Command: {' '.join(cmd)}\n"
                    f"stderr: {result.stderr.strip()}"
                )

            # Build exclusion set
            skip: Set[str] = {".git", "..", "."}
            if exclude:
                skip.update(exclude)

            # First pass: detect conflicts
            conflicts = []
            for root, dirs, files in os.walk(tmpdir):
                # relative path from tmpdir
                rel_root = os.path.relpath(root, tmpdir)
                if rel_root == ".":
                    rel_root = ""
                # Filter directories in-place
                dirs[:] = [d for d in dirs if d not in skip]
                for fname in files:
                    if fname in skip:
                        continue
                    rel_path = os.path.normpath(os.path.join(rel_root, fname))
                    target_path = os.path.join(dest_dir, rel_path)
                    if os.path.exists(target_path) and not overwrite:
                        conflicts.append(rel_path)
            if conflicts and not overwrite:
                sample = "\n".join(conflicts[:10])
                more = "" if len(conflicts) <= 10 else f"\n... and {len(conflicts)-10} more"
                raise RuntimeError(
                    "Conflicts detected; use overwrite=True to replace existing files:\n"
                    f"{sample}{more}"
                )

            # Second pass: copy files
            for root, dirs, files in os.walk(tmpdir):
                rel_root = os.path.relpath(root, tmpdir)
                if rel_root == ".":
                    rel_root = ""
                dirs[:] = [d for d in dirs if d not in skip]
                for d in dirs:
                    os.makedirs(os.path.join(dest_dir, rel_root, d), exist_ok=True)
                for fname in files:
                    if fname in skip:
                        continue
                    src = os.path.join(root, fname)
                    rel_path = os.path.normpath(os.path.join(rel_root, fname))
                    dst = os.path.join(dest_dir, rel_path)
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.copy2(src, dst)

            return dest_dir
        finally:
            # Clean up the temporary clone
            try:
                shutil.rmtree(tmpdir)
            except Exception:
                # Best-effort; avoid masking earlier exceptions
                pass
