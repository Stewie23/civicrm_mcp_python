from __future__ import annotations
import time
import typing as t

class SchemaCache:
    """Sehr einfacher In-Memory-Cache für Entities/Felder."""
    def __init__(self, ttl_seconds: int = 600):
        self.ttl = ttl_seconds
        self._entities: tuple[float, list[str]] | None = None
        self._fields: dict[str, tuple[float, list[dict]]] = {}

    def get_entities(self) -> list[str] | None:
        if self._entities is None:
            return None
        ts, data = self._entities
        if time.time() - ts > self.ttl:
            self._entities = None
            return None
        return data

    def set_entities(self, entities: list[str]) -> None:
        self._entities = (time.time(), entities)

    def get_fields(self, entity: str) -> list[dict] | None:
        entry = self._fields.get(entity)
        if not entry:
            return None
        ts, data = entry
        if time.time() - ts > self.ttl:
            self._fields.pop(entity, None)
            return None
        return data

    def set_fields(self, entity: str, fields: list[dict]) -> None:
        self._fields[entity] = (time.time(), fields)
