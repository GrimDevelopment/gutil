def print_success(message: str) -> None:
    """Prints a success message in green."""
    print(f"\033[92m{message}\033[0m")

def print_error(message: str) -> None:
    """Prints an error message in red."""
    print(f"\033[91m{message}\033[0m")

def print_info(message: str) -> None:
    """Prints an informational message in blue."""
    print(f"\033[94m{message}\033[0m")

def print_warning(message: str) -> None:
    """Prints a warning message in yellow."""
    print(f"\033[93m{message}\033[0m")