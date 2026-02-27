import numpy as np
import re


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
        self.drs_RateConfigurationNumber = 0
        self.drs_TimeOfPreviousDRSUpdate = 0.0
        self.drs_DurationUntilThresholdCrossing = 0.0
        self.drs_ThresholdCrossingLevelOrTimerNumber = 0
        self.drs_ThresholdIsCrossedByTimer = 0
        self.drs_DirectionOfThresholdCrossing = 0
        self.current_assignment_address = 0

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

    def evaluate_expression(self, expression_string: str) -> float:
        """
        Parses and executes Arena formula strings against the simulation state.

        Args:
            expression_string: The Arena-formatted formula string.

        Returns:
            The evaluated result as a float.
        """
        if not expression_string or expression_string.strip() == "0":
            return 0.0

        processed = expression_string.strip()

        # Remove Eval(...) wrapper if it exists
        eval_match = re.match(r"^Eval\((.*)\)$", processed, re.IGNORECASE)
        if eval_match:
            processed = eval_match.group(1)

        # Translate Arena functions MN/MX to min/max
        processed = processed.replace("MN(", "min(").replace("MX(", "max(")

        # Convert 1-based parentheses indexing to 0-based bracket indexing
        # Patterns like drs_Level(X) -> drs_Level[X-1]
        def replace_index(match):
            prefix = match.group(1)
            index = int(match.group(2))
            return f"{prefix}[{index - 1}]"

        processed = re.sub(r"(drs_Level|drs_Timer)\((\d+)\)", replace_index, processed)

        # Local namespace for safe evaluation
        local_namespace = {
            "drs_Level": self.drs_Level,
            "drs_Timer": self.drs_Timer,
            "drs_RateConfigurationNumber": self.drs_RateConfigurationNumber,
            "min": min,
            "max": max,
            "MN": min,
            "MX": max,
        }

        try:
            # Safely evaluate the expression
            result = eval(processed, {"__builtins__": None}, local_namespace)
            return float(result)
        except Exception as e:
            # In a real scenario, we might want more specific error handling or logging
            raise ValueError(f"Error evaluating expression '{expression_string}': {e}")

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
            self.drs_DiscretelyDynamicalNumericalVariable[i] = self.evaluate_expression(
                self.confExString_InitialDiscretelyDynamicalNumericalVariableValue[i]
            )

        # Loop through categorical variables
        # Note: evaluate_expression currently returns float, but categorical might need strings.
        # For now, we follow the instruction to repeat the evaluation pattern.
        for i in range(self.dim_NumberOfCategoricalVariables):
            # evaluate_expression returns float, but CategoricalVariable is a list of strings
            # We'll need to decide if we want a separate evaluate_string_expression or just str() the result.
            # Given the instruction "Repeat this loop evaluation for... drs_CategoricalVariable",
            # and that categorical values are strings, we might need to handle this.
            # However, the prompt says "Repeat this loop evaluation ... using their respective Initial... string arrays".
            # If evaluate_expression is strictly numeric, we might have an issue here.
            # Let's check evaluate_expression again. It returns float(result).
            val = self.evaluate_expression(
                self.confExString_InitialCategoricalVariableValue[i]
            )
            self.drs_CategoricalVariable[i] = str(val)

    def characterize_thresholds(self):
        """
        Calculates the time until the next discrete event by evaluating all levels and timers
        against their respective thresholds based on current rates.
        """
        self.drs_DurationUntilThresholdCrossing = 99999.0
        rate_config = self.drs_RateConfigurationNumber

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

            if time_to_cross < self.drs_DurationUntilThresholdCrossing:
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

            if time_to_cross < self.drs_DurationUntilThresholdCrossing:
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

        rate_config = self.drs_RateConfigurationNumber

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

    def execute_assignments(self):
        """
        Parses and applies discrete instantaneous changes triggered by threshold events.
        Loops through the assignment sequence at current_assignment_address.
        """
        if self.current_assignment_address == 0:
            return

        # 1-based address to 0-based Python index
        addr_idx = self.current_assignment_address - 1

        # The assignment sequence is stored as Matrix[MaxLength][NumberOfAddresses]
        # We need to iterate through the sequence for the given address.
        for step in range(self.dim_MaxLengthOfAssignmentSequence):
            assignment_str = self.confExString_AssignmentSequence[step][addr_idx]
            if not assignment_str or assignment_str.strip() == "":
                continue

            assignment_str = assignment_str.strip()
            # Extract type identifier: 'L', 'T', 'N', 'C', or 'E'
            type_id = assignment_str[0].upper()

            # Extract 1-based target index (indices 1 to 3)
            # E.g., "L002=150" -> index "002" -> 2
            try:
                target_idx_1based = int(assignment_str[1:4])
            except (ValueError, IndexError):
                # If the string doesn't follow the "Xnnn=" format strictly, we might need more robust parsing.
                # But following instructions for extraction indices 1 to 3.
                continue

            target_idx = target_idx_1based - 1  # 0-based

            # Extract the expression (indices 5 onwards)
            # E.g., "L002=150" -> "=150" is at index 4 onwards, expression starts at 5
            expression = assignment_str[5:]

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
        Placeholder method for triggering custom VBA/Python logic.
        """
        # Simple match or if/elif block for future custom logic
        if code_number == 1:
            # Example logic for code 1
            pass
        elif code_number == 2:
            # Example logic for code 2
            pass
        else:
            # Default or unknown code logic
            pass

    def update_rate_configuration(self):
        """
        Shifts the system into its new state (rate configuration) based on the threshold crossed.
        """
        idx = self.drs_ThresholdCrossingLevelOrTimerNumber
        current_rate_config = self.drs_RateConfigurationNumber
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

        # Assign the new rate configuration
        self.drs_RateConfigurationNumber = new_rate_config
