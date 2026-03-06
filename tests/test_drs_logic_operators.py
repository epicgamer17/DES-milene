import pytest
from model.drs_model import DRSModel


@pytest.fixture
def model():
    return DRSModel()


def test_evaluate_logical_and(model):
    assert model.evaluate_expression("1 && 1") == 1.0
    assert model.evaluate_expression("1 && 0") == 0.0
    assert model.evaluate_expression("0 && 0") == 0.0


def test_evaluate_logical_or(model):
    assert model.evaluate_expression("1 || 1") == 1.0
    assert model.evaluate_expression("1 || 0") == 1.0
    assert model.evaluate_expression("0 || 1") == 1.0
    assert model.evaluate_expression("0 || 0") == 0.0


def test_evaluate_combined_logic(model):
    assert model.evaluate_expression("(1 || 0) && 1") == 1.0
    assert model.evaluate_expression("(1 || 0) && 0") == 0.0
    assert model.evaluate_expression("(0 && 1) || 1") == 1.0


def test_evaluate_logic_with_levels(model):
    model.drs_Level[0] = 100
    model.drs_Level[1] = 20
    assert model.evaluate_expression("drs_Level(1) > 50 && drs_Level(2) < 50") == 1.0
    assert model.evaluate_expression("drs_Level(1) < 50 || drs_Level(2) < 50") == 1.0
    assert model.evaluate_expression("drs_Level(1) < 50 || drs_Level(2) > 50") == 0.0
