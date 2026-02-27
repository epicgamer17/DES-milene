import pytest
from model.drs_model import DRSModel


@pytest.fixture
def drs_model():
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
    return model


def test_history_logging(drs_model):
    """
    Call advance_simulation once with a mock duration of 5.
    Assert that the history_time list contains [0.0, 5.0] and history_rate_config contains two identical entries.
    """
    drs_model.drs_DurationUntilThresholdCrossing = 5.0
    drs_model.drs_RateConfigurationNumber = 2  # Arbitrary config

    # Mock some ore levels to check history_ore_levels
    drs_model.OreStock_Level = 1000.0
    drs_model.Ore1Stock_Level = 600.0
    drs_model.Ore2Stock_Level = 400.0

    drs_model.advance_simulation()

    # history_time should contain [0.0, 5.0]
    assert drs_model.history_time == [0.0, 5.0]

    # history_rate_config should contain [2, 2]
    assert drs_model.history_rate_config == [2, 2]

    # history_ore_levels should contain [(1000.0, 600.0, 400.0), (1000.0, 600.0, 400.0)]
    # (Since rates were 0)
    expected_ore = (1000.0, 600.0, 400.0)
    assert drs_model.history_ore_levels == [expected_ore, expected_ore]

    assert drs_model.TNOW == 5.0
