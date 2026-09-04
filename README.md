# Busy Duck 🦆

> All your calendars in one pond.

Busy Duck is a local-first Python desktop application that consolidates calendar events from multiple providers into one unified view.

It currently supports demo connectors for Google Calendar and Microsoft Outlook, event normalization, conflict detection, availability calculation, local SQLite persistence, account management, and light/dark themes.

## Current features

- Desktop UI built with PySide6
- Unified calendar agenda
- Google Calendar demo provider
- Microsoft Outlook demo provider
- Local SQLite database
- Event synchronization and normalization
- Conflict detection
- Free-time calculation
- Provider and account management
- Edit and delete connected accounts
- Light and dark themes
- Search and event sorting
- Calendar, Overview, Availability, and Insights navigation
- Application icon and enterprise-style interface
- CLI synchronization and event listing

> Provider integrations currently use demo data. Real Google and Microsoft OAuth integrations are planned.

## Technology stack

- Python 3.11+
- PySide6
- SQLAlchemy
- SQLite
- Pydantic
- Pytest
- python-dotenv

## Architecture

```text
Provider adapters
       |
       v
Synchronization services
       |
       v
Repositories
       |
       v
SQLite database
       |
       v
PySide6 desktop UI
```

### Providers

Provider adapters implement a common interface and return normalized event data.

Current providers:

- `google`
- `outlook`

### Services

Services contain application and business logic:

- Event synchronization
- Multi-provider synchronization
- Conflict detection
- Free-time calculation
- Calendar event queries
- Weather service abstraction

### Repositories

Repositories isolate database access for:

- Accounts
- Providers
- Provider configurations
- Calendars
- Events

### UI

The UI includes:

- Main dashboard
- Calendar agenda
- Account setup dialog
- Event table model
- Light and dark themes
- Provider status indicators

## Project structure

```text
busy-duck/
├── README.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── build.spec
├── docs/
│   └── USAGE.md
├── tests/
│   └── test_app_pipeline.py
└── src/
    └── busy_duck/
        ├── __init__.py
        ├── app.py
        ├── cli.py
        ├── config.py
        ├── main.py
        ├── database/
        │   ├── connection.py
        │   └── models/
        │       ├── base.py
        │       ├── account_model.py
        │       ├── calendar_model.py
        │       ├── event_model.py
        │       ├── provider_config_model.py
        │       └── provider_model.py
        ├── models/
        │   ├── account.py
        │   ├── calendar.py
        │   ├── event.py
        │   └── provider.py
        ├── providers/
        │   ├── base_provider.py
        │   ├── google_provider.py
        │   ├── outlook_provider.py
        │   └── provider_registry.py
        ├── repositories/
        │   ├── account_repository.py
        │   ├── calendar_repository.py
        │   ├── event_repository.py
        │   ├── provider_config_repository.py
        │   └── provider_repository.py
        ├── services/
        │   ├── analytics_service.py
        │   ├── calendar_service.py
        │   ├── multi_provider_sync_service.py
        │   ├── provider_sync_service.py
        │   ├── sync_service.py
        │   └── weather_service.py
        └── ui/
            ├── account_setup.py
            ├── busy_duck.svg
            ├── event_table_model.py
            ├── main_window.py
            └── theme.py
```

## Installation

```bash
git clone <repository-url>
cd busy-duck

python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e .
```

## Running the desktop application

```bash
PYTHONPATH=src python -m busy_duck.main
```

The application creates its SQLite database under:

```text
data/busy_duck.db
```

For headless environments:

```bash
QT_QPA_PLATFORM=offscreen PYTHONPATH=src python -m busy_duck.main
```

## Running tests

```bash
python -m pytest -q
```

## CLI usage

Synchronize configured providers:

```bash
PYTHONPATH=src python -m busy_duck.cli sync
```

List locally stored events:

```bash
PYTHONPATH=src python -m busy_duck.cli list
```

## Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Available settings include:

```env
APP_ENV=development
APP_NAME=busy_duck
DB_PATH=./data/busy_duck.db
DEFAULT_TIME_WINDOW_DAYS=7
```

OAuth variables are reserved for future real provider integrations:

```env
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:8000/oauth/google/callback

OUTLOOK_CLIENT_ID=
OUTLOOK_CLIENT_SECRET=
OUTLOOK_REDIRECT_URI=http://localhost:8000/oauth/outlook/callback
```

Never commit `.env`, access tokens, client secrets, or the local database.

## Account management

Open **Accounts** from the sidebar to:

- Add an account
- Select Google Calendar or Microsoft Outlook
- Edit account name and email
- Delete an account
- Trigger synchronization for a new account

The current implementation uses demo provider data and does not perform real OAuth authentication.

## Application workflow

1. Start Busy Duck.
2. Open **Accounts**.
3. Add one or more provider accounts.
4. Return to **Calendar**.
5. Click **Sync calendars**.
6. Review events in the unified agenda.
7. Use search, date filters, sorting, and theme controls.
8. Select an event to inspect its details.
9. Review conflicts and available time in the dashboard.

## Development status

Busy Duck is an early MVP. The next major development areas are:

- Real Google Calendar OAuth
- Real Microsoft Graph OAuth
- Apple Calendar support
- Background synchronization
- Month and week calendar views
- Persistent user preferences
- Weather enrichment
- Notifications
- Meeting analytics

## License

Busy Duck is distributed under the GNU General Public License v3. See [LICENSE](LICENSE).