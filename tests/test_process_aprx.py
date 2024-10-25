import pytest
from pathlib import Path
from scripts.process_aprx import APRXProcessor

def test_aprx_processor_initialization():
    processor = APRXProcessor(Path("test.aprx"))
    assert processor.aprx_path == Path("test.aprx")
    assert processor.aprx is None
