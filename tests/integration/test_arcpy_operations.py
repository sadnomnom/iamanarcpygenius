import pytest
from pathlib import Path
from scripts.file_handler import FileHandler

@pytest.mark.integration
def test_real_arcpy_operations(real_arcpy):
    """Test with real arcpy - only runs if ArcGIS is installed"""
    assert real_arcpy.env is not None
    assert hasattr(real_arcpy, 'mp')  # Changed from 'mapping' to 'mp' for ArcGIS Pro

@pytest.mark.integration
def test_process_real_mxd(real_arcpy, tmp_path):
    """Test processing a real MXD file"""
    # This test only runs if test data is available
    test_mxd = Path("tests/data/test.mxd")
    if not test_mxd.exists():
        pytest.skip("Test MXD file not available")
    
    handler = FileHandler()
    output_path = tmp_path / "output.pdf"
    
    result = handler.process_file(test_mxd, output_path)
    assert result
    assert output_path.exists()
