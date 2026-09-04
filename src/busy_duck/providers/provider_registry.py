from __future__ import annotations

from typing import Type

from busy_duck.providers.base_provider import BaseProvider
from busy_duck.providers.google_provider import GoogleProvider
from busy_duck.providers.outlook_provider import OutlookProvider


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, Type[BaseProvider]] = {}

    def register(self, name: str, provider_cls: Type[BaseProvider]) -> None:
        self._providers[name] = provider_cls

    def create(self, name: str, config: dict | None = None) -> BaseProvider:
        key = name.lower()
        if key not in self._providers:
            raise ValueError(f"Provider '{name}' not registered.")

        return self._providers[key](config or {})

    def list_registered(self) -> list[str]:
        return sorted(self._providers.keys())


registry = ProviderRegistry()
registry.register("google", GoogleProvider)
registry.register("outlook", OutlookProvider)