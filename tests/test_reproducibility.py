from pathlib import Path

from geom328 import generate_dataset

def test_same_seed_produces_identical_dataset(tmp_path):
    output_a = tmp_path / "dataset_a"
    output_b = tmp_path / "dataset_b"

    generate_dataset(
        output_dir=output_a,
        classes=[0, 5, 7],
        samples_per_class=5,
        seed=123,
        validate=True,
        split=True,
    )

    generate_dataset(
        output_dir=output_b,
        classes=[0, 5, 7],
        samples_per_class=5,
        seed=123,
        validate=True,
        split=True,
    )

    files_to_compare = [
        "metadata/metadata.csv",
        "train.csv",
        "val.csv",
        "test.csv",
        "dataset_info.txt",
        "split_info.txt",
        "scenes/000000.json",
        "scenes/000005.json",
        "svg/000000.svg",
        "svg/000005.svg",
        "images/000000.png",
        "images/000005.png",
    ]

    for relative_path in files_to_compare:
        file_a = output_a / relative_path
        file_b = output_b / relative_path

        assert file_a.exists(), f"Missing file: {file_a}"
        assert file_b.exists(), f"Missing file: {file_b}"

        assert file_a.read_bytes() == file_b.read_bytes(), (f"Files differ: {relative_path}")

def test_different_seeds_produce_different_dataset(tmp_path):
    output_a = tmp_path / "dataset_a"
    output_b = tmp_path / "dataset_b"

    generate_dataset(
        output_dir=output_a,
        classes=[0, 5, 7],
        samples_per_class=5,
        seed=123,
        validate=True,
        split=True,
    )

    generate_dataset(
        output_dir=output_b,
        classes=[0, 5, 7],
        samples_per_class=5,
        seed=456,
        validate=True,
        split=True,
    )

    scene_a = (output_a / "scenes" / "000000.json").read_bytes()
    scene_b = (output_b / "scenes" / "000000.json").read_bytes()

    assert scene_a != scene_b