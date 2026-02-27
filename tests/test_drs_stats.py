import pytest
import numpy as np
from model.drs_model import DRSModel, OutputStatistics


@pytest.fixture
def drs_model():
    return DRSModel()


def test_calculate_statistics_normal(drs_model):
    """
    Manually set the timer aliases to simple values (e.g., all set to 10.0).
    Assert that all "Portion" statistics equal 1/7 and Throughput is calculated correctly.
    """
    # Set all 7 mode timers to 10.0
    drs_model.TimeInModeA_Timer = 10.0
    drs_model.TimeInModeAContingency_Timer = 10.0
    drs_model.TimeInModeAMineSurging_Timer = 10.0
    drs_model.TimeInModeB_Timer = 10.0
    drs_model.TimeInModeBContingency_Timer = 10.0
    drs_model.TimeInModeBMineSurging_Timer = 10.0
    drs_model.TimeInShutdown_Timer = 10.0

    # Set OreExtraction_Level and parameter_OreToBeExtractedDuringWarmingPeriod
    drs_model.OreExtraction_Level = 700000.0
    drs_model.parameter_OreToBeExtractedDuringWarmingPeriod = 600000.0

    stats = drs_model.calculate_statistics()

    # Denominators
    # total_time = 70.0
    # active_time = 60.0
    assert stats.total_time == 70.0
    assert stats.active_time == 60.0

    # Portions should be 10.0 / 70.0 = 1/7
    expected_portion = 1.0 / 7.0
    assert pytest.approx(stats.PortionOfTimeInModeA) == expected_portion
    assert pytest.approx(stats.PortionOfTimeInModeAContingency) == expected_portion
    assert pytest.approx(stats.PortionOfTimeInModeAMineSurging) == expected_portion
    assert pytest.approx(stats.PortionOfTimeInModeB) == expected_portion
    assert pytest.approx(stats.PortionOfTimeInModeBContingency) == expected_portion
    assert pytest.approx(stats.PortionOfTimeInModeBMineSurging) == expected_portion
    assert pytest.approx(stats.PortionOfTimeInShutdown) == expected_portion

    # Throughput calculation
    # (700000 - 600000) / 60.0 = 100000 / 60.0 = 1666.666...
    expected_throughput = 100000.0 / 60.0
    assert pytest.approx(stats.Throughput) == expected_throughput


def test_calculate_statistics_zero_time(drs_model):
    """
    Ensure that calling calculate_statistics immediately after initialization
    (when all timers are 0) does not throw a ZeroDivisionError and returns 0.0 for all fields.
    """
    stats = drs_model.calculate_statistics()

    assert stats.total_time == 0.0
    assert stats.active_time == 0.0
    assert stats.PortionOfTimeInModeA == 0.0
    assert stats.PortionOfTimeInModeAContingency == 0.0
    assert stats.PortionOfTimeInModeAMineSurging == 0.0
    assert stats.PortionOfTimeInModeB == 0.0
    assert stats.PortionOfTimeInModeBContingency == 0.0
    assert stats.PortionOfTimeInModeBMineSurging == 0.0
    assert stats.PortionOfTimeInShutdown == 0.0
    assert stats.Throughput == 0.0
