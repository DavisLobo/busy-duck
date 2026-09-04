# BusyDuck 🦆

> All your calendars in one pond.

Busy Duck is a desktop application built with Python that consolidates events from multiple calendar providers into a single local and unified view.

The application focuses on aggregation, normalization, and enrichment of calendar data while keeping user data stored locally.

## Features

### Current Goals

- Connect multiple calendar providers
- Aggregate events into a unified timeline
- Detect scheduling conflicts
- Calculate availability and free time
- Persist event data locally
- Enrich events with external information such as weather forecasts

### Supported Providers (Planned)

- Google Calendar
- Microsoft Outlook Calendar
- Apple Calendar

### Future Enhancements

- Meeting analytics
- Productivity insights
- Travel and commute suggestions
- Smart event categorization
- Desktop notifications
- Calendar health reports

---

## Architecture

Busy Duck follows a modular architecture inspired by clean software engineering principles.

```text
Provider APIs
       |
       v
  Connectors
       |
       v
   Services
       |
       v
 Repositories
       |
       v
   SQLite DB
       |
       v
 Desktop UI
```

### Main Layers

#### Connectors

Responsible for interacting with external providers.

Examples:

- Google Calendar
- Outlook Calendar
- Apple Calendar
- Weather APIs

#### Services

Contain business logic such as:

- Event synchronization
- Event merging
- Conflict detection
- Availability calculation
- Weather enrichment

#### Repositories

Provide data access abstraction and database operations.

#### UI

Desktop user interface built with Qt.

---

## Technology Stack

### Language

- Python 3.13+

### Desktop Framework

- PySide6 (Qt)

### Database

- SQLite

### ORM

- SQLAlchemy

### Validation

- Pydantic

### Testing

- Pytest

---

## Project Structure

```text
busy-duck/
│
├── README.md
├── pyproject.toml
├── .gitignore
│
├── docs/
│
├── tests/
│
└── src/
    └── busy_duck/
        │
        ├── app.py
        │
        ├── ui/
        │   ├── windows/
        │   ├── dialogs/
        │   └── widgets/
        │
        ├── connectors/
        │   ├── google/
        │   ├── outlook/
        │   ├── apple/
        │   └── weather/
        │
        ├── services/
        │   ├── sync_service.py
        │   ├── calendar_service.py
        │   ├── analytics_service.py
        │   └── weather_service.py
        │
        ├── repositories/
        │   ├── event_repository.py
        │   ├── account_repository.py
        │   └── settings_repository.py
        │
        ├── models/
        │   ├── event.py
        │   ├── calendar.py
        │   └── account.py
        │
        ├── database/
        │   └── connection.py
        │
        ├── config/
        │
        └── assets/
```

---

## Design Principles

Busy Duck is built around the following principles:

- Local-first architecture
- Read-only integration with external providers
- Clear separation of concerns
- Modular and maintainable codebase
- Provider-agnostic integrations
- Extensible architecture
- Minimal setup for end users

---

## Vision

Most people manage multiple calendars across different providers.

Busy Duck does not aim to replace existing calendar platforms.

Instead, it provides a single source of visibility by bringing events together, identifying conflicts, and generating insights that individual providers cannot easily offer on their own.

---

## Status

🚧 Early Development

Busy Duck is currently in the planning and architecture phase.