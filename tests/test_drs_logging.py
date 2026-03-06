import pytest
import numpy as np
from model.drs_model import DRSModel


@pytest.fixture
def drs_model():
    model = DRSModel()
    model.initialize_simulation()
    return model


def test_data_logging_during_run(drs_model):
    """
    Test that the run() loop correctly logs state at initialization, before advance, and after update.
    """
    # Setup initial state for a single-step run
    drs_model.confExString_InitialRateConfigurationNumber = "1"
    drs_model.confExString_InitialLevelValue = ["0", "0", "1000", "500", "500"]
    drs_model.confExString_LevelRate[2][0] = "100"  # OreStock rate
    drs_model.confExString_LevelRate[3][0] = "50"  # Ore1Stock rate
    drs_model.confExString_LevelRate[4][0] = "50"  # Ore2Stock rate

    # Threshold: Timer 1 reaches 5
    drs_model.confExString_InitialTimerValue[0] = "0"
    drs_model.confExString_TimerRate[0][0] = "1"
    drs_model.confExString_UpperTimerThreshold[0][0] = "5"
    drs_model.confExString_TerminatingCondition = "drs_Timer(1) >= 5"

    # Act
    drs_model.run(max_iterations=1)

    # Assert
    # 1. Initial State (at initialization)
    # 2. Before Advance (at iteration start)
    # 3. After Update (at iteration end)
    assert len(drs_model.history_time) == 3

    # Initial state (TNOW=0)
    assert drs_model.history_time[0] == 0.0
    assert drs_model.history_ore_levels[0] == (1000.0, 500.0, 500.0)

    # Before advance (TNOW=0)
    assert drs_model.history_time[1] == 0.0

    # After update (TNOW=5)
    assert drs_model.history_time[2] == 5.0
    assert drs_model.history_ore_levels[2] == (1500.0, 750.0, 750.0)


def test_log_history_standalone():
    """
    Verify the log_history helper appends data correctly.
    """
    model = DRSModel()
    model.TNOW = 20.0
    model.drs_RateConfigurationNumber = 3
    model.OreStock_Level = 500
    model.Ore1Stock_Level = 250
    model.Ore2Stock_Level = 250

    model.log_history()

    assert model.history_time == [20.0]
    assert model.history_rate_config == [3]
    assert model.history_ore_levels == [(500.0, 250.0, 250.0)]
