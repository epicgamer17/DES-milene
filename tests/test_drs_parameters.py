from dataclasses import dataclass
from model.drs_model import DRSModel


@dataclass
class MiningParameters:
    parameter_OreToBeExtractedDuringWarmingPeriod: float = 600000.0
    parameter_TotalOreToBeExtracted: float = 6600000.0
    parameter_DurationOfProductionCampaigns: float = 34.0
    parameter_DurationOfShutdowns: float = 1.0
    parameter_ModeAOre1MillingRate: float = 3600.0
    parameter_ModeAOre2MillingRate: float = 2400.0
    parameter_ModeAContingencyOre1MillingRate: float = 3900.0
    parameter_ModeBOre1MillingRate: float = 4600.0
    parameter_ModeBOre2MillingRate: float = 800.0
    parameter_ModeBContingencyOre2MillingRate: float = 2500.0
    parameterVector_GeostatisticalModelParameters: list = None
    controlVariable_CriticalOre2Level: float = 20400.0
    controlVariable_TargetOreStockLevel: float = 60000.0
    controlVariable_DurationOfContingencySegments: float = 1.0

    def __post_init__(self):
        if self.parameterVector_GeostatisticalModelParameters is None:
            self.parameterVector_GeostatisticalModelParameters = [
                30000.0,
                50000.0,
                30.0,
                30.0,
                5.0,
                1.0,
            ]


def test_drs_domain_constants():
    """
    Verifies that the DRSModel initializes correctly when passed an external parameters object.
    """
    params = MiningParameters()
    model = DRSModel(parameters=params)

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
