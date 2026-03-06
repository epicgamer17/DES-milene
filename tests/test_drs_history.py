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
    Test the log_history method directly.
    """
    drs_model.TNOW = 5.0
    drs_model.drs_RateConfigurationNumber = 2
    drs_model.OreStock_Level = 1000.0
    drs_model.Ore1Stock_Level = 600.0
    drs_model.Ore2Stock_Level = 400.0

    drs_model.log_history()

    assert drs_model.history_time == [5.0]
    assert drs_model.history_rate_config == [2]
    assert drs_model.history_ore_levels == [(1000.0, 600.0, 400.0)]

    assert drs_model.TNOW == 5.0
