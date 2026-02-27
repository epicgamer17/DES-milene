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


if __name__ == "__main__":
    unittest.main()
