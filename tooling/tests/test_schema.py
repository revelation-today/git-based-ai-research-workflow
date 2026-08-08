"""Tests for thscript.schema — TC-35, TC-36 (X-01..X-03).

The failure being prevented: one script writes `total`, a later script
reads `total_words`, and the survey recorded 24 KeyError from exactly that
drift. KeyError is the *lucky* outcome — the unlucky one is a key that
exists but means something else.
"""
import json
from pathlib import Path

import pytest

from thscript import schema

FIX = Path(__file__).parent / "fixtures"

COUNTS = schema.define("counts", {
    "unit": str,
    "total_words": int,
}, version=2)


# ------------------------------------------------------------- TC-35, X-01
def test_tc35_writing_a_row_missing_a_field_raises_at_write_time(tmp_path):
    """Not three scripts later, in a consumer."""
    with pytest.raises(schema.SchemaError) as e:
        schema.write_table(tmp_path / "out.json", [{"unit": "Tst.1"}],
                           schema=COUNTS)
    assert "total_words" in str(e.value)


def test_tc35b_a_valid_row_round_trips(tmp_path):
    p = tmp_path / "out.json"
    rows = [{"unit": "Tst.1", "total_words": 2}]
    schema.write_table(p, rows, schema=COUNTS)
    back = schema.read_table(p, schema=COUNTS)
    assert [dict(r) for r in back] == rows


def test_tc35c_wrong_type_is_rejected(tmp_path):
    with pytest.raises(schema.SchemaError):
        schema.write_table(tmp_path / "out.json",
                           [{"unit": "Tst.1", "total_words": "two"}],
                           schema=COUNTS)


def test_tc35d_unexpected_field_is_rejected(tmp_path):
    """An extra field is drift too, and silently ignoring it hides it."""
    with pytest.raises(schema.SchemaError):
        schema.write_table(tmp_path / "out.json",
                           [{"unit": "Tst.1", "total_words": 2, "extra": 1}],
                           schema=COUNTS)


# ------------------------------------------------------------- TC-36, X-02
def test_tc36_reading_an_older_version_raises():
    """The exact 24-KeyError shape, caught at the boundary instead."""
    with pytest.raises(schema.SchemaError) as e:
        schema.read_table(FIX / "schema/produced_v1.json", schema=COUNTS)
    assert "version" in str(e.value).lower()


def test_tc36b_the_v1_fixture_really_is_the_drifted_shape():
    """Precondition: the fixture must actually carry the old field name."""
    raw = json.loads((FIX / "schema/produced_v1.json").read_text(encoding="utf-8"))
    assert raw["version"] == 1
    assert "total" in raw["rows"][0]
    assert "total_words" not in raw["rows"][0]


def test_tc36c_the_matching_version_reads_cleanly():
    rows = schema.read_table(FIX / "schema/produced_v2.json", schema=COUNTS)
    assert rows[0]["total_words"] == 2


# ------------------------------------------------------------- TC-?? , X-03
def test_x03_rows_expose_typed_access():
    rows = schema.read_table(FIX / "schema/produced_v2.json", schema=COUNTS)
    r = rows[0]
    assert r.total_words == 2          # attribute access, not a string key
    assert r["total_words"] == 2       # mapping access still available


def test_x03b_unknown_field_access_fails_loudly():
    rows = schema.read_table(FIX / "schema/produced_v2.json", schema=COUNTS)
    with pytest.raises((AttributeError, KeyError)):
        rows[0].total                  # the drifted name must not resolve


# ------------------------------------------------------------- edge cases
def test_empty_table_round_trips(tmp_path):
    p = tmp_path / "empty.json"
    schema.write_table(p, [], schema=COUNTS)
    assert schema.read_table(p, schema=COUNTS) == []


def test_reading_a_file_written_by_another_schema_raises(tmp_path):
    other = schema.define("other", {"a": int}, version=1)
    p = tmp_path / "x.json"
    schema.write_table(p, [{"a": 1}], schema=other)
    with pytest.raises(schema.SchemaError) as e:
        schema.read_table(p, schema=COUNTS)
    assert "counts" in str(e.value) or "other" in str(e.value)


def test_unicode_survives_the_round_trip(tmp_path):
    """Hebrew in a data file must not be mangled or escaped away."""
    s = schema.define("heb", {"word": str}, version=1)
    p = tmp_path / "h.json"
    schema.write_table(p, [{"word": "בְּרֵאשִׁית"}], schema=s)
    assert schema.read_table(p, schema=s)[0]["word"] == "בְּרֵאשִׁית"
    assert "\\u" not in p.read_text(encoding="utf-8")
