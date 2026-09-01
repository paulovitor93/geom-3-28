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
    seed: Optional[int] = None

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
    validation_attempts: int = 1000

    # Dataset split
    # --------------------------------------------------
    split: bool = True

    train_ratio: float = 0.70
    val_ratio: float = 0.15
    test_ratio: float = 0.15

    def __post_init__(self):
        if self.min_objects < 1:
            raise ValueError("min_objects must be at least 1.")

        if self.max_objects < self.min_objects:
            raise ValueError("max_objects must be greater than or equal to min_objects.")

        if self.min_size <= 0:
            raise ValueError("min_size must be greater than 0.")

        if self.max_size <= self.min_size:
            raise ValueError("max_size must be greater than min_size.")

        if self.min_largest_size > self.max_size:
            raise ValueError("min_largest_size cannot exceed max_size.")

        if self.min_size_difference <= 0:
            raise ValueError("min_size_difference must be greater than 0.")

        if self.min_size + self.min_size_difference > self.max_size:
            raise ValueError("min_size + min_size_difference must be less than or equal to max_size.")

        if self.lambda_min < 0:
            raise ValueError("lambda_min cannot be negative.")

        if self.lambda_min > 1:
            raise ValueError("lambda_min cannot be greater than 1.")

        if self.train_ratio < 0:
            raise ValueError("train_ratio cannot be negative.")

        if self.val_ratio < 0:
            raise ValueError("val_ratio cannot be negative.")

        if self.test_ratio < 0:
            raise ValueError("test_ratio cannot be negative.")

        ratio_sum = (self.train_ratio + self.val_ratio + self.test_ratio)

        if abs(ratio_sum - 1.0) > 1e-8:
            raise ValueError("train_ratio + val_ratio + test_ratio must equal 1.")

        if self.validation_attempts < 1:
            raise ValueError("validation_attempts must be at least 1.")