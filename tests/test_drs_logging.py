import pytest
import numpy as np
from model.drs_model import DRSModel


@pytest.fixture
def drs_model():
    model = DRSModel()
    model.initialize_simulation()
    return model


def test_data_logging_during_advance(drs_model):
    """
    Test that advance_simulation correctly logs state before and after updates.
    """
    # Setup initial state
    drs_model.TNOW = 10.0
    drs_model.OreStock_Level = 1000.0
    drs_model.Ore1Stock_Level = 500.0
    drs_model.Ore2Stock_Level = 500.0
    drs_model.drs_RateConfigurationNumber = 1

    # Mock duration and rates
    drs_model.drs_DurationUntilThresholdCrossing = 5.0
    drs_model.confExString_LevelRate[2][1] = "100"  # OreStock rate
    drs_model.confExString_LevelRate[3][1] = "50"  # Ore1Stock rate
    drs_model.confExString_LevelRate[4][1] = "50"  # Ore2Stock rate

    # Mock threshold crossing to avoid address evaluation errors if any
    drs_model.drs_ThresholdCrossingLevelOrTimerNumber = 0
    drs_model.drs_ThresholdIsCrossedByTimer = 0
    drs_model.drs_DirectionOfThresholdCrossing = 1
    drs_model.confExString_UpperLevelAssignmentAddress[0][1] = "0"

    # Verify history is initially empty (or contains initialization if we added it there,
    # but my implementation only appends in advance_simulation)
    assert len(drs_model.history_time) == 0

    # Act
    drs_model.advance_simulation()

    # Assert
    # Should have 2 entries: before and after
    assert len(drs_model.history_time) == 2
    assert len(drs_model.history_rate_config) == 2
    assert len(drs_model.history_ore_levels) == 2

    # Before state
    assert drs_model.history_time[0] == 10.0
    assert drs_model.history_rate_config[0] == 1
    assert drs_model.history_ore_levels[0] == (1000.0, 500.0, 500.0)

    # After state
    assert drs_model.history_time[1] == 15.0
    assert drs_model.history_rate_config[1] == 1
    assert drs_model.history_ore_levels[1] == (1500.0, 750.0, 750.0)
