from pathlib import Path
import random
from .generator import RuleBasedSceneGenerator
from .renderer_svg import SceneRendererSVG
from .extractor import ConceptExtractor
from .dataset_builder import DatasetBuilder
from .config import GeomConfig
from .split import DatasetSplitter
from .validator import SceneValidator
from .classifier import RuleBasedClassifier

def generate_dataset(
    output_dir="geom328_dataset",
    classes=None,
    samples_per_class=100,
    seed=None,
    image_size=224,
    min_objects=3,
    max_objects=5,
    min_size=2.0,
    max_size=7.0,
    min_largest_size=5.0,
    min_size_difference=2.2,
    lambda_min=0.2,
    rotation=True,
    save_png=True,
    save_svg=True,
    save_scenes=True,
    save_metadata=True,
    validate=True,
    validation_attempts=100,
    split=True,
    train_ratio=0.70,
    val_ratio=0.15,
    test_ratio=0.15,
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
    output_dir = Path(output_dir)

    if seed is None:
        seed = random.SystemRandom().randint(0, 2**32 - 1)

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

        save_png=save_png,
        save_svg=save_svg,
        save_scenes=save_scenes,
        save_metadata=save_metadata,

        validate=validate,
        validation_attempts=validation_attempts,

        split=split,
        train_ratio=train_ratio,
        val_ratio=val_ratio,
        test_ratio=test_ratio,
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

    classifier = RuleBasedClassifier(generator.specification)

    validator = SceneValidator(extractor=extractor, classifier=classifier,)

    builder = DatasetBuilder(
        generator=generator,
        renderer=renderer,
        extractor=extractor,
        config=config,
        validator=validator,
    )

    builder.build(
        output_dir=output_dir,
        samples_per_class=config.samples_per_class,
        generation_seed=config.seed,
        classes=selected_classes,
    )

    if config.split:

        if not config.save_metadata:
            raise ValueError("split=True requires save_metadata=True.")

        splitter = DatasetSplitter(seed=config.seed)

        splitter.split(
            metadata_csv=output_dir / "metadata" / "metadata.csv",
            output_dir=output_dir,
            train_ratio=config.train_ratio,
            val_ratio=config.val_ratio,
            test_ratio=config.test_ratio,
        )

__all__ = [
    "GeomConfig",
    "generate_dataset",
    "RuleBasedSceneGenerator",
    "RuleBasedClassifier",
]