import pytest
import numpy as np
from model.drs_model import DRSModel


@pytest.fixture
def drs_model():
    return DRSModel()


def test_characterize_thresholds_level_drop(drs_model):
    """
    Set Level 0 to 100, Rate to -10, Lower Threshold to 20.
    Assert duration is calculated as 8.0 days, CrossedByTimer is 0, Direction is -1.
    """
    drs_model.drs_Level[0] = 100.0
    drs_model.drs_RateConfigurationNumber = 1
    drs_model.confExString_LevelRate[0][0] = "-10"
    drs_model.confExString_LowerLevelThreshold[0][0] = "20"

    # We need to make sure other levels/timers don't interfere
    # By default rates are 0, so they shouldn't interfere.

    drs_model.characterize_thresholds()

    assert drs_model.drs_DurationUntilThresholdCrossing == pytest.approx(8.0)
    assert drs_model.drs_ThresholdCrossingLevelOrTimerNumber == 0
    assert drs_model.drs_ThresholdIsCrossedByTimer == 0
    assert drs_model.drs_DirectionOfThresholdCrossing == -1


def test_characterize_thresholds_timer_rise(drs_model):
    """
    Set Timer 1 to 0, Rate to 1, Upper Threshold to 24. Assert duration is 24.0.
    """
    drs_model.drs_Timer[1] = 0.0
    drs_model.drs_RateConfigurationNumber = 1
    drs_model.confExString_TimerRate[1][0] = "1"
    drs_model.confExString_UpperTimerThreshold[1][0] = "24"

    drs_model.characterize_thresholds()

    assert drs_model.drs_DurationUntilThresholdCrossing == pytest.approx(24.0)
    assert drs_model.drs_ThresholdCrossingLevelOrTimerNumber == 1
    assert drs_model.drs_ThresholdIsCrossedByTimer == 1
    assert drs_model.drs_DirectionOfThresholdCrossing == 1


def test_characterize_thresholds_multiple_events(drs_model):
    """
    Check if it correctly finds the minimum duration among multiple events.
    """
    # Event 1: Level 0 crosses in 10 units
    drs_model.drs_Level[0] = 50.0
    drs_model.confExString_LevelRate[0][0] = "5"
    drs_model.confExString_UpperLevelThreshold[0][0] = "100"  # (100-50)/5 = 10

    # Event 2: Timer 2 crosses in 5 units
    drs_model.drs_Timer[2] = 0.0
    drs_model.confExString_TimerRate[2][0] = "2"
    drs_model.confExString_UpperTimerThreshold[2][0] = "10"  # (10-0)/2 = 5

    drs_model.characterize_thresholds()

    assert drs_model.drs_DurationUntilThresholdCrossing == pytest.approx(5.0)
    assert drs_model.drs_ThresholdCrossingLevelOrTimerNumber == 2
    assert drs_model.drs_ThresholdIsCrossedByTimer == 1
    assert drs_model.drs_DirectionOfThresholdCrossing == 1
