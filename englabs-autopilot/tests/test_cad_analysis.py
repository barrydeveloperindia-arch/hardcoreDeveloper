import pytest
from src.cad_worker import calculate_bounding_box_volume

def test_calculate_bounding_box_volume_cube():
    # Mocking a 10x10x10 cube parsed from a STEP file
    mock_dimensions = {"x": 10.0, "y": 10.0, "z": 10.0}
    volume = calculate_bounding_box_volume(mock_dimensions)
    assert volume == 1000.0, f"Expected 1000.0, got {volume}"

def test_calculate_bounding_box_volume_zero():
    # Edge case
    mock_dimensions = {"x": 0.0, "y": 10.0, "z": 10.0}
    volume = calculate_bounding_box_volume(mock_dimensions)
    assert volume == 0.0
