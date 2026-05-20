def calculate_bounding_box_volume(dimensions: dict) -> float:
    """
    Calculates the bounding box volume from FreeCAD/step dimensions.
    """
    return dimensions.get("x", 0.0) * dimensions.get("y", 0.0) * dimensions.get("z", 0.0)
