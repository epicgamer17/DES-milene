import pytest
import numpy as np
from model.drs_model import DRSModel, OutputStatistics


def test_calculate_statistics_basic():
    model = DRSModel()

    # Manually set timer values (aliases)
    model.TimeInModeA_Timer = 10.0
    model.TimeInModeAContingency_Timer = 5.0
    model.TimeInModeAMineSurging_Timer = 2.0
    model.TimeInModeB_Timer = 8.0
    model.TimeInModeBContingency_Timer = 4.0
    model.TimeInModeBMineSurging_Timer = 1.0
    model.TimeInShutdown_Timer = 10.0

    # total_time = 10 + 5 + 2 + 8 + 4 + 1 + 10 = 40.0
    # active_time = 40 - 10 = 30.0

    # Set levels for throughput
    model.OreExtraction_Level = 1000000.0  # 1,000,000
    model.parameter_OreToBeExtractedDuringWarmingPeriod = 600000.0  # 600,000
    # Throughput = (1,000,000 - 600,000) / 30 = 400,000 / 30 = 13333.333...

    stats = model.calculate_statistics()

    assert isinstance(stats, OutputStatistics)
    assert stats.total_time == 40.0
    assert stats.active_time == 30.0
    assert stats.PortionOfTimeInModeA == 10.0 / 40.0
    assert pytest.approx(stats.Throughput) == 400000.0 / 30.0
    assert stats.PortionOfTimeInShutdown == 10.0 / 40.0


def test_calculate_statistics_zero_total_time():
    model = DRSModel()
    # Timers are 0 by default
    stats = model.calculate_statistics()

    assert stats.total_time == 0.0
    assert stats.active_time == 0.0
    assert stats.PortionOfTimeInModeA == 0.0
    assert stats.Throughput == 0.0


def test_calculate_statistics_zero_active_time():
    model = DRSModel()
    model.TimeInShutdown_Timer = 10.0
    # Other timers are 0
    # total_time = 10, active_time = 0

    stats = model.calculate_statistics()

    assert stats.total_time == 10.0
    assert stats.active_time == 0.0
    assert stats.Throughput == 0.0
    assert stats.PortionOfTimeInShutdown == 1.0
