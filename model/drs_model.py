import numpy as np


class DRSModel:
    """
    Core DRSModel class for a Discrete Rate Simulation framework.
    Initializes foundational dimension attributes based on the "Model Dimensions" specification.
    """

    def __init__(
        self,
        dim_NumberOfLevels: int = 5,
        dim_NumberOfTimers: int = 9,
        dim_NumberOfDiscretelyDynamicalNumericalVariables: int = 3,
        dim_NumberOfCategoricalVariables: int = 1,
        dim_NumberOfRateConfigurations: int = 7,
        dim_NumberOfAssignmentSequenceAddresses: int = 6,
        dim_MaxLengthOfAssignmentSequence: int = 7,
    ):
        """
        Initializes the dimension variables for the simulation state.

        Args:
            dim_NumberOfLevels: Number of continuous level variables.
            dim_NumberOfTimers: Number of timer variables.
            dim_NumberOfDiscretelyDynamicalNumericalVariables: Number of discrete numerical variables.
            dim_NumberOfCategoricalVariables: Number of categorical variables.
            dim_NumberOfRateConfigurations: Number of different rate configurations.
            dim_NumberOfAssignmentSequenceAddresses: Number of assignment sequence addresses.
            dim_MaxLengthOfAssignmentSequence: Maximum length of an assignment sequence.
        """
        self.dim_NumberOfLevels = dim_NumberOfLevels
        self.dim_NumberOfTimers = dim_NumberOfTimers
        self.dim_NumberOfDiscretelyDynamicalNumericalVariables = (
            dim_NumberOfDiscretelyDynamicalNumericalVariables
        )
        self.dim_NumberOfCategoricalVariables = dim_NumberOfCategoricalVariables
        self.dim_NumberOfRateConfigurations = dim_NumberOfRateConfigurations
        self.dim_NumberOfAssignmentSequenceAddresses = (
            dim_NumberOfAssignmentSequenceAddresses
        )
        self.dim_MaxLengthOfAssignmentSequence = dim_MaxLengthOfAssignmentSequence

        # State tracking vectors
        self.drs_Level = np.zeros(self.dim_NumberOfLevels, dtype=np.float64)
        self.drs_Timer = np.zeros(self.dim_NumberOfTimers, dtype=np.float64)
        self.drs_DiscretelyDynamicalNumericalVariable = np.zeros(
            self.dim_NumberOfDiscretelyDynamicalNumericalVariables, dtype=np.float64
        )
        self.drs_CategoricalVariable = [""] * self.dim_NumberOfCategoricalVariables

        # Scalar functional variables
        self.drs_RateConfigurationNumber = 0
        self.drs_TimeOfPreviousDRSUpdate = 0.0
        self.drs_DurationUntilThresholdCrossing = 0.0
        self.drs_ThresholdCrossingLevelOrTimerNumber = 0
        self.drs_ThresholdIsCrossedByTimer = 0
        self.drs_DirectionOfThresholdCrossing = 0
