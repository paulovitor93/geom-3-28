import argparse

from . import generate_dataset

def main():
    parser = argparse.ArgumentParser(description="Generate the Geom-3-28 synthetic dataset.")

    # Dataset
    # --------------------------------------------------
    parser.add_argument("--output-dir", default="geom328_dataset", help="Output directory.",)

    parser.add_argument("--classes", nargs="+", default=None, help="Class IDs to generate, or 'all'.",)

    parser.add_argument("--samples-per-class", type=int, default=100, help="Number of samples per class.",)

    parser.add_argument("--seed", type=int, default=None, help="Random seed. If omitted, a random seed is generated.",)

    # Image
    # --------------------------------------------------
    parser.add_argument("--image-size", type=int, default=224, help="Image resolution.",)

    # Objects
    # --------------------------------------------------
    parser.add_argument("--min-objects", type=int, default=3, help="Minimum number of objects.",)

    parser.add_argument("--max-objects", type=int, default=5, help="Maximum number of objects.",)

    # Size
    # --------------------------------------------------
    parser.add_argument("--min-size", type=float, default=2.0, help="Minimum logical object size.",)

    parser.add_argument("--max-size", type=float, default=7.0, help="Maximum logical object size.",)

    parser.add_argument("--min-largest-size", type=float, default=5.0, help="Minimum size of the largest object.",)

    parser.add_argument("--min-size-difference", type=float, default=2.2, help="Minimum size difference between largest and smaller objects.",)

    # Spatial
    # --------------------------------------------------
    parser.add_argument("--lambda-min", type=float, default=0.2, help="Minimum normalized distance between objects.",)

    # Rendering
    # --------------------------------------------------
    parser.add_argument("--no-rotation", action="store_true", help="Disable object rotation.",)

    # Validation
    # --------------------------------------------------
    parser.add_argument("--no-validation", action="store_true", help="Disable scene validation.",)

    parser.add_argument("--validation-attempts", type=int, default=100, help="Maximum attempts to generate a valid scene.",)

    # Split
    # --------------------------------------------------
    parser.add_argument("--no-split", action="store_true", help="Do not create train/validation/test splits.",)

    parser.add_argument("--train-ratio", type=float, default=0.70, help="Training split ratio.",)

    parser.add_argument("--val-ratio", type=float, default=0.15, help="Validation split ratio.",)

    parser.add_argument("--test-ratio", type=float, default=0.15, help="Test split ratio.",)

    args = parser.parse_args()

    # Classes
    # --------------------------------------------------
    if args.classes is None:
        classes = None

    elif len(args.classes) == 1 and args.classes[0].lower() == "all":
        classes = "all"

    else:
        try:
            classes = [int(class_id) for class_id in args.classes]
        except ValueError:
            parser.error("--classes must contain integer class IDs or 'all'.")

    # Generate
    # --------------------------------------------------
    generate_dataset(
        output_dir=args.output_dir,
        classes=classes,
        samples_per_class=args.samples_per_class,
        seed=args.seed,

        image_size=args.image_size,

        min_objects=args.min_objects,
        max_objects=args.max_objects,

        min_size=args.min_size,
        max_size=args.max_size,
        min_largest_size=args.min_largest_size,
        min_size_difference=args.min_size_difference,

        lambda_min=args.lambda_min,

        rotation=not args.no_rotation,

        validate=not args.no_validation,
        validation_attempts=args.validation_attempts,

        split=not args.no_split,
        train_ratio=args.train_ratio,
        val_ratio=args.val_ratio,
        test_ratio=args.test_ratio,
    )


if __name__ == "__main__":
    main()