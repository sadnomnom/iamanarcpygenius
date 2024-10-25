import pytest
from pathlib import Path
from scripts.table_builder import TableBuilder

def test_table_builder_initialization():
    builder = TableBuilder()
    assert len(builder.data) == 0

def test_add_entry():
    builder = TableBuilder()
    builder.add_entry(
        Path("input.mxd"),
        Path("output.pdf"),
        "Success",
        1.5
    )
    assert len(builder.data) == 1
    assert builder.data[0]["Status"] == "Success"
