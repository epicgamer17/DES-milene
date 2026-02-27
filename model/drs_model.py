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

        # Configuration Expression Strings - Scalars
        self.confExString_TerminatingCondition = ""
        self.confExString_InitialRateConfigurationNumber = "0"

        # Configuration Expression Strings - Vectors
        self.confExString_InitialLevelValue = [""] * self.dim_NumberOfLevels
        self.confExString_InitialTimerValue = [""] * self.dim_NumberOfTimers
        self.confExString_InitialDiscretelyDynamicalNumericalVariableValue = [
            ""
        ] * self.dim_NumberOfDiscretelyDynamicalNumericalVariables
        self.confExString_InitialCategoricalVariableValue = [
            ""
        ] * self.dim_NumberOfCategoricalVariables

        # Configuration Expression Strings - Matrices (Levels x RateConfigurations)
        self.confExString_LevelRate = [
            ["" for _ in range(self.dim_NumberOfRateConfigurations)]
            for _ in range(self.dim_NumberOfLevels)
        ]
        self.confExString_LowerLevelThreshold = [
            ["" for _ in range(self.dim_NumberOfRateConfigurations)]
            for _ in range(self.dim_NumberOfLevels)
        ]
        self.confExString_UpperLevelThreshold = [
            ["" for _ in range(self.dim_NumberOfRateConfigurations)]
            for _ in range(self.dim_NumberOfLevels)
        ]
        self.confExString_LowerLevelResultantRateConfiguration = [
            ["" for _ in range(self.dim_NumberOfRateConfigurations)]
            for _ in range(self.dim_NumberOfLevels)
        ]
        self.confExString_UpperLevelResultantRateConfiguration = [
            ["" for _ in range(self.dim_NumberOfRateConfigurations)]
            for _ in range(self.dim_NumberOfLevels)
        ]
        self.confExString_LowerLevelAssignmentAddress = [
            ["" for _ in range(self.dim_NumberOfRateConfigurations)]
            for _ in range(self.dim_NumberOfLevels)
        ]
        self.confExString_UpperLevelAssignmentAddress = [
            ["" for _ in range(self.dim_NumberOfRateConfigurations)]
            for _ in range(self.dim_NumberOfLevels)
        ]

        # Configuration Expression Strings - Matrices (Timers x RateConfigurations)
        self.confExString_TimerRate = [
            ["" for _ in range(self.dim_NumberOfRateConfigurations)]
            for _ in range(self.dim_NumberOfTimers)
        ]
        self.confExString_LowerTimerThreshold = [
            ["" for _ in range(self.dim_NumberOfRateConfigurations)]
            for _ in range(self.dim_NumberOfTimers)
        ]
        self.confExString_UpperTimerThreshold = [
            ["" for _ in range(self.dim_NumberOfRateConfigurations)]
            for _ in range(self.dim_NumberOfTimers)
        ]
        self.confExString_LowerTimerResultantRateConfiguration = [
            ["" for _ in range(self.dim_NumberOfRateConfigurations)]
            for _ in range(self.dim_NumberOfTimers)
        ]
        self.confExString_UpperTimerResultantRateConfiguration = [
            ["" for _ in range(self.dim_NumberOfRateConfigurations)]
            for _ in range(self.dim_NumberOfTimers)
        ]
        self.confExString_LowerTimerAssignmentAddress = [
            ["" for _ in range(self.dim_NumberOfRateConfigurations)]
            for _ in range(self.dim_NumberOfTimers)
        ]
        self.confExString_UpperTimerAssignmentAddress = [
            ["" for _ in range(self.dim_NumberOfRateConfigurations)]
            for _ in range(self.dim_NumberOfTimers)
        ]

        # Configuration Expression Strings - Assignment Sequence
        self.confExString_AssignmentSequence = [
            ["" for _ in range(self.dim_NumberOfAssignmentSequenceAddresses)]
            for _ in range(self.dim_MaxLengthOfAssignmentSequence)
        ]

    @property
    def OreExtraction_Level(self) -> float:
        """Alias for drs_Level[0]"""
        return self.drs_Level[0]

    @OreExtraction_Level.setter
    def OreExtraction_Level(self, value: float):
        self.drs_Level[0] = value

    @property
    def OreExtractedFromCurrentParcel_Level(self) -> float:
        """Alias for drs_Level[1]"""
        return self.drs_Level[1]

    @OreExtractedFromCurrentParcel_Level.setter
    def OreExtractedFromCurrentParcel_Level(self, value: float):
        self.drs_Level[1] = value

    @property
    def OreStock_Level(self) -> float:
        """Alias for drs_Level[2]"""
        return self.drs_Level[2]

    @OreStock_Level.setter
    def OreStock_Level(self, value: float):
        self.drs_Level[2] = value

    @property
    def Ore1Stock_Level(self) -> float:
        """Alias for drs_Level[3]"""
        return self.drs_Level[3]

    @Ore1Stock_Level.setter
    def Ore1Stock_Level(self, value: float):
        self.drs_Level[3] = value

    @property
    def Ore2Stock_Level(self) -> float:
        """Alias for drs_Level[4]"""
        return self.drs_Level[4]

    @Ore2Stock_Level.setter
    def Ore2Stock_Level(self, value: float):
        self.drs_Level[4] = value

    @property
    def TimeExecutedInCurrentCampaignOrShutdown_Timer(self) -> float:
        """Alias for drs_Timer[0]"""
        return self.drs_Timer[0]

    @TimeExecutedInCurrentCampaignOrShutdown_Timer.setter
    def TimeExecutedInCurrentCampaignOrShutdown_Timer(self, value: float):
        self.drs_Timer[0] = value

    @property
    def TimeExecutedInCurrentContingencySegment_Timer(self) -> float:
        """Alias for drs_Timer[1]"""
        return self.drs_Timer[1]

    @TimeExecutedInCurrentContingencySegment_Timer.setter
    def TimeExecutedInCurrentContingencySegment_Timer(self, value: float):
        self.drs_Timer[1] = value

    @property
    def TimeInModeA_Timer(self) -> float:
        """Alias for drs_Timer[2]"""
        return self.drs_Timer[2]

    @TimeInModeA_Timer.setter
    def TimeInModeA_Timer(self, value: float):
        self.drs_Timer[2] = value

    @property
    def TimeInModeAContingency_Timer(self) -> float:
        """Alias for drs_Timer[3]"""
        return self.drs_Timer[3]

    @TimeInModeAContingency_Timer.setter
    def TimeInModeAContingency_Timer(self, value: float):
        self.drs_Timer[3] = value

    @property
    def TimeInModeAMineSurging_Timer(self) -> float:
        """Alias for drs_Timer[4]"""
        return self.drs_Timer[4]

    @TimeInModeAMineSurging_Timer.setter
    def TimeInModeAMineSurging_Timer(self, value: float):
        self.drs_Timer[4] = value

    @property
    def TimeInModeB_Timer(self) -> float:
        """Alias for drs_Timer[5]"""
        return self.drs_Timer[5]

    @TimeInModeB_Timer.setter
    def TimeInModeB_Timer(self, value: float):
        self.drs_Timer[5] = value

    @property
    def TimeInModeBContingency_Timer(self) -> float:
        """Alias for drs_Timer[6]"""
        return self.drs_Timer[6]

    @TimeInModeBContingency_Timer.setter
    def TimeInModeBContingency_Timer(self, value: float):
        self.drs_Timer[6] = value

    @property
    def TimeInModeBMineSurging_Timer(self) -> float:
        """Alias for drs_Timer[7]"""
        return self.drs_Timer[7]

    @TimeInModeBMineSurging_Timer.setter
    def TimeInModeBMineSurging_Timer(self, value: float):
        self.drs_Timer[7] = value

    @property
    def TimeInShutdown_Timer(self) -> float:
        """Alias for drs_Timer[8]"""
        return self.drs_Timer[8]

    @property
    def MassOfCurrentParcel(self) -> float:
        """Alias for drs_DiscretelyDynamicalNumericalVariable[0]"""
        return self.drs_DiscretelyDynamicalNumericalVariable[0]

    @MassOfCurrentParcel.setter
    def MassOfCurrentParcel(self, value: float):
        self.drs_DiscretelyDynamicalNumericalVariable[0] = value

    @property
    def PercentageOfOre2InCurrentParcel(self) -> float:
        """Alias for drs_DiscretelyDynamicalNumericalVariable[1]"""
        return self.drs_DiscretelyDynamicalNumericalVariable[1]

    @PercentageOfOre2InCurrentParcel.setter
    def PercentageOfOre2InCurrentParcel(self, value: float):
        self.drs_DiscretelyDynamicalNumericalVariable[1] = value

    @property
    def NextParcelIsNewFacies(self) -> float:
        """Alias for drs_DiscretelyDynamicalNumericalVariable[2]"""
        return self.drs_DiscretelyDynamicalNumericalVariable[2]

    @NextParcelIsNewFacies.setter
    def NextParcelIsNewFacies(self, value: float):
        self.drs_DiscretelyDynamicalNumericalVariable[2] = value

    @TimeInShutdown_Timer.setter
    def TimeInShutdown_Timer(self, value: float):
        self.drs_Timer[8] = value

    def load_configuration(self, config_dict: dict):
        """
        Populates configuration expression strings from an external dictionary or JSON.

        Args:
            config_dict: A dictionary containing configuration strings.
        """
        for key, value in config_dict.items():
            if key.startswith("confExString_") and hasattr(self, key):
                # Basic shape validation for 2D lists (matrices)
                if (
                    isinstance(value, list)
                    and len(value) > 0
                    and isinstance(value[0], list)
                ):
                    if "Level" in key:
                        assert (
                            len(value) == self.dim_NumberOfLevels
                        ), f"Outer dimension mismatch for {key}: expected {self.dim_NumberOfLevels}, got {len(value)}"
                        assert (
                            len(value[0]) == self.dim_NumberOfRateConfigurations
                        ), f"Inner dimension mismatch for {key}: expected {self.dim_NumberOfRateConfigurations}, got {len(value[0])}"
                    elif "Timer" in key:
                        assert (
                            len(value) == self.dim_NumberOfTimers
                        ), f"Outer dimension mismatch for {key}: expected {self.dim_NumberOfTimers}, got {len(value)}"
                        assert (
                            len(value[0]) == self.dim_NumberOfRateConfigurations
                        ), f"Inner dimension mismatch for {key}: expected {self.dim_NumberOfRateConfigurations}, got {len(value[0])}"
                    elif key == "confExString_AssignmentSequence":
                        assert (
                            len(value) == self.dim_MaxLengthOfAssignmentSequence
                        ), f"Outer dimension mismatch for {key}: expected {self.dim_MaxLengthOfAssignmentSequence}, got {len(value)}"
                        assert (
                            len(value[0])
                            == self.dim_NumberOfAssignmentSequenceAddresses
                        ), f"Inner dimension mismatch for {key}: expected {self.dim_NumberOfAssignmentSequenceAddresses}, got {len(value[0])}"

                # Basic shape validation for 1D lists (vectors)
                elif isinstance(value, list):
                    if key == "confExString_InitialLevelValue":
                        assert (
                            len(value) == self.dim_NumberOfLevels
                        ), f"Dimension mismatch for {key}: expected {self.dim_NumberOfLevels}, got {len(value)}"
                    elif key == "confExString_InitialTimerValue":
                        assert (
                            len(value) == self.dim_NumberOfTimers
                        ), f"Dimension mismatch for {key}: expected {self.dim_NumberOfTimers}, got {len(value)}"
                    elif (
                        key
                        == "confExString_InitialDiscretelyDynamicalNumericalVariableValue"
                    ):
                        assert (
                            len(value)
                            == self.dim_NumberOfDiscretelyDynamicalNumericalVariables
                        ), f"Dimension mismatch for {key}: expected {self.dim_NumberOfDiscretelyDynamicalNumericalVariables}, got {len(value)}"
                    elif key == "confExString_InitialCategoricalVariableValue":
                        assert (
                            len(value) == self.dim_NumberOfCategoricalVariables
                        ), f"Dimension mismatch for {key}: expected {self.dim_NumberOfCategoricalVariables}, got {len(value)}"

                setattr(self, key, value)
