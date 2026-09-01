# Geom-3-28

Geom-3-28 is a configurable synthetic dataset generator for geometric scenes.

The dataset contains 28 classes based on combinations of:

- geometric shape presence
- largest-object shape
- spatial relations between shapes

The generator can be used through either a Python API or a command-line interface.

# Project Structure

```text
geom-3-28/
│
├── src/
│   └── geom328/
│       ├── __init__.py
│       ├── classifier.py
│       ├── cli.py
│       ├── config.py
│       ├── constants.py
│       ├── dataset_builder.py
│       ├── extractor.py
│       ├── generator.py
│       ├── geometry.py
│       ├── objects.py
│       ├── renderer_svg.py
│       ├── scene.py
│       ├── specification.py
│       ├── split.py
│       └── validator.py
│
├── tests/
│
├── pyproject.toml
├── .gitignore
└── README.md
```
---

# Features

- Generate any subset of the 28 classes.
- Generate all 28 classes.
- Configure the number of samples per class.
- Generate datasets with a random seed automatically.
- Reproduce datasets with an explicit random seed.
- Configure image resolution.
- Configure the number of objects per scene.
- Configure logical object sizes.
- Configure the minimum distance between objects.
- Enable or disable object rotation.
- Validate generated scenes against their expected class.
- Generate SVG scenes.
- Generate PNG images.
- Save scene descriptions as JSON.
- Generate metadata CSV files.
- Create train, validation, and test splits.
- Use the generator through Python or the command line.
- Run automated tests with `pytest`.

---

# Installation

Clone the repository:

```bash
git clone https://github.com/paulovitor93/geom-3-28.git
cd geom-3-28
```

Install the package in editable mode:

```bash
pip install -e .
```

After installation, the package can be imported as `geom328`, and the command-line tool `generate_geom` becomes available.

---

# Quick Start

## Python API

The simplest example is:

```python
from geom328 import generate_dataset

generate_dataset(
    output_dir="my_dataset",
    classes=[0, 5, 7],
    samples_per_class=50,
)
```

If no seed is provided, a random seed is generated automatically.

The generation seed is stored in the generated dataset information.

---

## Reproducible Generation

To reproduce a dataset, provide an explicit seed:

```python
from geom328 import generate_dataset

generate_dataset(
    output_dir="my_dataset",
    classes=[0, 5, 7],
    samples_per_class=50,
    seed=123,
)
```

Using the same configuration and the same seed reproduces the generation process.

For example:

```python
generate_dataset(
    output_dir="dataset_a",
    classes=[0, 5, 7],
    samples_per_class=50,
    seed=123,
)

generate_dataset(
    output_dir="dataset_b",
    classes=[0, 5, 7],
    samples_per_class=50,
    seed=123,
)
```

The generation seed is also used for dataset splitting.

---

# Command-Line Interface

After installation, the following command is available:

```bash
generate_geom --help
```

Example:

```bash
generate_geom --classes 0 5 7 --samples-per-class 50
```

Generate all 28 classes:

```bash
generate_geom --classes all --samples-per-class 100
```

Generate a reproducible dataset:

```bash
generate_geom \
    --classes 0 5 7 \
    --samples-per-class 50 \
    --seed 123
```

Specify an output directory:

```bash
generate_geom \
    --classes 0 5 7 \
    --samples-per-class 50 \
    --output-dir my_dataset
```
When no classes are specified, all available classes are generated.

---

# Dataset Classes

Geom-3-28 contains 28 classes.

## Classes 0-2: Single-shape classes

| Class | Required Shape | Largest Shape |
|---:|---|---|
| 0 | Triangle | Triangle |
| 1 | Circle | Circle |
| 2 | Square | Square |

---

## Class 3: Presence class

Class 3 requires the presence of:

- Triangle
- Circle
- Square

There is no constraint specifying which shape must be the largest.

---

## Classes 4-11: Circle-Square relations

These classes contain circles and squares.

The classes vary according to:

- which shape is largest
- whether the circle is above the square
- whether the circle is left of the square

There are:

```text
2 largest-shape possibilities
× 2 vertical relations
× 2 horizontal relations
= 8 classes
```

The circle is the reference shape and the square is the target shape.

---

## Classes 12-19: Triangle-Circle relations

These classes contain triangles and circles.

The classes vary according to:

- which shape is largest
- whether the triangle is above the circle
- whether the triangle is left of the circle

The triangle is the reference shape and the circle is the target shape.

---

## Classes 20-27: Triangle-Square relations

These classes contain triangles and squares.

The classes vary according to:

- which shape is largest
- whether the triangle is above the square
- whether the triangle is left of the square

The triangle is the reference shape and the square is the target shape.

---

# Concepts

The dataset concept representation contains concepts describing:

1. shape presence
2. the largest shape
3. spatial relations between shape pairs

## Presence Concepts

```text
triangle_present
circle_present
square_present
```

---

## Largest-Shape Concepts

```text
largest_triangle
largest_circle
largest_square
```

---

## Spatial Concepts

```text
triangle_above_circle
triangle_left_circle

triangle_above_square
triangle_left_square

circle_above_square
circle_left_square
```

A spatial relation is true only when every object of the first shape satisfies the relation with every object of the second shape.

---

# Configuration

The generator can be configured through the Python API.

The main function is:

```python
generate_dataset(...)
```

The available parameters include:

| Parameter | Default | Description |
|---|---:|---|
| `output_dir` | `"geom328_dataset"` | Output directory |
| `classes` | `None` | Classes to generate |
| `samples_per_class` | `100` | Number of samples per class |
| `seed` | `None` | Random seed |
| `image_size` | `224` | Image resolution |
| `min_objects` | `3` | Minimum number of objects |
| `max_objects` | `5` | Maximum number of objects |
| `min_size` | `2.0` | Minimum logical object size |
| `max_size` | `7.0` | Maximum logical object size |
| `min_largest_size` | `5.0` | Minimum size of the largest object |
| `min_size_difference` | `2.2` | Minimum size difference between the largest and smaller objects |
| `lambda_min` | `0.2` | Minimum normalized distance between objects |
| `rotation` | `True` | Enable object rotation |
| `save_png` | `True` | Save PNG images |
| `save_svg` | `True` | Save SVG files |
| `save_scenes` | `True` | Save scene JSON files |
| `save_metadata` | `True` | Save metadata CSV |
| `validate` | `True` | Validate generated scenes |
| `validation_attempts` | `1000` | Maximum validation attempts |
| `split` | `True` | Create dataset splits |
| `train_ratio` | `0.70` | Training split ratio |
| `val_ratio` | `0.15` | Validation split ratio |
| `test_ratio` | `0.15` | Test split ratio |

---

# Object Configuration

## Number of Objects

Generate exactly four objects per scene:

```bash
generate_geom \
  --output-dir four_objects \
  --classes 0 5 7 \
  --samples-per-class 50 \
  --min-objects 4 \
  --max-objects 4
```
Using Python:
```python
generate_dataset(
    output_dir="four_objects",
    classes=[0, 5, 7],
    samples_per_class=50,
    min_objects=4,
    max_objects=4,
)
```

Allow between three and five objects:
```bash
generate_geom --min-objects 3 --max-objects 5
```
Using Python:
```python
generate_dataset(
    min_objects=3,
    max_objects=5,
)
```

---

# Size Configuration

Configure object sizes:
```bash
generate_geom --min-size 2.0 --max-size 7.0
```
Using Python:
```python
generate_dataset(
    min_size=2.0,
    max_size=7.0,
)
```

Configure the minimum size of the largest object:
```bash
generate_geom --min-largest-size 5.0
```
Using Python:
```python
generate_dataset(
    min_largest_size=5.0,
)
```

Configure the minimum size difference between the largest object and the other objects:
```bash
generate_geom --min-size-difference 2.2
```
Using Python:
```python
generate_dataset(
    min_size_difference=2.2,
)
```

The configuration validates that the size constraints are feasible.

---

# Spatial Configuration
## Overlap Control
The minimum normalized distance between objects can be configured with `lambda_min`.
```bash
generate_geom --lambda-min 0.2
```
Using Python:
```python
generate_dataset(
    lambda_min=0.2,
)
```

During placement, the normalized distance is computed using the effective radius of the objects.

---

# Rotation

Rotation is enabled by default.

Disable rotation in Python:
```bash
generate_geom --no-rotation
```
Using Python:

```python
generate_dataset(
    rotation=False,
)
```
When rotation is disabled, generated objects have an angle of zero.

---

# Scene Validation

Scene validation is enabled by default.

During generation:

1. a candidate scene is generated
2. concepts are extracted from the scene
3. the scene is validated against the expected class
4. generation is repeated if the candidate is invalid

The maximum number of attempts can be configured:
```bash
generate_geom --validation-attempts 1000
```
Using Python:
```python
generate_dataset(
    validate=True,
    validation_attempts=1000,
)
```

Disable validation in Python:
```bash
generate_geom --no-validation
```
Using Python:
```python
generate_dataset(
    validate=False,
)
```
If a valid scene cannot be generated within the configured number of attempts, generation raises an error.

---

# Output Files

A generated dataset can contain the following structure:

```text
geom328_dataset/
│
├── images/
│   ├── 000000.png
│   ├── 000001.png
│   └── ...
│
├── svg/
│   ├── 000000.svg
│   ├── 000001.svg
│   └── ...
│
├── scenes/
│   ├── 000000.json
│   ├── 000001.json
│   └── ...
│
├── metadata/
│   └── metadata.csv
│
├── train.csv
├── val.csv
├── test.csv
├── dataset_info.txt
└── split_info.txt
```

Depending on the configuration, some files or directories may not be generated.

---

# SVG and PNG Generation

Scenes are rendered as SVG.

When PNG output is enabled, the SVG representation is converted to PNG.

The generation process is:

```text
Scene
  │
  ▼
SVG Rendering
  │
  ├──────────────► SVG file
  │
  ▼
SVG → PNG Conversion
  │
  ▼
PNG file
```

When SVG output is disabled but PNG output is enabled, a temporary SVG file is used internally and removed afterward.

---

# Scene Files

When scene saving is enabled, each scene is stored as a JSON file.

A scene contains:

- class ID
- image name
- object shape
- object position
- logical object size
- rotation angle

Example:

```json
{
    "class": 0,
    "image_name": "000000.png",
    "objects": [
        {
            "shape": "triangle",
            "x": 100,
            "y": 120,
            "size": 5.3,
            "angle": 42.0
        }
    ]
}
```

---

# Metadata

Metadata is stored in:

```text
metadata/metadata.csv
```

Each row corresponds to one generated image.

The metadata includes:

```text
image_id
image_name
class
```

followed by the extracted concept values.

The concepts describe shape presence, largest shape, and spatial relations.

---

# Dataset Splitting

Train, validation, and test splitting is enabled by default.

The default split ratios are:

```text
Train:       70%
Validation:  15%
Test:        15%
```

The ratios can be configured:
```bash
generate_geom --train-ratio 0.70 --val-ratio 0.15 --test-ratio 0.15
```
Using Python:

```python
generate_dataset(
    train_ratio=0.70,
    val_ratio=0.15,
    test_ratio=0.15,
)
```

The split ratios must sum to 1.

Splitting can be disabled:
```bash
generate_geom --no-split
```
Using Python:
```python
generate_dataset(
    split=False,
)
```
The dataset split uses the generation seed.

---
# Examples

## Generate 50 samples from three classes

```bash
generate_geom \
    --classes 0 5 7 \
    --samples-per-class 50
```

---

## Generate all 28 classes

```bash
generate_geom \
    --classes all \
    --samples-per-class 100
```

---

## Generate a reproducible dataset

```bash
generate_geom \
    --classes 0 5 7 \
    --samples-per-class 50 \
    --seed 123
```

---

## Generate 128×128 images

```bash
generate_geom \
    --classes 0 5 7 \
    --samples-per-class 50 \
    --image-size 128
```

---

## Generate exactly four objects per scene

```bash
generate_geom \
    --classes 0 5 7 \
    --samples-per-class 50 \
    --min-objects 4 \
    --max-objects 4
```

---

## Disable validation

```bash
generate_geom \
    --classes 0 5 7 \
    --samples-per-class 50 \
    --no-validation
```

---

## Disable dataset splitting

```bash
generate_geom \
    --classes 0 5 7 \
    --samples-per-class 50 \
    --no-split
```

---

## Generate only PNG files

```python
generate_dataset(
    classes=[0, 5, 7],
    samples_per_class=50,
    save_png=True,
    save_svg=False,
)
```

---

## Generate only SVG files

```python
generate_dataset(
    classes=[0, 5, 7],
    samples_per_class=50,
    save_png=False,
    save_svg=True,
)
```

---

# Development

Clone the repository:

```bash
git clone https://github.com/paulovitor93/geom-3-28.git
cd geom-3-28
```

Install the package with development dependencies
```bash
pip install -e ".[dev]"
```
---

# Running the Tests

The project uses `pytest`.

Run the complete test suite:

```bash
pytest
```

The test suite covers:

- dataset generation
- public API
- configuration
- configuration validation
- scene generation
- reproducibility
- dataset splitting
- scene validation

---