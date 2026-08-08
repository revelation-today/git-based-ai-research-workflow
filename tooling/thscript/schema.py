"""Declared data contracts between scripts — the C-03 module.

The failure: one script writes ``total``, a later script reads
``total_words``. The survey recorded 24 ``KeyError`` from that drift, and
74 scripts index results by bare string literal.

``KeyError`` is the *lucky* outcome. The unlucky one is a key that exists
but means something different from what the consumer assumes — no
exception, just a wrong number. So validation happens at **both** ends and
a version mismatch is an error rather than a best-effort read.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

__all__ = ["define", "Schema", "Row", "SchemaError", "read_table",
           "write_table"]


class SchemaError(ValueError):
    """Raised when data and its declared contract disagree."""


@dataclass(frozen=True)
class Schema:
    name: str
    fields: dict           # field name -> python type
    version: int = 1

    def validate(self, row: dict, *, where: str) -> None:
        missing = set(self.fields) - set(row)
        extra = set(row) - set(self.fields)
        if missing:
            raise SchemaError(
                f"{where}: missing field(s) {sorted(missing)} for schema "
                f"{self.name!r} v{self.version}")
        if extra:
            raise SchemaError(
                f"{where}: unexpected field(s) {sorted(extra)} for schema "
                f"{self.name!r} v{self.version} — an extra field is drift "
                f"too, and ignoring it hides it")
        for key, want in self.fields.items():
            got = row[key]
            if want is float and isinstance(got, int) and not isinstance(got, bool):
                continue
            if not isinstance(got, want) or isinstance(got, bool) is not (want is bool):
                raise SchemaError(
                    f"{where}: field {key!r} should be {want.__name__}, "
                    f"got {type(got).__name__} ({got!r})")


def define(name: str, fields: dict, *, version: int = 1) -> Schema:
    return Schema(name=name, fields=dict(fields), version=version)


class Row(dict):
    """A validated row. Supports attribute access so that a drifted field
    name fails loudly instead of silently resolving (X-03)."""

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError as exc:
            raise AttributeError(
                f"no field {item!r}; this row has {sorted(self)}") from exc


def write_table(path, rows, *, schema: Schema) -> Path:
    """Validate every row, then write. Failure happens here, not downstream."""
    rows = [dict(r) for r in rows]
    for i, row in enumerate(rows):
        schema.validate(row, where=f"row {i} being written to {Path(path).name}")
    payload = {"schema": schema.name, "version": schema.version, "rows": rows}
    path = Path(path)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    return path


def read_table(path, *, schema: Schema) -> list[Row]:
    """Validate on read as well as on write.

    A version or name mismatch raises rather than being read best-effort —
    which is the whole point, since a best-effort read of a drifted file is
    how a wrong number reaches a paper.
    """
    path = Path(path)
    payload = json.loads(path.read_text(encoding="utf-8"))

    got_name = payload.get("schema")
    if got_name != schema.name:
        raise SchemaError(
            f"{path.name}: declares schema {got_name!r}, expected "
            f"{schema.name!r}")

    got_version = payload.get("version")
    if got_version != schema.version:
        raise SchemaError(
            f"{path.name}: schema {schema.name!r} version mismatch — file is "
            f"v{got_version}, this code expects v{schema.version}. Fields may "
            f"have been renamed; read it with the matching schema and migrate "
            f"deliberately.")

    rows = payload.get("rows", [])
    for i, row in enumerate(rows):
        schema.validate(row, where=f"row {i} of {path.name}")
    return [Row(r) for r in rows]
