from __future__ import annotations

from typing import Callable

from busy_duck.providers.base_provider import BaseProvider
from busy_duck.providers.google_provider import GoogleProvider


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, Callable[..., BaseProvider]] = {}

    def register(self, name: str, factory: Callable[..., BaseProvider]) -> None:
        self._providers[name] = factory

    def create(self, name: str, config: dict | None = None) -> BaseProvider:
        if name not in self._providers:
            raise ValueError(f"Provider '{name}' is not registered.")
        return self._providers[name](config)

    def list(self) -> list[str]:
        return sorted(self._providers.keys())


registry = ProviderRegistry()
registry.register("google", GoogleProvider)