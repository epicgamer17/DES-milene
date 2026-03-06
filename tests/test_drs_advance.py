import pytest
import numpy as np
from model.drs_model import DRSModel


@pytest.fixture
def drs_model():
    return DRSModel()


def test_advance_simulation(drs_model):
    """
    Unit Test: Set TNOW = 0, duration to 5, Level 0 to 50, Level 0 rate to 2.
    Run advance. Assert TNOW == 5, Level 0 == 60, and TimeOfPreviousDRSUpdate == 5.
    """
    drs_model.TNOW = 0.0
    drs_model.drs_DurationUntilThresholdCrossing = 5.0
    drs_model.drs_Level[0] = 50.0
    drs_model.drs_RateConfigurationNumber = 1
    drs_model.confExString_LevelRate[0][0] = "2"

    # We also need to set some crossing info to test assignment address calculation
    # Let's say Level 0 crossed upper threshold at rate config 0
    drs_model.drs_ThresholdCrossingLevelOrTimerNumber = 0
    drs_model.drs_ThresholdIsCrossedByTimer = 0
    drs_model.drs_DirectionOfThresholdCrossing = 1
    drs_model.confExString_UpperLevelAssignmentAddress[0][0] = "123"

    drs_model.advance_simulation()

    assert drs_model.TNOW == 5.0
    assert drs_model.drs_Level[0] == 60.0
    assert drs_model.drs_TimeOfPreviousDRSUpdate == 5.0
    assert drs_model.current_assignment_address == 123


def test_advance_simulation_timer(drs_model):
    """
    Test timers updating during advance.
    """
    drs_model.TNOW = 10.0
    drs_model.drs_DurationUntilThresholdCrossing = 2.0
    drs_model.drs_Timer[1] = 5.0
    drs_model.drs_RateConfigurationNumber = 1
    drs_model.confExString_TimerRate[1][0] = "1"

    # Timer crossing info
    drs_model.drs_ThresholdCrossingLevelOrTimerNumber = 1
    drs_model.drs_ThresholdIsCrossedByTimer = 1
    drs_model.drs_DirectionOfThresholdCrossing = 1
    drs_model.confExString_UpperTimerAssignmentAddress[1][0] = "456"

    drs_model.advance_simulation()

    assert drs_model.TNOW == 12.0
    assert drs_model.drs_Timer[1] == 7.0
    assert drs_model.drs_TimeOfPreviousDRSUpdate == 12.0
    assert drs_model.current_assignment_address == 456
