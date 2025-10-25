import os
import shutil
import subprocess
import tempfile
from typing import Iterable, Optional


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

        # Determine source directory: either an existing path or a temp clone
        cleanup_dir: Optional[str] = None
        if os.path.isdir(template_url):
            source_dir = os.path.abspath(template_url)
        else:
            tmpdir = tempfile.mkdtemp(prefix="gutil-template-")
            cleanup_dir = tmpdir
            try:
                cmd = ["git", "clone", template_url, tmpdir]
                if branch:
                    cmd = [
                        "git",
                        "clone",
                        "--branch",
                        branch,
                        "--single-branch",
                        template_url,
                        tmpdir,
                    ]

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
            except Exception:
                # Ensure we clean up on failure before re-raising
                if cleanup_dir:
                    try:
                        shutil.rmtree(cleanup_dir)
                    except Exception:
                        pass
                raise
            source_dir = tmpdir

        try:
            rsync_cmd = ["rsync", "-a", "--exclude=.git"]
            if exclude:
                # Apply exclude patterns for rsync as --exclude=pattern
                rsync_cmd.extend(f"--exclude={pattern}" for pattern in exclude)
            if not overwrite:
                rsync_cmd.append("--ignore-existing")

            # Ensure trailing slash to copy contents rather than directory itself
            source_with_slash = source_dir if source_dir.endswith(os.sep) else f"{source_dir}{os.sep}"
            rsync_cmd.extend([source_with_slash, dest_dir])

            try:
                rsync_result = subprocess.run(
                    rsync_cmd,
                    check=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
            except FileNotFoundError as e:
                raise RuntimeError("rsync is not installed or not found in PATH") from e

            if rsync_result.returncode != 0:
                raise RuntimeError(
                    "Failed to merge template files with rsync "
                    f"(exit {rsync_result.returncode}).\n"
                    f"Command: {' '.join(rsync_cmd)}\n"
                    f"stderr: {rsync_result.stderr.strip()}"
                )

            return dest_dir
        finally:
            if cleanup_dir:
                try:
                    shutil.rmtree(cleanup_dir)
                except Exception:
                    # Best-effort; avoid masking earlier exceptions
                    pass
