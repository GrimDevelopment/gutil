from cli.commands import auth, generate, config
import argparse

def main():
    parser = argparse.ArgumentParser(description="CLI tool for interacting with the Codex backend.")
    subparsers = parser.add_subparsers(dest="command")

    # Authentication commands
    auth_parser = subparsers.add_parser("auth", help="Authentication commands")
    auth.add_auth_commands(auth_parser)

    # Generate commands
    generate_parser = subparsers.add_parser("generate", help="Generate content using Codex")
    generate.add_generate_commands(generate_parser)

    # Configuration commands
    config_parser = subparsers.add_parser("config", help="Configuration commands")
    config.add_config_commands(config_parser)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    else:
        if args.command == "auth":
            auth.handle_auth_command(args)
        elif args.command == "generate":
            generate.handle_generate_command(args)
        elif args.command == "config":
            config.handle_config_command(args)

if __name__ == "__main__":
    main()