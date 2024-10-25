import pytest
from pathlib import Path
from scripts.file_handler import FileHandler

def test_validate_file(mock_arcpy, tmp_path):
    """Test file validation without real arcpy"""
    handler = FileHandler()
    test_file = tmp_path / "test.mxd"
    test_file.touch()
    assert handler.validate_file(test_file)

def test_process_file_mxd(mock_arcpy, tmp_path):
    """Test MXD processing with mocked arcpy"""
    handler = FileHandler()
    input_path = tmp_path / "test.mxd"
    output_path = tmp_path / "test.pdf"
    input_path.touch()
    
    # Configure mock behavior
    mock_arcpy.mapping.MapDocument.return_value.dataDrivenPages.exportToPDF.return_value = True
    
    assert handler.process_file(input_path, output_path)
