import pytest

from geom328 import generate_dataset

def test_invalid_class_is_rejected(tmp_path):
    with pytest.raises(ValueError, match="Unknown class IDs"):
        generate_dataset(
            output_dir=tmp_path / "invalid_class",
            classes=[999],
            samples_per_class=1,
            seed=123,
            validate=False,
            split=False,
        )

def test_mixed_valid_and_invalid_classes_are_rejected(tmp_path):
    with pytest.raises(ValueError, match="Unknown class IDs"):
        generate_dataset(
            output_dir=tmp_path / "mixed_classes",
            classes=[0, 5, 999],
            samples_per_class=1,
            seed=123,
            validate=False,
            split=False,
        )

def test_validation_enabled_generates_valid_scenes(tmp_path):
    output_dir = tmp_path / "validation"

    generate_dataset(
        output_dir=output_dir,
        classes=[0, 5, 7],
        samples_per_class=2,
        seed=123,
        validate=True,
        split=False,
    )

    assert (output_dir / "metadata" / "metadata.csv").exists()