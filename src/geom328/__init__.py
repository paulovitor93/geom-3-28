from .generator import RuleBasedSceneGenerator
from .renderer_svg import SceneRendererSVG
from .extractor import ConceptExtractor
from .dataset_builder import DatasetBuilder
from .config import GeomConfig

def generate_dataset(
    output_dir="geom328_dataset",
    classes=None,
    samples_per_class=100,
    seed=42,
    image_size=224,
    min_objects=3,
    max_objects=5,
    min_size=2.0,
    max_size=7.0,
    min_largest_size=5.0,
    min_size_difference=2.2,
    lambda_min=0.2,
    rotation=True,
):
    """
    Generate the Geom-3-28 synthetic dataset.

    Parameters
    ----------
    output_dir: str
        Directory where the dataset will be saved.

    classes: list[int] or None
        Class IDs to generate.
        If None or all, the 28 classes are generated.

    samples_per_class: int
        Number of images generated for each class.

    seed: int
        Random seed used for generation.

    image_size: int
        Image resolution.
    """

    config = GeomConfig(
        classes=classes,
        samples_per_class=samples_per_class,
        seed=seed,
        image_size=image_size,
        min_objects=min_objects,
        max_objects=max_objects,
        min_size=min_size,
        max_size=max_size,
        min_largest_size=min_largest_size,
        min_size_difference=min_size_difference,
        lambda_min=lambda_min,
        rotation=rotation,
    )

    generator = RuleBasedSceneGenerator(config=config,)

    available_classes = sorted(generator.specification.CLASS_SPECS.keys())

    if classes is None or classes == "all":
        selected_classes = available_classes
    else:
        selected_classes = list(classes)

        invalid_classes = set(selected_classes) - set(available_classes)

        if invalid_classes:
            raise ValueError(
                f"Unknown class IDs: {sorted(invalid_classes)}. "
                f"Available classes: {available_classes}"
            )

    renderer = SceneRendererSVG(image_size=config.image_size,)

    extractor = ConceptExtractor()

    builder = DatasetBuilder(
        generator=generator,
        renderer=renderer,
        extractor=extractor,
    )

    builder.build(
        output_dir=output_dir,
        samples_per_class=config.samples_per_class,
        generation_seed=config.seed,
        classes=selected_classes,
    )

__all__ = [
    "GeomConfig",
    "generate_dataset",
    "RuleBasedSceneGenerator",
]