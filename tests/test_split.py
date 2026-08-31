import pandas as pd

from geom328 import DatasetSplitter

def create_test_metadata(path):
    rows = []

    image_id = 0

    for class_id in [0, 5, 7]:
        for _ in range(20):
            rows.append(
                {
                    "image_id": image_id,
                    "image_name": f"{image_id:06d}.png",
                    "class": class_id,
                }
            )

            image_id += 1

    pd.DataFrame(rows).to_csv(path, index=False)


def test_split_preserves_class_distribution(tmp_path):
    metadata_path = tmp_path / "metadata.csv"
    output_dir = tmp_path / "split"

    create_test_metadata(metadata_path)

    splitter = DatasetSplitter(seed=123)

    splitter.split(
        metadata_csv=metadata_path,
        output_dir=output_dir,
        train_ratio=0.70,
        val_ratio=0.15,
        test_ratio=0.15,
    )

    train = pd.read_csv(output_dir / "train.csv")
    val = pd.read_csv(output_dir / "val.csv")
    test = pd.read_csv(output_dir / "test.csv")

    assert len(train) == 42
    assert len(val) == 9
    assert len(test) == 9

    for class_id in [0, 5, 7]:
        assert (train["class"] == class_id).sum() == 14
        assert (val["class"] == class_id).sum() == 3
        assert (test["class"] == class_id).sum() == 3


def test_split_is_reproducible(tmp_path):
    metadata_path = tmp_path / "metadata.csv"

    create_test_metadata(metadata_path)

    output_a = tmp_path / "split_a"
    output_b = tmp_path / "split_b"

    splitter_a = DatasetSplitter(seed=123)
    splitter_a.split(metadata_csv=metadata_path, output_dir=output_a,)

    splitter_b = DatasetSplitter(seed=123)
    splitter_b.split(metadata_csv=metadata_path, output_dir=output_b,)

    train_a = pd.read_csv(output_a / "train.csv")
    train_b = pd.read_csv(output_b / "train.csv")

    val_a = pd.read_csv(output_a / "val.csv")
    val_b = pd.read_csv(output_b / "val.csv")

    test_a = pd.read_csv(output_a / "test.csv")
    test_b = pd.read_csv(output_b / "test.csv")

    pd.testing.assert_frame_equal(train_a, train_b)
    pd.testing.assert_frame_equal(val_a, val_b)
    pd.testing.assert_frame_equal(test_a, test_b)


def test_split_different_seeds_produce_different_splits(tmp_path):
    metadata_path = tmp_path / "metadata.csv"

    create_test_metadata(metadata_path)

    output_a = tmp_path / "split_a"
    output_b = tmp_path / "split_b"

    splitter_a = DatasetSplitter(seed=123)
    splitter_a.split(metadata_csv=metadata_path, output_dir=output_a,)

    splitter_b = DatasetSplitter(seed=456)
    splitter_b.split(metadata_csv=metadata_path, output_dir=output_b,)

    train_a = pd.read_csv(output_a / "train.csv")
    train_b = pd.read_csv(output_b / "train.csv")

    assert not train_a.equals(train_b)