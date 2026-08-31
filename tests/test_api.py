from pathlib import Path
import pandas as pd

from geom328 import generate_dataset

def test_selected_classes(tmp_path):
    output_dir = tmp_path / "selected_classes"

    generate_dataset(
        output_dir=output_dir,
        classes=[0, 5, 7],
        samples_per_class=2,
        seed=123,
        validate=True,
        split=False,
    )

    metadata = pd.read_csv(output_dir / "metadata" / "metadata.csv")

    assert len(metadata) == 6
    assert sorted(metadata["class"].unique()) == [0, 5, 7]
    assert all(
        metadata["class"].value_counts()[class_id] == 2
        for class_id in [0, 5, 7]
    )

def test_all_classes(tmp_path):
    output_dir = tmp_path / "all_classes"

    generate_dataset(
        output_dir=output_dir,
        classes="all",
        samples_per_class=1,
        seed=123,
        validate=True,
        split=False,
    )

    metadata = pd.read_csv(output_dir / "metadata" / "metadata.csv")

    assert len(metadata) == 28
    assert sorted(metadata["class"].unique()) == list(range(28))


def test_none_classes_generates_all_classes(tmp_path):
    output_dir = tmp_path / "none_classes"

    generate_dataset(
        output_dir=output_dir,
        classes=None,
        samples_per_class=1,
        seed=123,
        validate=True,
        split=False,
    )

    metadata = pd.read_csv(output_dir / "metadata" / "metadata.csv")

    assert len(metadata) == 28
    assert sorted(metadata["class"].unique()) == list(range(28))