from pathlib import Path
import pandas as pd
from tqdm import tqdm
import random
import numpy as np
import json
import resvg_py
import tempfile

class DatasetBuilder:
    def __init__(self, generator, renderer, extractor, config, validator=None,):
        self.generator = generator
        self.renderer = renderer
        self.extractor = extractor
        self.config = config
        self.validator = validator

    def build(
        self,
        output_dir,
        samples_per_class,
        generation_seed,
        classes=None,
        image_format="png",
    ):
        output_dir = Path(output_dir)

        random.seed(generation_seed)
        np.random.seed(generation_seed)

        images_dir = output_dir / "images"
        metadata_dir = output_dir / "metadata"
        scenes_dir = output_dir / "scenes"
        svg_dir = output_dir / "svg"

        if self.config.save_png:
            images_dir.mkdir(parents=True, exist_ok=True)

        if self.config.save_metadata:
            metadata_dir.mkdir(parents=True, exist_ok=True)

        if self.config.save_scenes:
            scenes_dir.mkdir(parents=True, exist_ok=True)

        if self.config.save_svg:
            svg_dir.mkdir(parents=True, exist_ok=True)

        rows = []

        image_id = 0

        available_classes = sorted(self.generator.specification.CLASS_SPECS.keys())

        if classes is None:
            classes = available_classes
        else:
            classes = list(classes)

            invalid_classes = set(classes) - set(available_classes)

            if invalid_classes:
                raise ValueError(
                    f"Unknown class IDs: {sorted(invalid_classes)}. "
                    f"Available classes: {available_classes}"
                )

        num_classes = len(classes)

        for class_id in classes:
            print(f"Generating class {class_id}")

            for _ in tqdm(range(samples_per_class)):

                scene = None

                if self.config.validate:

                    for attempt in range(self.config.validation_attempts):

                        candidate = self.generator.generate(class_id)

                        valid, predicted = self.validator.validate(
                            candidate,
                            expected_class=class_id,
                        )

                        if valid:
                            scene = candidate
                            break

                    if scene is None:
                        raise RuntimeError(
                            f"Unable to generate a valid scene for class "
                            f"{class_id} after "
                            f"{self.config.validation_attempts} attempts."
                        )

                else:

                    scene = self.generator.generate(class_id)

                image_name = f"{image_id:06d}.png"
                svg_name = f"{image_id:06d}.svg"
                scene_name = f"{image_id:06d}.json"

                if self.config.save_scenes:
                    self.save_scene(scene, class_id, image_name, scenes_dir / scene_name,)

                concepts = self.extractor.extract(scene)

                svg_path = svg_dir / svg_name
                png_path = images_dir / image_name


                if self.config.save_png or self.config.save_svg:

                    if self.config.save_svg:
                        svg_path = svg_dir / svg_name

                    else:
                        temporary_svg = output_dir / f".temporary_{image_id}.svg"
                        svg_path = temporary_svg

                    self.renderer.render(scene, svg_path,)

                    if self.config.save_png:

                        png_bytes = resvg_py.svg_to_bytes(
                            svg_path=str(svg_path),
                            width=self.renderer.image_size,
                            height=self.renderer.image_size,
                        )

                        with open(png_path, "wb") as f:
                            f.write(bytes(png_bytes))

                if not self.config.save_svg:
                    svg_path.unlink(missing_ok=True)

                row = {
                    "image_id": image_id,
                    "image_name": image_name,
                    "class": class_id,
                }

                row.update(concepts)
                rows.append(row)
                image_id += 1

        df = pd.DataFrame(rows)

        metadata_file = None

        if self.config.save_metadata:

            metadata_file = metadata_dir / "metadata.csv"

            df.to_csv(metadata_file, index=False,)

        info_file = output_dir / "dataset_info.txt"

        with open(info_file, "w") as f:

            f.write("Geom-3-28 Synthetic Dataset\n")
            f.write("===========================\n\n")

            f.write(f"Generation seed: {generation_seed}\n")
            f.write(f"Classes: {classes}\n")
            f.write(f"Number of classes: {num_classes}\n")
            f.write(f"Samples per class: {samples_per_class}\n")
            f.write(f"Total images: {len(df)}\n")

            f.write(f"Image size: {self.renderer.image_size} x {self.renderer.image_size}\n")

            f.write(f"Validation enabled: {self.config.validate}\n")

            if self.config.validate:
                f.write(
                    f"Validation attempts: "
                    f"{self.config.validation_attempts}\n"
                )

            f.write("\nGeneration parameters\n")
            f.write("---------------------\n")
            f.write(f"Min objects: {self.config.min_objects}\n")
            f.write(f"Max objects: {self.config.max_objects}\n")
            f.write(f"Min size: {self.config.min_size}\n")
            f.write(f"Max size: {self.config.max_size}\n")
            f.write(f"Min largest size: {self.config.min_largest_size}\n")
            f.write(f"Min size difference: {self.config.min_size_difference}\n")
            f.write(f"Lambda min: {self.config.lambda_min}\n")
            f.write(f"Rotation: {self.config.rotation}\n")

            f.write("\nOutput\n")
            f.write("------\n")
            f.write(f"PNG: {self.config.save_png}\n")
            f.write(f"SVG: {self.config.save_svg}\n")
            f.write(f"Scenes: {self.config.save_scenes}\n")
            f.write(f"Metadata: {self.config.save_metadata}\n")

        print()
        print(f"Generation seed: {generation_seed}")
        print(f"Dataset saved to: {output_dir}")
        print(f"Images : {len(df)}")
        print(f"Classes: {num_classes}")
        if metadata_file is not None:
            print(f"Metadata: {metadata_file}")

    def save_scene(self, scene, class_id, image_name, filepath):
        data = {
            "class": class_id,
            "image_name": image_name,
            "objects": []
        }

        for obj in scene:
            data["objects"].append({
                "shape": obj.shape,
                "x": obj.x,
                "y": obj.y,
                "size": obj.size,
                "angle": obj.angle,
            })

        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)