import json
from geom328 import generate_dataset

def test_image_size(tmp_path):
    output_dir = tmp_path / "image_size"

    generate_dataset(
        output_dir=output_dir,
        classes=[0],
        samples_per_class=1,
        seed=123,
        image_size=128,
        validate=True,
        split=False,
    )

    from PIL import Image

    image = Image.open(output_dir / "images" / "000000.png")

    assert image.size == (128, 128)


def test_number_of_objects(tmp_path):
    output_dir = tmp_path / "objects"

    generate_dataset(
        output_dir=output_dir,
        classes=[0],
        samples_per_class=5,
        seed=123,
        min_objects=4,
        max_objects=4,
        validate=True,
        split=False,
    )

    for scene_path in (output_dir / "scenes").glob("*.json"):
        with open(scene_path) as f:
            scene = json.load(f)

        assert len(scene["objects"]) == 4


def test_size_configuration(tmp_path):
    output_dir = tmp_path / "sizes"

    generate_dataset(
        output_dir=output_dir,
        classes=[0],
        samples_per_class=5,
        seed=123,
        min_size=2.0,
        max_size=7.0,
        validate=True,
        split=False,
    )

    for scene_path in (output_dir / "scenes").glob("*.json"):
        with open(scene_path) as f:
            scene = json.load(f)

        for obj in scene["objects"]:
            assert 2.0 <= obj["size"] <= 7.0


def test_rotation_can_be_disabled(tmp_path):
    output_dir = tmp_path / "no_rotation"

    generate_dataset(
        output_dir=output_dir,
        classes=[0],
        samples_per_class=5,
        seed=123,
        rotation=False,
        validate=True,
        split=False,
    )

    for scene_path in (output_dir / "scenes").glob("*.json"):
        with open(scene_path) as f:
            scene = json.load(f)

        for obj in scene["objects"]:
            assert obj["angle"] == 0