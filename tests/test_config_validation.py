import pytest
from geom328.config import GeomConfig

def test_min_objects_must_be_positive():
    with pytest.raises(ValueError, match="min_objects"):
        GeomConfig(min_objects=0)

def test_max_objects_cannot_be_less_than_min_objects():
    with pytest.raises(ValueError, match="max_objects"):
        GeomConfig(min_objects=5, max_objects=3,)

def test_min_size_must_be_positive():
    with pytest.raises(ValueError, match="min_size"):
        GeomConfig(min_size=0)

def test_max_size_must_be_greater_than_min_size():
    with pytest.raises(ValueError, match="max_size"):
        GeomConfig(min_size=5.0, max_size=5.0,)

def test_min_largest_size_cannot_exceed_max_size():
    with pytest.raises(ValueError, match="min_largest_size"):
        GeomConfig(min_largest_size=8.0, max_size=7.0,)

def test_min_size_difference_must_be_positive():
    with pytest.raises(ValueError, match="min_size_difference"):
        GeomConfig(min_size_difference=0)

def test_size_configuration_must_be_feasible():
    with pytest.raises(ValueError, match="min_size \\+ min_size_difference",):
        GeomConfig(min_size=3.0, max_size=5.0, min_size_difference=2.2,)

def test_lambda_min_must_be_valid():
    with pytest.raises(ValueError, match="lambda_min"):
        GeomConfig(lambda_min=-0.1)

    with pytest.raises(ValueError, match="lambda_min"):
        GeomConfig(lambda_min=1.1)

def test_split_ratios_must_be_non_negative():
    with pytest.raises(ValueError, match="train_ratio"):
        GeomConfig(train_ratio=-0.1)

    with pytest.raises(ValueError, match="val_ratio"):
        GeomConfig(val_ratio=-0.1)

    with pytest.raises(ValueError, match="test_ratio"):
        GeomConfig(test_ratio=-0.1)

def test_split_ratios_must_sum_to_one():
    with pytest.raises(ValueError, match="train_ratio.*val_ratio.*test_ratio",):
        GeomConfig(train_ratio=0.5, val_ratio=0.2, test_ratio=0.2,)

def test_validation_attempts_must_be_positive():
    with pytest.raises(ValueError, match="validation_attempts"):
        GeomConfig(validation_attempts=0)