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
