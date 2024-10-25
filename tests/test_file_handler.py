import pytest
from pathlib import Path
from scripts.file_handler import FileHandler

def test_file_handler_initialization():
    handler = FileHandler()
    assert '.mxd' in handler.supported_extensions
    assert '.aprx' in handler.supported_extensions

def test_validate_file(tmp_path):
    handler = FileHandler()
    test_file = tmp_path / "test.mxd"
    test_file.touch()
    assert handler.validate_file(test_file)
