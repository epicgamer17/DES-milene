import numpy as np
import re
from dataclasses import dataclass, asdict
import matplotlib.pyplot as plt


@dataclass
class OutputStatistics:
    total_time: float
    active_time: float
    PortionOfTimeInModeA: float
    PortionOfTimeInModeAContingency: float
    PortionOfTimeInModeAMineSurging: float
    PortionOfTimeInModeB: float
    PortionOfTimeInModeBContingency: float
    PortionOfTimeInModeBMineSurging: float
    PortionOfTimeInShutdown: float
    Throughput: float


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
        parameters: any = None,
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

        # Simulation clock
        self.TNOW = 0.0

        # State tracking vectors
        self.drs_Level = np.zeros(self.dim_NumberOfLevels, dtype=np.float64)
        self.drs_Timer = np.zeros(self.dim_NumberOfTimers, dtype=np.float64)
        self.drs_DiscretelyDynamicalNumericalVariable = np.zeros(
            self.dim_NumberOfDiscretelyDynamicalNumericalVariables, dtype=np.float64
        )
        self.drs_CategoricalVariable = [""] * self.dim_NumberOfCategoricalVariables

        # Scalar functional variables
        self.drs_RateConfigurationNumber = 1
        self.drs_TimeOfPreviousDRSUpdate = 0.0
        self.drs_DurationUntilThresholdCrossing = 0.0
        self.drs_ThresholdCrossingLevelOrTimerNumber = 0
        self.drs_ThresholdIsCrossedByTimer = 0
        self.drs_DirectionOfThresholdCrossing = 0
        self.current_assignment_address = 0

        # History Logs
        self.history_time = []
        self.history_rate_config = []
        self.history_ore_levels = []

        # Unpack external parameters if provided
        if parameters is not None:
            # Handle both dataclasses and classes/objects
            params_dict = (
                asdict(parameters)
                if hasattr(parameters, "__dataclass_fields__")
                else vars(parameters)
            )
            for key, value in params_dict.items():
                setattr(self, key, value)

        # Configuration Expression Strings - Scalars
        self.confExString_TerminatingCondition = ""
        self.confExString_InitialRateConfigurationNumber = "1"

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
            ["" for _ in range(self.dim_MaxLengthOfAssignmentSequence)]
            for _ in range(self.dim_NumberOfAssignmentSequenceAddresses)
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
                            len(value) == self.dim_NumberOfAssignmentSequenceAddresses
                        ), f"Outer dimension mismatch for {key}: expected {self.dim_NumberOfAssignmentSequenceAddresses}, got {len(value)}"
                        assert (
                            len(value[0]) == self.dim_MaxLengthOfAssignmentSequence
                        ), f"Inner dimension mismatch for {key}: expected {self.dim_MaxLengthOfAssignmentSequence}, got {len(value[0])}"

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

    def evaluate_expression(self, expression_string: str) -> float:
        """
        Parses and executes Arena formula strings against the simulation state.
        """
        if not expression_string or expression_string.strip() == "":
            return 0.0

        processed = expression_string.strip()

        # 1. Remove Eval(...) wrapper if it exists
        eval_match = re.match(r"^Eval\((.*)\)$", processed, re.IGNORECASE)
        if eval_match:
            processed = eval_match.group(1)

        # 2. Translate Arena Math & Logic to Python
        processed = processed.replace("&&", " and ")
        processed = processed.replace("||", " or ")
        processed = processed.replace("<>", " != ")
        processed = processed.replace("MN(", "min(").replace("MX(", "max(")
        processed = processed.replace("ABS(", "abs(")
        processed = processed.replace("UNIF(", "np.random.uniform(")
        processed = processed.replace("NORM(", "np.random.normal(")

        # 3. Handle 1-based indexing for drs_ arrays and parameter vectors
        def replace_index(match):
            prefix = match.group(1)
            index = int(match.group(2))
            return f"{prefix}[{index - 1}]"

        processed = re.sub(
            r"(drs_Level|drs_Timer|drs_DiscretelyDynamicalNumericalVariable|drs_CategoricalVariable)\((\d+)\)",
            replace_index,
            processed,
        )
        processed = re.sub(
            r"(parameterVector_GeostatisticalModelParameters)\((\d+)\)",
            replace_index,
            processed,
        )

        # 4. Build the Execution Namespace
        local_namespace = {
            "drs_Level": self.drs_Level,
            "drs_Timer": self.drs_Timer,
            "drs_RateConfigurationNumber": self.drs_RateConfigurationNumber,
            "TNOW": self.TNOW,
            "min": min,
            "max": max,
            "abs": abs,
            "np": np,  # Needed for the random distribution functions
        }

        # Dynamically load all parameters and properties into the namespace so eval() can see them
        for attr in dir(self):
            if (
                attr.startswith("parameter")
                or attr.startswith("controlVariable")
                or attr.endswith("_Level")
                or attr.endswith("_Timer")
                or attr
                in [
                    "MassOfCurrentParcel",
                    "PercentageOfOre2InCurrentParcel",
                    "NextParcelIsNewFacies",
                ]
            ):
                local_namespace[attr] = getattr(self, attr)

        try:
            # Safely evaluate the expression
            result = eval(processed, {"__builtins__": None}, local_namespace)

            # Handle booleans and strings
            if isinstance(result, bool):
                return 1.0 if result else 0.0
            if isinstance(result, str):
                return result

            return float(result)
        except Exception as e:
            raise ValueError(
                f"Error evaluating expression '{expression_string}'\nTranslated to: '{processed}'\nError: {e}"
            )

    def initialize_simulation(self):
        """
        Sets the simulation to time zero and evaluates all initial starting strings.
        Bootstraps the DRSModel state before the event loop begins.
        """
        self.TNOW = 0.0
        self.drs_TimeOfPreviousDRSUpdate = self.TNOW

        # Evaluate and assign the starting rate configuration
        self.drs_RateConfigurationNumber = int(
            self.evaluate_expression(self.confExString_InitialRateConfigurationNumber)
        )

        # Loop through levels and populate drs_Level
        for i in range(self.dim_NumberOfLevels):
            self.drs_Level[i] = self.evaluate_expression(
                self.confExString_InitialLevelValue[i]
            )

        # Loop through timers and populate drs_Timer
        for i in range(self.dim_NumberOfTimers):
            self.drs_Timer[i] = self.evaluate_expression(
                self.confExString_InitialTimerValue[i]
            )

        # Loop through discrete numerical variables
        for i in range(self.dim_NumberOfDiscretelyDynamicalNumericalVariables):
            self.drs_DiscretelyDynamicalNumericalVariable[i] = float(
                self.evaluate_expression(
                    self.confExString_InitialDiscretelyDynamicalNumericalVariableValue[
                        i
                    ]
                )
            )

        # Loop through categorical variables
        for i in range(self.dim_NumberOfCategoricalVariables):
            expr = self.confExString_InitialCategoricalVariableValue[i]
            if not expr or expr.strip() == "":
                self.drs_CategoricalVariable[i] = ""
            else:
                self.drs_CategoricalVariable[i] = str(self.evaluate_expression(expr))

    def characterize_thresholds(self):
        """
        Calculates the time until the next discrete event by evaluating all levels and timers
        against their respective thresholds based on current rates.
        """
        self.drs_DurationUntilThresholdCrossing = 99999.0
        rate_config = self.drs_RateConfigurationNumber - 1

        # Step 1: Calculate Minimum Duration for Levels
        for i in range(self.dim_NumberOfLevels):
            rate_expr = self.confExString_LevelRate[i][rate_config]
            rate = self.evaluate_expression(rate_expr)

            time_to_cross = 99999.0
            direction = 0

            if rate < 0:
                lower_threshold_expr = self.confExString_LowerLevelThreshold[i][
                    rate_config
                ]
                lower_threshold = self.evaluate_expression(lower_threshold_expr)
                time_to_cross = (lower_threshold - self.drs_Level[i]) / rate
                direction = -1
            elif rate > 0:
                upper_threshold_expr = self.confExString_UpperLevelThreshold[i][
                    rate_config
                ]
                upper_threshold = self.evaluate_expression(upper_threshold_expr)
                time_to_cross = (upper_threshold - self.drs_Level[i]) / rate
                direction = 1

            if (
                time_to_cross < self.drs_DurationUntilThresholdCrossing
                and time_to_cross > 1e-9
            ):
                self.drs_DurationUntilThresholdCrossing = time_to_cross
                self.drs_ThresholdCrossingLevelOrTimerNumber = i
                self.drs_ThresholdIsCrossedByTimer = 0
                self.drs_DirectionOfThresholdCrossing = direction

        # Step 2: Repeat for Timers
        for i in range(self.dim_NumberOfTimers):
            rate_expr = self.confExString_TimerRate[i][rate_config]
            rate = self.evaluate_expression(rate_expr)

            time_to_cross = 99999.0
            direction = 0

            if rate < 0:
                lower_threshold_expr = self.confExString_LowerTimerThreshold[i][
                    rate_config
                ]
                lower_threshold = self.evaluate_expression(lower_threshold_expr)
                time_to_cross = (lower_threshold - self.drs_Timer[i]) / rate
                direction = -1
            elif rate > 0:
                upper_threshold_expr = self.confExString_UpperTimerThreshold[i][
                    rate_config
                ]
                upper_threshold = self.evaluate_expression(upper_threshold_expr)
                time_to_cross = (upper_threshold - self.drs_Timer[i]) / rate
                direction = 1

            if (
                time_to_cross < self.drs_DurationUntilThresholdCrossing
                and time_to_cross > 1e-9
            ):
                self.drs_DurationUntilThresholdCrossing = time_to_cross
                self.drs_ThresholdCrossingLevelOrTimerNumber = i
                self.drs_ThresholdIsCrossedByTimer = 1
                self.drs_DirectionOfThresholdCrossing = direction

    def advance_simulation(self):
        """
        Fast-forwards the simulation clock and updates continuous variables.
        """
        duration = max(self.drs_DurationUntilThresholdCrossing, 0.0)

        # Advance global clock
        self.TNOW += duration

        rate_config = self.drs_RateConfigurationNumber - 1

        # Update Levels
        for i in range(self.dim_NumberOfLevels):
            rate_expr = self.confExString_LevelRate[i][rate_config]
            rate = self.evaluate_expression(rate_expr)
            self.drs_Level[i] += rate * duration

        # Update Timers
        for i in range(self.dim_NumberOfTimers):
            rate_expr = self.confExString_TimerRate[i][rate_config]
            rate = self.evaluate_expression(rate_expr)
            self.drs_Timer[i] += rate * duration

        self.drs_TimeOfPreviousDRSUpdate = self.TNOW

        # Determine Assignment Address
        idx = self.drs_ThresholdCrossingLevelOrTimerNumber
        direction = self.drs_DirectionOfThresholdCrossing

        if self.drs_ThresholdIsCrossedByTimer == 0:  # Level
            if direction == -1:  # Lower
                addr_expr = self.confExString_LowerLevelAssignmentAddress[idx][
                    rate_config
                ]
            elif direction == 1:  # Upper
                addr_expr = self.confExString_UpperLevelAssignmentAddress[idx][
                    rate_config
                ]
            else:
                addr_expr = "0"
        else:  # Timer
            if direction == -1:  # Lower
                addr_expr = self.confExString_LowerTimerAssignmentAddress[idx][
                    rate_config
                ]
            elif direction == 1:  # Upper
                addr_expr = self.confExString_UpperTimerAssignmentAddress[idx][
                    rate_config
                ]
            else:
                addr_expr = "0"

        self.current_assignment_address = int(self.evaluate_expression(addr_expr))

        self.current_assignment_address = int(self.evaluate_expression(addr_expr))

    def execute_assignments(self):
        """
        Parses and applies discrete instantaneous changes triggered by threshold events.
        Loops through the assignment sequence at current_assignment_address.
        """
        if self.current_assignment_address == 0:
            return

        # 1-based address to 0-based Python index
        addr_idx = self.current_assignment_address - 1

        # The assignment sequence is stored as Matrix[NumberOfAddresses][MaxLength]
        # We need to iterate through the sequence for the given address.
        for step in range(self.dim_MaxLengthOfAssignmentSequence):
            assignment_str = self.confExString_AssignmentSequence[addr_idx][step]
            if not assignment_str or assignment_str.strip() == "":
                continue

            assignment_str = assignment_str.strip()
            # Match the assignment string: TypeIdentifier, index, and expression
            # Example: "L002:150"
            match = re.match(r"^([LTNCE])(\d+):(.*)$", assignment_str)
            if not match:
                continue

            type_id = match.group(1).upper()
            target_idx_1based = int(match.group(2))
            expression = match.group(3).strip()

            target_idx = target_idx_1based - 1  # 0-based

            if type_id == "E":
                # For 'E', cast expression to int and execute external code
                try:
                    code_number = int(expression)
                    self.execute_external_code(code_number)
                except ValueError:
                    # If expression isn't a simple int, evaluate it first?
                    # "cast the expression to an int" suggests it should be an int.
                    val = int(self.evaluate_expression(expression))
                    self.execute_external_code(val)
                continue

            # For others, evaluate the expression
            value = self.evaluate_expression(expression)

            if type_id == "L":
                self.drs_Level[target_idx] = value
            elif type_id == "T":
                self.drs_Timer[target_idx] = value
            elif type_id == "N":
                self.drs_DiscretelyDynamicalNumericalVariable[target_idx] = value
            elif type_id == "C":
                self.drs_CategoricalVariable[target_idx] = str(value)

    def execute_external_code(self, code_number: int):
        """
        Triggered by 'E' in assignment sequences for custom control logic.
        """
        if code_number == 1:
            # Check if the ablation toggle is ON (defaults to False if not provided)
            if getattr(self, "enable_feed_control", False):
                # Calculate stockpile imbalance (avoid division by zero)
                total_stock = max(self.Ore1Stock_Level + self.Ore2Stock_Level, 1.0)
                ore2_ratio = self.Ore2Stock_Level / total_stock

                # If Ore 2 makes up > 40% of the stock, we have too much!
                if ore2_ratio > 0.40:
                    # Force the next parcel to have 2% less Ore 2
                    self.PercentageOfOre2InCurrentParcel = max(
                        self.PercentageOfOre2InCurrentParcel - 2.0, 0.0
                    )

                # If Ore 2 makes up < 20% of the stock, we need more!
                elif ore2_ratio < 0.20:
                    self.PercentageOfOre2InCurrentParcel = min(
                        self.PercentageOfOre2InCurrentParcel + 2.0, 100.0
                    )

    def update_rate_configuration(self):
        """
        Shifts the system into its new state (rate configuration) based on the threshold crossed.
        """
        idx = self.drs_ThresholdCrossingLevelOrTimerNumber
        current_rate_config = self.drs_RateConfigurationNumber - 1
        direction = self.drs_DirectionOfThresholdCrossing

        if self.drs_ThresholdIsCrossedByTimer == 0:  # Level
            if direction == -1:  # Lower
                matrix = self.confExString_LowerLevelResultantRateConfiguration
            else:  # Upper (1)
                matrix = self.confExString_UpperLevelResultantRateConfiguration
        else:  # Timer (1)
            if direction == -1:  # Lower
                matrix = self.confExString_LowerTimerResultantRateConfiguration
            else:  # Upper (1)
                matrix = self.confExString_UpperTimerResultantRateConfiguration

        # Evaluate the string at (ThresholdCrossingNumber, CurrentRateConfiguration)
        expr = matrix[idx][current_rate_config]
        new_rate_config = int(self.evaluate_expression(expr))

        # Assign the new rate configuration only if it's not 0
        if new_rate_config != 0:
            self.drs_RateConfigurationNumber = new_rate_config

    def run(self, max_iterations: int = 100000):
        """
        Main execution loop for the DRS model.
        Cycles through subsystems until the terminating condition is met.

        Args:
            max_iterations: Safety break to prevent infinite loops.
        """
        self.initialize_simulation()

        # Helper to log history
        def log_state():
            self.history_time.append(self.TNOW)
            self.history_rate_config.append(self.drs_RateConfigurationNumber)
            self.history_ore_levels.append(
                (self.OreStock_Level, self.Ore1Stock_Level, self.Ore2Stock_Level)
            )

        log_state()  # Log Initial State

        iterations = 0
        while not self.evaluate_expression(self.confExString_TerminatingCondition):
            if iterations >= max_iterations:
                print(
                    f"Warning: Simulation reached max iterations ({max_iterations}). Breaking loop."
                )
                break

            self.characterize_thresholds()

            # Log state right before time advances (creates the vertical "step" in the plot)
            log_state()

            self.advance_simulation()
            self.execute_assignments()
            self.update_rate_configuration()

            # Log state right after discrete events resolve
            log_state()

            iterations += 1

            if iterations % 100 == 0:
                print(f"Iteration {iterations}: TNOW = {self.TNOW:.2f}")

    def calculate_statistics(self) -> OutputStatistics:
        """
        Calculates and returns the final simulation report statistics.
        Calculates exact ratios and throughput based on terminal state.
        """
        # Calculate denominators
        total_time = (
            self.TimeInModeA_Timer
            + self.TimeInModeAContingency_Timer
            + self.TimeInModeAMineSurging_Timer
            + self.TimeInModeB_Timer
            + self.TimeInModeBContingency_Timer
            + self.TimeInModeBMineSurging_Timer
            + self.TimeInShutdown_Timer
        )

        active_time = total_time - self.TimeInShutdown_Timer

        return OutputStatistics(
            total_time=total_time,
            active_time=active_time,
            PortionOfTimeInModeA=(
                self.TimeInModeA_Timer / total_time if total_time > 0 else 0.0
            ),
            PortionOfTimeInModeAContingency=(
                self.TimeInModeAContingency_Timer / total_time
                if total_time > 0
                else 0.0
            ),
            PortionOfTimeInModeAMineSurging=(
                self.TimeInModeAMineSurging_Timer / total_time
                if total_time > 0
                else 0.0
            ),
            PortionOfTimeInModeB=(
                self.TimeInModeB_Timer / total_time if total_time > 0 else 0.0
            ),
            PortionOfTimeInModeBContingency=(
                self.TimeInModeBContingency_Timer / total_time
                if total_time > 0
                else 0.0
            ),
            PortionOfTimeInModeBMineSurging=(
                self.TimeInModeBMineSurging_Timer / total_time
                if total_time > 0
                else 0.0
            ),
            PortionOfTimeInShutdown=(
                self.TimeInShutdown_Timer / total_time if total_time > 0 else 0.0
            ),
            Throughput=(
                (self.Ore1Stock_Level + self.Ore2Stock_Level) / total_time
                if total_time > 0
                else 0.0
            ),
        )

    def plot_results(self):
        """
        Generates graphical outputs: "Modes" plot and "Ore Level" plot.
        """
        if not self.history_time:
            print("No history data to plot.")
            return

        times = np.array(self.history_time)
        rate_configs = np.array(self.history_rate_config)
        ore_levels = np.array(self.history_ore_levels)

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

        # Plot 1: Modes Plot
        # Mode A: Y=3 if rate_config in [1, 2, 3] else 0
        mode_a = np.where(np.isin(rate_configs, [1, 2, 3]), 3, 0)
        # Mode B: Y=2 if rate_config in [4, 5, 6] else 0
        mode_b = np.where(np.isin(rate_configs, [4, 5, 6]), 2, 0)
        # Shutdown: Y=1 if rate_config == 7 else 0
        shutdown = np.where(rate_configs == 7, 1, 0)

        ax1.step(times, mode_a, where="post", label="Mode A", color="blue")
        ax1.step(times, mode_b, where="post", label="Mode B", color="orange")
        ax1.step(times, shutdown, where="post", label="Shutdown", color="red")

        ax1.set_ylim(0, 4)
        ax1.set_ylabel("Active Mode")
        ax1.set_title("Simulation Modes")
        ax1.legend()
        ax1.grid(True)

        # Plot 2: Ore Level Plot
        # Unpack and divide by 1000 for kilotonnes
        total_ore = ore_levels[:, 0] / 1000.0
        ore1 = ore_levels[:, 1] / 1000.0
        ore2 = ore_levels[:, 2] / 1000.0

        ax2.plot(times, total_ore, label="Total Ore Stockpile Level", color="black")
        ax2.plot(times, ore1, label="Ore 1 Stockpile Level", color="green")
        ax2.plot(times, ore2, label="Ore 2 Stockpile Level", color="pink")

        target_kt = self.controlVariable_TargetOreStockLevel / 1000.0
        upper_kt = getattr(self, "controlVariable_StockUpperLimit", 60000.0) / 1000.0
        lower_kt = getattr(self, "controlVariable_StockLowerLimit", 60000.0) / 1000.0

        ax2.axhline(target_kt, color="gray", linestyle="--", alpha=0.7, label="Target")
        if upper_kt != target_kt:  # Only plot bounds if Hysteresis is active
            ax2.axhspan(
                lower_kt, upper_kt, color="yellow", alpha=0.2, label="Control Deadband"
            )

        ax2.set_ylim(0, 80)
        ax2.set_ylabel("Ore Level (kt)")
        ax2.set_xlabel("Time (h)")
        ax2.set_title("Ore Stockpile Levels")
        ax2.legend()
        ax2.grid(True)

        plt.tight_layout()
        plt.show()
