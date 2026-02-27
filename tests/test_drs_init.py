import unittest
import numpy as np
from model.drs_model import DRSModel


class TestDRSInitialization(unittest.TestCase):
    def test_default_initialization(self):
        model = DRSModel()

        # Verify vectors
        self.assertIsInstance(model.drs_Level, np.ndarray)
        self.assertEqual(model.drs_Level.shape, (model.dim_NumberOfLevels,))
        self.assertEqual(model.drs_Level.dtype, np.float64)
        self.assertTrue(np.all(model.drs_Level == 0))

        self.assertIsInstance(model.drs_Timer, np.ndarray)
        self.assertEqual(model.drs_Timer.shape, (model.dim_NumberOfTimers,))
        self.assertTrue(np.all(model.drs_Timer == 0))

        self.assertIsInstance(
            model.drs_DiscretelyDynamicalNumericalVariable, np.ndarray
        )
        self.assertEqual(
            model.drs_DiscretelyDynamicalNumericalVariable.shape,
            (model.dim_NumberOfDiscretelyDynamicalNumericalVariables,),
        )
        self.assertTrue(np.all(model.drs_DiscretelyDynamicalNumericalVariable == 0))

        # Verify categorical
        self.assertIsInstance(model.drs_CategoricalVariable, list)
        self.assertEqual(
            len(model.drs_CategoricalVariable), model.dim_NumberOfCategoricalVariables
        )
        self.assertEqual(
            model.drs_CategoricalVariable, [""] * model.dim_NumberOfCategoricalVariables
        )

        # Verify scalars
        self.assertEqual(model.drs_RateConfigurationNumber, 0)
        self.assertEqual(model.drs_TimeOfPreviousDRSUpdate, 0.0)
        self.assertEqual(model.drs_DurationUntilThresholdCrossing, 0.0)
        self.assertEqual(model.drs_ThresholdCrossingLevelOrTimerNumber, 0)
        self.assertEqual(model.drs_ThresholdIsCrossedByTimer, 0)
        self.assertEqual(model.drs_DirectionOfThresholdCrossing, 0)

    def test_custom_initialization(self):
        model = DRSModel(dim_NumberOfLevels=10, dim_NumberOfCategoricalVariables=5)
        self.assertEqual(model.drs_Level.shape, (10,))
        self.assertEqual(len(model.drs_CategoricalVariable), 5)

    def test_configuration_expression_initialization(self):
        model = DRSModel()

        # Scalars
        self.assertEqual(model.confExString_TerminatingCondition, "")
        self.assertEqual(model.confExString_InitialRateConfigurationNumber, "0")

        # Vectors
        self.assertEqual(
            len(model.confExString_InitialLevelValue), model.dim_NumberOfLevels
        )
        self.assertEqual(
            len(model.confExString_InitialTimerValue), model.dim_NumberOfTimers
        )
        self.assertEqual(
            len(model.confExString_InitialDiscretelyDynamicalNumericalVariableValue),
            model.dim_NumberOfDiscretelyDynamicalNumericalVariables,
        )
        self.assertEqual(
            len(model.confExString_InitialCategoricalVariableValue),
            model.dim_NumberOfCategoricalVariables,
        )

        # Matrices (Level-indexed)
        level_matrices = [
            model.confExString_LevelRate,
            model.confExString_LowerLevelThreshold,
            model.confExString_UpperLevelThreshold,
            model.confExString_LowerLevelResultantRateConfiguration,
            model.confExString_UpperLevelResultantRateConfiguration,
            model.confExString_LowerLevelAssignmentAddress,
            model.confExString_UpperLevelAssignmentAddress,
        ]
        for matrix in level_matrices:
            self.assertEqual(len(matrix), model.dim_NumberOfLevels)
            for row in matrix:
                self.assertEqual(len(row), model.dim_NumberOfRateConfigurations)
                self.assertTrue(all(cell == "" for cell in row))

        # Matrices (Timer-indexed)
        timer_matrices = [
            model.confExString_TimerRate,
            model.confExString_LowerTimerThreshold,
            model.confExString_UpperTimerThreshold,
            model.confExString_LowerTimerResultantRateConfiguration,
            model.confExString_UpperTimerResultantRateConfiguration,
            model.confExString_LowerTimerAssignmentAddress,
            model.confExString_UpperTimerAssignmentAddress,
        ]
        for matrix in timer_matrices:
            self.assertEqual(len(matrix), model.dim_NumberOfTimers)
            for row in matrix:
                self.assertEqual(len(row), model.dim_NumberOfRateConfigurations)
                self.assertTrue(all(cell == "" for cell in row))

        # Assignment Sequence Matrix
        self.assertEqual(
            len(model.confExString_AssignmentSequence),
            model.dim_NumberOfAssignmentSequenceAddresses,
        )
        for row in model.confExString_AssignmentSequence:
            self.assertEqual(len(row), model.dim_MaxLengthOfAssignmentSequence)
            self.assertTrue(all(cell == "" for cell in row))


if __name__ == "__main__":
    unittest.main()
