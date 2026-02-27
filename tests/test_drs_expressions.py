import pytest
from model.drs_model import DRSModel


@pytest.fixture
def model():
    return DRSModel()


def test_evaluate_basic_arithmetic(model):
    assert model.evaluate_expression("1 + 1") == 2.0
    assert model.evaluate_expression("10 * 2.5") == 25.0
    assert model.evaluate_expression("10 / 4") == 2.5


def test_evaluate_empty_or_zero(model):
    assert model.evaluate_expression("") == 0.0
    assert model.evaluate_expression("0") == 0.0
    assert model.evaluate_expression("  0  ") == 0.0


def test_evaluate_eval_wrapper(model):
    assert model.evaluate_expression("Eval(10 + 5)") == 15.0
    assert model.evaluate_expression("eval(20 / 2)") == 10.0


def test_evaluate_min_max(model):
    assert model.evaluate_expression("MN(10, 20)") == 10.0
    assert model.evaluate_expression("MX(10, 20)") == 20.0
    assert model.evaluate_expression("min(5, 15)") == 5.0
    assert model.evaluate_expression("max(5, 15)") == 15.0


def test_evaluate_drs_level_indexing(model):
    model.drs_Level[0] = 10.5
    model.drs_Level[4] = 99.9
    assert model.evaluate_expression("drs_Level(1)") == 10.5
    assert model.evaluate_expression("drs_Level(5)") == 99.9
    assert model.evaluate_expression("drs_Level(1) + drs_Level(5)") == 110.4


def test_evaluate_drs_timer_indexing(model):
    model.drs_Timer[0] = 5.0
    model.drs_Timer[8] = 123.4
    assert model.evaluate_expression("drs_Timer(1)") == 5.0
    assert model.evaluate_expression("drs_Timer(9)") == 123.4


def test_evaluate_complex_expression(model):
    # Eval(confExString_LevelRate(1,drs_RateConfigurationNumber))
    # Note: the example had confExString_LevelRate which is a list de-referenced.
    # But in the request it said: Use Regular Expressions to find patterns like drs_Level(X) or drs_Timer(Y)
    # The Eval(confExString_LevelRate(1,drs_RateConfigurationNumber)) might be trickier if confExString_LevelRate
    # is supposed to be accessed via [1, drs_RateConfigurationNumber].
    # Wait, the example: "Eval(confExString_LevelRate(1,drs_RateConfigurationNumber))"
    # If confExString_LevelRate is an attribute on the model, it needs to be in the namespace if we want to evaluate it.
    # However, the instructions ONLY mentioned drs_Level, drs_Timer, drs_RateConfigurationNumber, min/max/MN/MX.
    # Let's re-read the objective.
    # "Context: The simulation evaluates strings like "Eval(confExString_LevelRate(1,drs_RateConfigurationNumber))"..."
    # "Crucial Step: Use Regular Expressions to find patterns like drs_Level(X) or drs_Timer(Y) and replace them with drs_Level[X-1] and drs_Timer[Y-1]"
    # It DID NOT mention adding confExString_* matrices to the namespace.
    # If the user wants to evaluate strings that reference those matrices, they should have been in the namespace.
    # I'll stick to the requested namespace for now and see if I need to expand it.

    model.drs_Level[0] = 100
    model.drs_RateConfigurationNumber = 2
    assert model.evaluate_expression("MN(drs_Level(1), 50)") == 50.0
    assert model.evaluate_expression("MX(drs_Level(1), 150)") == 150.0


def test_evaluate_error_handling(model):
    with pytest.raises(ValueError):
        model.evaluate_expression("invalid syntax")
    with pytest.raises(ValueError):
        model.evaluate_expression("drs_Level(100)")  # Out of bounds
