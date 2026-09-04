from __future__ import annotations

import argparse
from datetime import datetime

from busy_duck.app import sync_all
from busy_duck.database.connection import get_session
from busy_duck.repositories.event_repository import EventRepository


def cmd_sync(args) -> None:
    result = sync_all()
    for provider_name, count in result.items():
        print(f"{provider_name}: {count} events synced")
    print("Sync completed.")


def cmd_list(args) -> None:
    session = get_session()
    try:
        repo = EventRepository(session)
        events = repo.find_all()
        for event in events:
            print(
                f"{event.title} | {event.provider_id} | "
                f"{event.start_datetime.isoformat()} -> {event.end_datetime.isoformat()}"
            )
    finally:
        session.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Busy Duck CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    sync_parser = subparsers.add_parser("sync", help="Sync all registered providers")
    sync_parser.set_defaults(func=cmd_sync)

    list_parser = subparsers.add_parser("list", help="List locally stored events")
    list_parser.set_defaults(func=cmd_list)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()