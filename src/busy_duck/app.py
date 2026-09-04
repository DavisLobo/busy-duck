from busy_duck.database.connection import get_session, initialize_database


def main() -> None:
    """Initialize Busy Duck application infrastructure."""
    initialize_database()

    session = get_session()
    try:
        # Service and UI wiring will use this session.
        pass
    finally:
        session.close()


if __name__ == "__main__":
    main()
