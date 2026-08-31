from geom328 import RuleBasedSceneGenerator

def test_all_classes_can_generate():
    generator = RuleBasedSceneGenerator()

    available_classes = sorted(generator.specification.CLASS_SPECS.keys())

    assert len(available_classes) == 28

    for class_id in available_classes:
        scene = generator.generate(class_id)

        assert scene is not None
        assert len(scene) > 0