import argparse
import sys

from .ProjectCreator import ProjectCreator
from .CodexBridge import CodexCLI, CodexCLIError
from .LanceDB import LanceDBClient, LanceDBNotInstalled
from .ToolboxBridge import ToolboxCLI, ToolboxError
from cli.app.services.api_client import AppClient, AppSettings
from cli.app.core.state import load_app_config, save_app_config


def _add_create_subparser(subparsers: argparse._SubParsersAction) -> None:
    create_parser = subparsers.add_parser(
        "create", help="Create resources (e.g., projects)"
    )

    create_sub = create_parser.add_subparsers(dest="create_target", required=True)

    # gutil create project <name> [--branch <branch>] [--template <url>]
    proj = create_sub.add_parser("project", help="Create a new project from a template repo")
    proj.add_argument("name", help="Project name (target directory)")
    proj.add_argument(
        "--branch",
        dest="branch",
        help="Template branch to use (defaults to template's default)",
    )
    proj.add_argument(
        "--template",
        dest="template",
        help="Template git URL to clone from (defaults to built-in)",
    )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="gutil", description="gutil CLI utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)

    _add_create_subparser(subparsers)

    # gutil codex -- <any codex args>
    codex_parser = subparsers.add_parser(
        "codex", help="Forward commands to the Codex CLI"
    )
    codex_parser.add_argument(
        "codex_args",
        nargs=argparse.REMAINDER,
        help="Arguments to pass through to the 'codex' binary",
    )

    # gutil lancedb ...
    ldb = subparsers.add_parser("lancedb", help="LanceDB utilities")
    ldb_sub = ldb.add_subparsers(dest="lancedb_cmd", required=True)

    # list tables
    l_list = ldb_sub.add_parser("list", help="List tables in a LanceDB at <uri>")
    l_list.add_argument("uri", help="LanceDB URI/path")

    # create from JSON file
    l_create = ldb_sub.add_parser(
        "create", help="Create table from a JSON file (object or array of objects)"
    )
    l_create.add_argument("uri", help="LanceDB URI/path")
    l_create.add_argument("table", help="Table name")
    l_create.add_argument("json_file", help="Path to JSON file")
    l_create.add_argument(
        "--exist-ok",
        action="store_true",
        help="Do not error if table already exists",
    )

    # query
    l_query = ldb_sub.add_parser("query", help="Query table and print rows as JSON")
    l_query.add_argument("uri", help="LanceDB URI/path")
    l_query.add_argument("table", help="Table name")
    l_query.add_argument("--limit", type=int, default=10, help="Max rows to return")

    # gutil toolbox ...
    tb = subparsers.add_parser("toolbox", help="MCP Toolbox (genai-toolbox) integration")
    tb_sub = tb.add_subparsers(dest="toolbox_cmd", required=True)

    # run server
    tb_run = tb_sub.add_parser("run", help="Run toolbox server with a tools.yaml file")
    tb_run.add_argument("--tools-file", required=True, help="Path to tools.yaml")
    tb_run.add_argument(
        "--disable-reload",
        action="store_true",
        help="Disable dynamic reload of tools file",
    )
    tb_run.add_argument(
        "--port",
        type=int,
        help="Port to bind (forwarded to toolbox if supported)",
    )

    # install binary
    tb_inst = tb_sub.add_parser("install", help="Download toolbox binary for this platform")
    tb_inst.add_argument(
        "--version",
        required=True,
        help="Version to install (e.g., 0.18.0)",
    )
    tb_inst.add_argument(
        "--dest",
        default="bin/toolbox",
        help="Destination path for the binary (default: bin/toolbox)",
    )

    # check binary
    tb_chk = tb_sub.add_parser("check", help="Check toolbox availability and print version")

    # gutil codex-repl [--config <path>]
    repl = subparsers.add_parser("codex-repl", help="Run the Codex REPL with LanceDB memory")
    repl.add_argument(
        "--config",
        default="cli/codex_cli/config.yaml",
        help="Path to codex_cli config.yaml (defaults to cli/codex_cli/config.yaml)",
    )

    # gutil env bootstrap [--force] [--src .env.example] [--dst .env]
    envp = subparsers.add_parser("env", help="Environment helpers (.env bootstrap)")
    env_sub = envp.add_subparsers(dest="env_cmd", required=True)
    env_boot = env_sub.add_parser("bootstrap", help="Create .env from example if missing")
    env_boot.add_argument("--src", default=".env.example", help="Source example file")
    env_boot.add_argument("--dst", default=".env", help="Destination .env path")
    env_boot.add_argument("--force", action="store_true", help="Overwrite if destination exists")

    # gutil template integrate [--template <url>] [--branch <name>] [--dest <dir>] [--overwrite] [--exclude NAME ...]
    tpl = subparsers.add_parser("template", help="Template utilities")
    tpl_sub = tpl.add_subparsers(dest="template_cmd", required=True)
    t_int = tpl_sub.add_parser(
        "integrate",
        help="Integrate a template repo into the current project and remove the temporary clone",
    )
    t_int.add_argument(
        "--template",
        dest="template",
        help="Template git URL to clone from (defaults to built-in)",
    )
    t_int.add_argument("--branch", dest="branch", help="Template branch to use")
    t_int.add_argument(
        "--dest",
        default=".",
        help="Destination directory to merge into (default: current directory)",
    )
    t_int.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing files if conflicts are found",
    )
    t_int.add_argument(
        "--exclude",
        nargs="*",
        default=None,
        help="Additional top-level names to exclude (e.g., .github LICENSE)",
    )

    # gutil app ...
    app = subparsers.add_parser("app", help="App commands (backend integration)")
    app_sub = app.add_subparsers(dest="app_cmd", required=True)

    # app auth ...
    app_auth = app_sub.add_parser("auth", help="Authentication")
    app_auth_sub = app_auth.add_subparsers(dest="auth_cmd", required=True)

    auth_login = app_auth_sub.add_parser("login", help="Login and store token")
    auth_login.add_argument("--email", required=True)
    auth_login.add_argument("--password", required=True)

    auth_register = app_auth_sub.add_parser("register", help="Register a new user")
    auth_register.add_argument("--email", required=True)
    auth_register.add_argument("--password", required=True)

    auth_logout = app_auth_sub.add_parser("logout", help="Logout and clear token")

    # app generate
    app_gen = app_sub.add_parser("generate", help="Generate content via backend Codex endpoint")
    app_gen.add_argument("--prompt", required=True)
    app_gen.add_argument("--max-tokens", type=int, default=100)

    # app config
    app_cfg = app_sub.add_parser("config", help="Configure API URL and endpoints")
    app_cfg_sub = app_cfg.add_subparsers(dest="cfg_cmd", required=True)
    cfg_set = app_cfg_sub.add_parser("set", help="Set a config key")
    cfg_set.add_argument("key")
    cfg_set.add_argument("value")
    cfg_get = app_cfg_sub.add_parser("get", help="Get a config value")
    cfg_get.add_argument("key")
    cfg_show = app_cfg_sub.add_parser("show", help="Show current config")

    args = parser.parse_args(argv)

    if args.command == "create":
        if args.create_target == "project":
            creator = ProjectCreator()
            try:
                target = creator.create_project(
                    name=args.name,
                    template_url=args.template or ProjectCreator.DEFAULT_TEMPLATE,
                    branch=args.branch,
                )
                print(f"Project created at: {target}")
                return 0
            except Exception as e:
                print(f"Error: {e}")
                return 2
    elif args.command == "codex":
        # Pass-through to Codex CLI
        cli = CodexCLI()
        try:
            # argparse.REMAINDER may include a leading "--"; strip it if present
            remainder = list(args.codex_args or [])
            if remainder and remainder[0] == "--":
                remainder = remainder[1:]
            code, out, err = cli.run(remainder)
            # Mirror Codex output to our stdout/stderr
            if out:
                print(out, end="")
            if err:
                print(err, end="", file=sys.stderr)
            return code
        except CodexCLIError as e:
            print(f"Error: {e}")
            return 2
    elif args.command == "template":
        if args.template_cmd == "integrate":
            creator = ProjectCreator()
            try:
                dest = creator.integrate_template(
                    template_url=args.template or ProjectCreator.DEFAULT_TEMPLATE,
                    branch=args.branch,
                    destination=args.dest,
                    overwrite=bool(args.overwrite),
                    exclude=args.exclude,
                )
                print(f"Template integrated into: {dest}")
                return 0
            except Exception as e:
                print(f"Error: {e}")
                return 2
    elif args.command == "lancedb":
        try:
            if args.lancedb_cmd == "list":
                client = LanceDBClient(args.uri)
                for name in client.list_tables():
                    print(name)
                return 0
            if args.lancedb_cmd == "create":
                client = LanceDBClient(args.uri)
                rows = LanceDBClient.load_json_file(args.json_file)
                client.create_table(args.table, rows, exist_ok=args.exist_ok)
                print(f"Created table '{args.table}' at {args.uri}")
                return 0
            if args.lancedb_cmd == "query":
                client = LanceDBClient(args.uri)
                rows = client.query(args.table, limit=args.limit)
                # Print as compact JSON lines
                import json as _json  # local import to avoid top-level dependency

                for row in rows:
                    print(_json.dumps(row, ensure_ascii=False))
                return 0
        except LanceDBNotInstalled as e:
            print(f"Error: {e}")
            return 2
        except Exception as e:
            print(f"Error: {e}")
            return 2
    elif args.command == "toolbox":
        try:
            if args.toolbox_cmd == "run":
                cli = ToolboxCLI()
                # Build arg list
                run_args = ["--tools-file", args.tools_file]
                if args.disable_reload:
                    run_args.append("--disable-reload")
                if args.port:
                    # As of toolbox v0.18.0, port is controlled via env or config; if CLI flag exists, forward it.
                    run_args.extend(["--port", str(args.port)])
                code, out, err = cli.run(run_args)
                if out:
                    print(out, end="")
                if err:
                    print(err, end="", file=sys.stderr)
                return code
            if args.toolbox_cmd == "install":
                cli = ToolboxCLI()
                path = cli.install(args.version, args.dest)
                print(f"Installed toolbox v{args.version} to: {path}")
                return 0
            if args.toolbox_cmd == "check":
                cli = ToolboxCLI()
                path = cli.resolve()
                print(f"toolbox binary: {path}")
                code, out, err = cli.run(["version"])  # best-effort
                if out:
                    print(out, end="")
                if err:
                    print(err, end="", file=sys.stderr)
                return code
        except ToolboxError as e:
            print(f"Error: {e}")
            return 2
    elif args.command == "codex-repl":
        # Run the internal REPL
        try:
            from cli.codex_cli.cli import run_repl
        except Exception as e:  # noqa: BLE001
            print(f"Error importing codex_cli: {e}")
            return 2
        return run_repl(args.config)
    elif args.command == "app":
        client = AppClient()
        try:
            if args.app_cmd == "auth":
                if args.auth_cmd == "login":
                    out = client.login(args.email, args.password)
                    print(out)
                    return 0
                if args.auth_cmd == "register":
                    out = client.register(args.email, args.password)
                    print(out)
                    return 0
                if args.auth_cmd == "logout":
                    out = client.logout()
                    print(out)
                    return 0
            if args.app_cmd == "generate":
                out = client.generate(args.prompt, max_tokens=args.max_tokens)
                # Print minimal JSON
                import json as _json

                print(_json.dumps(out, ensure_ascii=False))
                return 0
            if args.app_cmd == "config":
                cfg = load_app_config()
                if args.cfg_cmd == "set":
                    cfg[args.key] = args.value
                    save_app_config(cfg)
                    print(f"Set {args.key}")
                    return 0
                if args.cfg_cmd == "get":
                    print(cfg.get(args.key, ""))
                    return 0
                if args.cfg_cmd == "show":
                    import json as _json

                    print(_json.dumps(cfg, indent=2))
                    return 0
        except Exception as e:
            print(f"Error: {e}")
            return 2
    elif args.command == "env":
        if args.env_cmd == "bootstrap":
            import os, shutil
            src = args.src
            dst = args.dst
            if not os.path.exists(src):
                print(f"Error: source not found: {src}")
                return 2
            if os.path.exists(dst) and not args.force:
                print(f"Refusing to overwrite existing {dst}. Use --force to replace.")
                return 1
            os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
            shutil.copy2(src, dst)
            print(f"Wrote {dst} from {src}")
            return 0

    # Should not reach here if all subcommands handled
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
