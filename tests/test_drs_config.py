import pytest
from model.drs_model import DRSModel


@pytest.fixture
def drs_model():
    return DRSModel(
        dim_NumberOfLevels=2,
        dim_NumberOfTimers=3,
        dim_NumberOfDiscretelyDynamicalNumericalVariables=1,
        dim_NumberOfCategoricalVariables=1,
        dim_NumberOfRateConfigurations=4,
        dim_NumberOfAssignmentSequenceAddresses=2,
        dim_MaxLengthOfAssignmentSequence=2,
    )


def test_load_configuration_valid_scalars(drs_model):
    config = {
        "confExString_TerminatingCondition": "time > 100",
        "confExString_InitialRateConfigurationNumber": "1",
    }
    drs_model.load_configuration(config)
    assert drs_model.confExString_TerminatingCondition == "time > 100"
    assert drs_model.confExString_InitialRateConfigurationNumber == "1"


def test_load_configuration_valid_vectors(drs_model):
    config = {
        "confExString_InitialLevelValue": ["10.0", "20.0"],
        "confExString_InitialTimerValue": ["0.0", "1.0", "2.0"],
        "confExString_InitialDiscretelyDynamicalNumericalVariableValue": ["5"],
        "confExString_InitialCategoricalVariableValue": ["ModeA"],
    }
    drs_model.load_configuration(config)
    assert drs_model.confExString_InitialLevelValue == ["10.0", "20.0"]
    assert drs_model.confExString_InitialTimerValue == ["0.0", "1.0", "2.0"]


def test_load_configuration_valid_matrices(drs_model):
    # Levels x RateConfigs: 2 x 4
    level_rate = [["L1R1", "L1R2", "L1R3", "L1R4"], ["L2R1", "L2R2", "L2R3", "L2R4"]]
    # Timers x RateConfigs: 3 x 4
    timer_rate = [
        ["T1R1", "T1R2", "T1R3", "T1R4"],
        ["T2R1", "T2R2", "T2R3", "T2R4"],
        ["T3R1", "T3R2", "T3R3", "T3R4"],
    ]
    config = {
        "confExString_LevelRate": level_rate,
        "confExString_TimerRate": timer_rate,
    }
    drs_model.load_configuration(config)
    assert drs_model.confExString_LevelRate == level_rate
    assert drs_model.confExString_TimerRate == timer_rate


def test_load_configuration_assignment_sequence(drs_model):
    # MaxLength x Addresses: 2 x 2
    seq = [["Addr1", "Val1"], ["Addr2", "Val2"]]
    config = {"confExString_AssignmentSequence": seq}
    drs_model.load_configuration(config)
    assert drs_model.confExString_AssignmentSequence == seq


def test_load_configuration_invalid_vector_shape(drs_model):
    config = {"confExString_InitialLevelValue": ["10.0"]}  # Expected 2
    with pytest.raises(AssertionError) as excinfo:
        drs_model.load_configuration(config)
    assert "Dimension mismatch for confExString_InitialLevelValue" in str(excinfo.value)


def test_load_configuration_invalid_matrix_shape(drs_model):
    # Levels x RateConfigs: 2 x 4. Providing 3 x 4
    level_rate = [[""] * 4, [""] * 4, [""] * 4]
    config = {"confExString_LevelRate": level_rate}
    with pytest.raises(AssertionError) as excinfo:
        drs_model.load_configuration(config)
    assert "Outer dimension mismatch for confExString_LevelRate" in str(excinfo.value)

    # Providing 2 x 5
    level_rate = [[""] * 5, [""] * 5]
    config = {"confExString_LevelRate": level_rate}
    with pytest.raises(AssertionError) as excinfo:
        drs_model.load_configuration(config)
    assert "Inner dimension mismatch for confExString_LevelRate" in str(excinfo.value)


def test_load_non_conf_key(drs_model):
    config = {"some_other_key": "value"}
    drs_model.load_configuration(config)
    assert not hasattr(drs_model, "some_other_key")
