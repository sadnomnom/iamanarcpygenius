import pytest
from pathlib import Path
from scripts.file_handler import FileHandler
from unittest.mock import Mock

@pytest.mark.unit
def test_validate_file(mock_arcpy, tmp_path):
    """Test file validation without real arcpy"""
    handler = FileHandler()
    test_file = tmp_path / "test.mxd"
    test_file.touch()
    assert handler.validate_file(test_file)

@pytest.mark.unit
def test_process_file_mxd(mock_arcpy, tmp_path):
    """Test MXD processing with mocked arcpy"""
    handler = FileHandler()
    input_path = tmp_path / "test.mxd"
    output_path = tmp_path / "test.pdf"
    input_path.touch()
    
    # Configure mock behavior for ArcGIS Pro
    mock_arcpy.mp.ArcGISProject.return_value.listLayouts.return_value = [Mock()]
    
    assert handler.process_file(input_path, output_path)
