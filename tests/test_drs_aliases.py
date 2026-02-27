import numpy as np
import pytest
from model.drs_model import DRSModel


def test_level_aliases():
    model = DRSModel()

    # Test OreExtraction_Level
    model.OreExtraction_Level = 10.5
    assert model.drs_Level[0] == 10.5
    assert model.OreExtraction_Level == 10.5

    # Test OreExtractedFromCurrentParcel_Level
    model.OreExtractedFromCurrentParcel_Level = 5.2
    assert model.drs_Level[1] == 5.2
    assert model.OreExtractedFromCurrentParcel_Level == 5.2

    # Test OreStock_Level
    model.OreStock_Level = 100.0
    assert model.drs_Level[2] == 100.0
    assert model.OreStock_Level == 100.0

    # Test Ore1Stock_Level
    model.Ore1Stock_Level = 40.0
    assert model.drs_Level[3] == 40.0
    assert model.Ore1Stock_Level == 40.0

    # Test Ore2Stock_Level
    model.Ore2Stock_Level = 60.0
    assert model.drs_Level[4] == 60.0
    assert model.Ore2Stock_Level == 60.0


def test_timer_aliases():
    model = DRSModel()

    # Test TimeExecutedInCurrentCampaignOrShutdown_Timer
    model.TimeExecutedInCurrentCampaignOrShutdown_Timer = 1.0
    assert model.drs_Timer[0] == 1.0
    assert model.TimeExecutedInCurrentCampaignOrShutdown_Timer == 1.0

    # Test TimeExecutedInCurrentContingencySegment_Timer
    model.TimeExecutedInCurrentContingencySegment_Timer = 2.0
    assert model.drs_Timer[1] == 2.0
    assert model.TimeExecutedInCurrentContingencySegment_Timer == 2.0

    # Test TimeInModeA_Timer
    model.TimeInModeA_Timer = 3.0
    assert model.drs_Timer[2] == 3.0
    assert model.TimeInModeA_Timer == 3.0

    # Test TimeInModeAContingency_Timer
    model.TimeInModeAContingency_Timer = 4.0
    assert model.drs_Timer[3] == 4.0
    assert model.TimeInModeAContingency_Timer == 4.0

    # Test TimeInModeAMineSurging_Timer
    model.TimeInModeAMineSurging_Timer = 5.0
    assert model.drs_Timer[4] == 5.0
    assert model.TimeInModeAMineSurging_Timer == 5.0

    # Test TimeInModeB_Timer
    model.TimeInModeB_Timer = 6.0
    assert model.drs_Timer[5] == 6.0
    assert model.TimeInModeB_Timer == 6.0

    # Test TimeInModeBContingency_Timer
    model.TimeInModeBContingency_Timer = 7.0
    assert model.drs_Timer[6] == 7.0
    assert model.TimeInModeBContingency_Timer == 7.0

    # Test TimeInModeBMineSurging_Timer
    model.TimeInModeBMineSurging_Timer = 8.0
    assert model.drs_Timer[7] == 8.0
    assert model.TimeInModeBMineSurging_Timer == 8.0

    # Test TimeInShutdown_Timer
    model.TimeInShutdown_Timer = 9.0
    assert model.drs_Timer[8] == 9.0
    assert model.TimeInShutdown_Timer == 9.0


def test_numerical_variable_aliases():
    model = DRSModel()

    # Test MassOfCurrentParcel
    model.MassOfCurrentParcel = 500.0
    assert model.drs_DiscretelyDynamicalNumericalVariable[0] == 500.0
    assert model.MassOfCurrentParcel == 500.0

    # Test PercentageOfOre2InCurrentParcel
    model.PercentageOfOre2InCurrentParcel = 0.75
    assert model.drs_DiscretelyDynamicalNumericalVariable[1] == 0.75
    assert model.PercentageOfOre2InCurrentParcel == 0.75

    # Test NextParcelIsNewFacies
    model.NextParcelIsNewFacies = 1.0
    assert model.drs_DiscretelyDynamicalNumericalVariable[2] == 1.0
    assert model.NextParcelIsNewFacies == 1.0
