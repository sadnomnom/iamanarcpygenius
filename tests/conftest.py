import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_arcpy():
    """Mock arcpy for unit tests"""
    with patch('arcpy') as mock:
        # Setup common arcpy mocks
        mock.env = Mock()
        mock.mp = Mock()  # ArcGIS Pro uses mp instead of mapping
        yield mock

@pytest.fixture
def real_arcpy():
    """Fixture for integration tests that need real arcpy"""
    try:
        import arcpy
        return arcpy
    except ImportError:
        pytest.skip("ArcGIS not installed - skipping integration test")
