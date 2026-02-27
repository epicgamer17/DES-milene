import pytest
from model.drs_model import DRSModel


def test_drs_domain_constants():
    """
    Verifies that the DRSModel initializes with the correct hardcoded domain constants.
    """
    model = DRSModel()

    # Mining Parameters
    assert model.parameter_OreToBeExtractedDuringWarmingPeriod == 600000.0
    assert model.parameter_TotalOreToBeExtracted == 6600000.0
    assert model.parameter_DurationOfProductionCampaigns == 34.0
    assert model.parameter_DurationOfShutdowns == 1.0
    assert model.parameter_ModeAOre1MillingRate == 3600.0
    assert model.parameter_ModeAOre2MillingRate == 2400.0
    assert model.parameter_ModeAContingencyOre1MillingRate == 3900.0
    assert model.parameter_ModeBOre1MillingRate == 4600.0
    assert model.parameter_ModeBOre2MillingRate == 800.0
    assert model.parameter_ModeBContingencyOre2MillingRate == 2500.0
    assert model.parameterVector_GeostatisticalModelParameters == [
        30000.0,
        50000.0,
        30.0,
        30.0,
        5.0,
        1.0,
    ]

    # Control Variables
    assert model.controlVariable_CriticalOre2Level == 20400.0
    assert model.controlVariable_TargetOreStockLevel == 60000.0
    assert model.controlVariable_DurationOfContingencySegments == 1.0
