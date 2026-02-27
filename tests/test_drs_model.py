import pytest
import numpy as np
from model.drs_model import DRSModel


@pytest.fixture
def model():
    """Fixture that yields a fresh instance of DRSModel for testing."""
    return DRSModel()


def test_default_dimensions(model):
    """Assert that the initial dimension values match the specification."""
    assert model.dim_NumberOfLevels == 5
    assert model.dim_NumberOfTimers == 9
    assert model.dim_NumberOfDiscretelyDynamicalNumericalVariables == 3
    assert model.dim_NumberOfCategoricalVariables == 1
    assert model.dim_NumberOfRateConfigurations == 7
    assert model.dim_NumberOfAssignmentSequenceAddresses == 6
    assert model.dim_MaxLengthOfAssignmentSequence == 7


def test_state_array_shapes(model):
    """Assert that the shape of state tracking vectors match dimensions."""
    assert model.drs_Level.shape == (5,)
    assert model.drs_Timer.shape == (9,)
    assert model.drs_DiscretelyDynamicalNumericalVariable.shape == (3,)
    assert len(model.drs_CategoricalVariable) == 1


def test_variable_aliases_mutation(model):
    """Verify that property setters correctly mutate underlying memory."""
    # Set model.Ore1Stock_Level = 5000.0. Assert that model.drs_Level[3] == 5000.0.
    model.Ore1Stock_Level = 5000.0
    assert model.drs_Level[3] == 5000.0
    assert model.Ore1Stock_Level == 5000.0

    # Set model.drs_Timer[8] = 24.5. Assert that model.TimeInShutdown_Timer == 24.5.
    model.drs_Timer[8] = 24.5
    assert model.TimeInShutdown_Timer == 24.5
    assert model.drs_Timer[8] == 24.5


def test_array_persistence(model):
    """Ensure that setting an alias modifies the element within the array, not re-assigning."""
    original_level_array = model.drs_Level
    original_timer_array = model.drs_Timer

    # Modify via alias
    model.OreStock_Level = 123.4
    model.TimeInShutdown_Timer = 56.7

    # Assert that the underlying array is still the same object (reference persistence)
    assert model.drs_Level is original_level_array
    assert model.drs_Timer is original_timer_array

    # Assert that the value was indeed changed in the original array
    assert original_level_array[2] == 123.4
    assert original_timer_array[8] == 56.7


def test_matrix_initialization(model):
    """Verify that confExString_LevelRate is initialized correctly."""
    assert isinstance(model.confExString_LevelRate, list)
    assert len(model.confExString_LevelRate) == model.dim_NumberOfLevels
    assert all(isinstance(row, list) for row in model.confExString_LevelRate)
    assert len(model.confExString_LevelRate[0]) == model.dim_NumberOfRateConfigurations


def test_load_configuration(model):
    """Verify that load_configuration correctly assigns data."""
    mock_matrix = [["1.0"] * 7 for _ in range(5)]
    mock_data = {"confExString_LevelRate": mock_matrix}
    model.load_configuration(mock_data)
    assert model.confExString_LevelRate == mock_matrix


def test_evaluate_basic_math(model):
    """Verify basic math expression evaluation."""
    assert model.evaluate_expression("5 + 5") == 10.0
    assert model.evaluate_expression("10 * 2.5") == 25.0


def test_evaluate_arena_functions(model):
    """Verify Arena function translations (MN, MX)."""
    assert model.evaluate_expression("MN(10, 5)") == 5.0
    assert model.evaluate_expression("MX(10, 5)") == 10.0


def test_evaluate_state_variables(model):
    """Verify translation of 1-based Arena state variables to 0-based indexing."""
    model.drs_Level[0] = 50.0
    assert model.evaluate_expression("drs_Level(1) * 2") == 100.0
