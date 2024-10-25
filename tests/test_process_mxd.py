import pytest
from pathlib import Path
from scripts.process_mxd import MXDProcessor

def test_mxd_processor_initialization():
    processor = MXDProcessor(Path("test.mxd"))
    assert processor.mxd_path == Path("test.mxd")
    assert processor.mxd is None
