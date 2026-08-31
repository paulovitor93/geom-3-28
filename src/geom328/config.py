from dataclasses import dataclass
from typing import Optional, Sequence

@dataclass
class GeomConfig:
    """
    Configuration for Geom-3-28 dataset generation.
    """

    # Dataset
    # --------------------------------------------------
    classes: Optional[Sequence[int]] = None
    samples_per_class: int = 100

    # Reproducibility
    # --------------------------------------------------
    seed: int = 42
    split_seed: int = 42

    # Image
    # --------------------------------------------------
    image_size: int = 224

    # Number of objects
    # --------------------------------------------------
    min_objects: int = 3
    max_objects: int = 5

    # Logical object size
    # --------------------------------------------------
    min_size: float = 2.0
    max_size: float = 7.0

    min_largest_size: float = 5.0
    min_size_difference: float = 2.2

    # Spatial arrangement
    # --------------------------------------------------
    lambda_min: float = 0.2


    # Rendering
    # --------------------------------------------------
    rotation: bool = True

    # Output
    # --------------------------------------------------
    save_png: bool = True
    save_svg: bool = True
    save_scenes: bool = True
    save_metadata: bool = True

    # Validation
    # --------------------------------------------------
    validate: bool = True

    # Dataset split
    # --------------------------------------------------
    split: bool = True

    train_ratio: float = 0.70
    val_ratio: float = 0.15
    test_ratio: float = 0.15