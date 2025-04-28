"""Main module for the sales data export script."""

from getpass import getpass
from core.exportar_relatorios_v2 import get_sales_data


def main() -> None:
    """Main function."""
    username: str = input("Enter your username: ")
    password: str = getpass("Enter your password: ")
    get_sales_data(username, password)


if __name__ == "__main__":
    main()
