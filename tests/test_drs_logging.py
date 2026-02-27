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


def test_history_logging():
    """
    Call advance_simulation once with a mock duration of 5.
    Assert that the history_time list contains [0.0, 5.0] and history_rate_config contains two identical entries.
    """
    model = DRSModel()
    # Initialize basic configurations to avoid evaluation errors
    model.confExString_LevelRate = [
        ["0"] * model.dim_NumberOfRateConfigurations
        for _ in range(model.dim_NumberOfLevels)
    ]
    model.confExString_TimerRate = [
        ["1"] * model.dim_NumberOfRateConfigurations
        for _ in range(model.dim_NumberOfTimers)
    ]
    model.confExString_LowerLevelAssignmentAddress = [
        ["0"] * model.dim_NumberOfRateConfigurations
        for _ in range(model.dim_NumberOfLevels)
    ]
    model.confExString_UpperLevelAssignmentAddress = [
        ["0"] * model.dim_NumberOfRateConfigurations
        for _ in range(model.dim_NumberOfLevels)
    ]
    model.confExString_LowerTimerAssignmentAddress = [
        ["0"] * model.dim_NumberOfRateConfigurations
        for _ in range(model.dim_NumberOfTimers)
    ]
    model.confExString_UpperTimerAssignmentAddress = [
        ["0"] * model.dim_NumberOfRateConfigurations
        for _ in range(model.dim_NumberOfTimers)
    ]

    model.drs_DurationUntilThresholdCrossing = 5.0
    model.drs_RateConfigurationNumber = 2  # Arbitrary config

    # Mock some ore levels to check history_ore_levels
    model.OreStock_Level = 1000.0
    model.Ore1Stock_Level = 600.0
    model.Ore2Stock_Level = 400.0

    model.advance_simulation()

    # history_time should contain [0.0, 5.0]
    assert model.history_time == [0.0, 5.0]

    # history_rate_config should contain [2, 2]
    assert model.history_rate_config == [2, 2]

    # history_ore_levels should contain [(1000.0, 600.0, 400.0), (1000.0, 600.0, 400.0)]
    # (Since rates were 0)
    expected_ore = (1000.0, 600.0, 400.0)
    assert model.history_ore_levels == [expected_ore, expected_ore]

    assert model.TNOW == 5.0
