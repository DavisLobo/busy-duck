from busy_duck.database.connection import initialize_database


def main() -> None:
    """Initialize Busy Duck application infrastructure."""
    initialize_database()


if __name__ == "__main__":
    main()
