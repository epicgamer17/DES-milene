import pytest
from unittest.mock import patch, MagicMock
from model.drs_model import DRSModel


@pytest.fixture
def drs_model():
    """Fixture to provide a fresh DRSModel instance."""
    return DRSModel(
        dim_NumberOfLevels=5,
        dim_NumberOfTimers=9,
        dim_NumberOfDiscretelyDynamicalNumericalVariables=3,
        dim_NumberOfCategoricalVariables=1,
        dim_NumberOfRateConfigurations=7,
        dim_NumberOfAssignmentSequenceAddresses=6,
        dim_MaxLengthOfAssignmentSequence=7,
    )


def test_execute_assignments_level(drs_model):
    """Mock an assignment string 'L002=150'. Assert drs_Level[1] becomes 150."""
    # 1. Setup the assignment sequence
    # Assignment address 1 corresponds to index 0
    # Step 0 of sequence
    drs_model.confExString_AssignmentSequence[0][0] = "L002:150"
    drs_model.current_assignment_address = 1

    # 2. Execute assignments
    drs_model.execute_assignments()

    # 3. Assert level update (0-based index 1)
    assert drs_model.drs_Level[1] == 150.0


def test_execute_assignments_external(drs_model):
    """Mock string 'E001=42'. Verify execute_external_code(42) is called."""
    # 1. Setup the assignment sequence
    drs_model.confExString_AssignmentSequence[0][0] = "E001:42"
    drs_model.current_assignment_address = 1

    # 2. Mock execute_external_code and execute assignments
    with patch.object(drs_model, "execute_external_code") as mock_execute:
        drs_model.execute_assignments()
        # 3. Verify call
        mock_execute.assert_called_once_with(42)


def test_execute_assignments_numerical(drs_model):
    """Mock an assignment string 'N001=99.5'. Assert drs_DiscretelyDynamicalNumericalVariable[0] becomes 99.5."""
    drs_model.confExString_AssignmentSequence[0][0] = "N001:99.5"
    drs_model.current_assignment_address = 1

    drs_model.execute_assignments()

    assert drs_model.drs_DiscretelyDynamicalNumericalVariable[0] == 99.5


def test_execute_assignments_categorical(drs_model):
    """Mock an assignment string 'C001=10'. Assert drs_CategoricalVariable[0] becomes '10.0'."""
    drs_model.confExString_AssignmentSequence[0][0] = "C001:10"
    drs_model.current_assignment_address = 1

    drs_model.execute_assignments()

    assert drs_model.drs_CategoricalVariable[0] == "10.0"


def test_execute_assignments_timer(drs_model):
    """Mock an assignment string 'T003=5.5'. Assert drs_Timer[2] becomes 5.5."""
    drs_model.confExString_AssignmentSequence[0][0] = "T003:5.5"
    drs_model.current_assignment_address = 1

    drs_model.execute_assignments()

    assert drs_model.drs_Timer[2] == 5.5


def test_execute_assignments_no_address(drs_model):
    """Verify that if current_assignment_address is 0, no changes are made."""
    drs_model.confExString_AssignmentSequence[0][0] = "L001:100"
    drs_model.current_assignment_address = 0

    drs_model.execute_assignments()

    assert drs_model.drs_Level[0] == 0.0


def test_execute_assignments_multiple_steps(drs_model):
    """Verify that multiple steps in a sequence are executed."""
    drs_model.confExString_AssignmentSequence[0][0] = "L001:10"
    drs_model.confExString_AssignmentSequence[0][1] = "L002:20"
    drs_model.current_assignment_address = 1

    drs_model.execute_assignments()

    assert drs_model.drs_Level[0] == 10.0
    assert drs_model.drs_Level[1] == 20.0
