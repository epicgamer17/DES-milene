import sys
import os

# Add the project root to sys.path to allow importing drs_model
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from drs_model import DRSModel


def test_default_initialization():
    print("Testing default initialization...")
    model = DRSModel()
    assert model.dim_NumberOfLevels == 5
    assert model.dim_NumberOfTimers == 9
    assert model.dim_NumberOfDiscretelyDynamicalNumericalVariables == 3
    assert model.dim_NumberOfCategoricalVariables == 1
    assert model.dim_NumberOfRateConfigurations == 7
    assert model.dim_NumberOfAssignmentSequenceAddresses == 6
    assert model.dim_MaxLengthOfAssignmentSequence == 7
    print("Default initialization passed!")


def test_override_initialization():
    print("Testing override initialization...")
    model = DRSModel(
        dim_NumberOfLevels=10,
        dim_NumberOfTimers=15,
        dim_NumberOfDiscretelyDynamicalNumericalVariables=5,
        dim_NumberOfCategoricalVariables=2,
        dim_NumberOfRateConfigurations=10,
        dim_NumberOfAssignmentSequenceAddresses=8,
        dim_MaxLengthOfAssignmentSequence=12,
    )
    assert model.dim_NumberOfLevels == 10
    assert model.dim_NumberOfTimers == 15
    assert model.dim_NumberOfDiscretelyDynamicalNumericalVariables == 5
    assert model.dim_NumberOfCategoricalVariables == 2
    assert model.dim_NumberOfRateConfigurations == 10
    assert model.dim_NumberOfAssignmentSequenceAddresses == 8
    assert model.dim_MaxLengthOfAssignmentSequence == 12
    print("Override initialization passed!")


if __name__ == "__main__":
    test_default_initialization()
    test_override_initialization()
    print("All tests passed!")
