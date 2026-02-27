# DES-milene: Discrete Rate Simulation (DRS) Framework

A Python-based framework for Discrete Rate Simulation, designed to emulate complex system behaviors often modeled in tools like Arena. This project provides a structured state machine for tracking levels, timers, and variables in a mining system context.

## Core Concepts

The simulation is built around the `DRSModel`, which manages the state of the system through several vectors:

- **Levels (`drs_Level`)**: Continuous variables that change at specific rates over time (e.g., Ore Extraction, Stock levels).
- **Timers (`drs_Timer`)**: Variables that track elapsed time in various modes or subsystems (e.g., Shutdown time, Mode A active time).
- **Discrete Variables (`drs_DiscretelyDynamicalNumericalVariable`)**: Numerical values that change discretely at event points (e.g., Parcel mass, Facies flags).
- **Categorical Variables (`drs_CategoricalVariable`)**: Discrete labels or status strings.
- **Configuration Expressions (`confExString_*`)**: Dynamic formulas (as strings) that dictate rates, thresholds, and initial values based on the current "Rate Configuration".
- **Simulation Clock (`TNOW`)**: Current simulation time in days (defaults to 0.0).

## Model Configuration & Inputs

### Model Dimensions
When instantiating `DRSModel`, you define the size of the simulation state. These dimensions determine the shapes of all underlying arrays and matrices.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `dim_NumberOfLevels` | `int` | 5 | Number of continuous level variables. |
| `dim_NumberOfTimers` | `int` | 9 | Number of timer variables. |
| `dim_NumberOfDiscretelyDynamicalNumericalVariables` | `int` | 3 | Number of discrete numerical variables. |
| `dim_NumberOfCategoricalVariables` | `int` | 1 | Number of categorical variables. |
| `dim_NumberOfRateConfigurations` | `int` | 7 | Number of different rate configurations (e.g., Operating Modes). |
| `dim_NumberOfAssignmentSequenceAddresses` | `int` | 6 | Number of assignment addresses per sequence. |
| `dim_MaxLengthOfAssignmentSequence` | `int` | 7 | Maximum length of an assignment sequence. |

### Configuration Loading
The `load_configuration(config_dict)` method allows populating the `confExString_` attributes from an external source. It performs shape validation to ensure the input data matches the model's dimensions.

```python
model = DRSModel(dim_NumberOfLevels=2, dim_NumberOfRateConfigurations=3)
config_data = {
    "confExString_LevelRate": [
        ["0.5", "0.8", "0.0"], # Rates for Level 0 across 3 configurations
        ["0.2", "0.4", "0.1"]  # Rates for Level 1 across 3 configurations
    ],
    "confExString_TerminatingCondition": "time > 3600"
}
model.load_configuration(config_data)
```

### Simulation Initialization
Before the event loop begins, the model should be bootstrapped using `initialize_simulation()`. This method:
1. Resets `TNOW` to 0.0.
2. Sets `drs_TimeOfPreviousDRSUpdate` to `TNOW`.
3. Evaluates the initial configuration strings to set the starting levels, timers, discrete variables, and categorical variables.
4. Identifies the initial rate configuration number.

```python
model.initialize_simulation()
print(f"Simulation started at TNOW: {model.TNOW}")
```
 
## Expression Evaluation Engine
 
The `DRSModel` includes a robust engine for evaluating Arena-formatted expression strings against the simulation state. The `evaluate_expression(expression_string)` method handles preprocessing, indexing conversion, and safe execution.
 
### Features
- **Arena Syntax Support**: Automatically handles `Eval(...)` wrappers and translates `MN`/`MX` functions to Python's `min`/`max`.
- **1-Based Indexing Conversion**: Translates Arena-style 1-based indexing for Levels and Timers (e.g., `drs_Level(1)`) into Python's 0-based indexing (e.g., `drs_Level[0]`).
- **Safe Evaluation**: Executes expressions in a restricted namespace with access only to specific state vectors (`drs_Level`, `drs_Timer`), scalar variables (`drs_RateConfigurationNumber`), and mathematical functions.
 
### Example
```python
model.drs_Level[0] = 50.0
model.drs_Timer[4] = 10.0
# Arena formula: Eval(MX(drs_Level(1), drs_Timer(5) * 6))
result = model.evaluate_expression("Eval(MX(drs_Level(1), drs_Timer(5) * 6))")
# Evaluates MX(50.0, 10.0 * 6) -> 60.0
```

## Event Prediction (Characterizing Thresholds)

The core of the Discrete Rate Simulation is the ability to predict when the next state change will occur. The `characterize_thresholds()` method calculates the time until the next discrete event (e.g., a level hitting its capacity or a timer reaching its limit).

### How it Works
1. **Initializes Duration**: Starts with a large default value (`99999.0`).
2. **Evaluates Rates**: For every Level and Timer, it evaluates their current rate based on the active `drs_RateConfigurationNumber`.
3. **Calculates Time-to-Cross**: 
   - If `rate > 0`, it calculates the time to hit the `UpperThreshold`.
   - If `rate < 0`, it calculates the time to hit the `LowerThreshold`.
4. **Finds Minimum**: The absolute minimum time among all valid trajectories determines the next event.
5. **Updates Tracking Variables**:
   - `drs_DurationUntilThresholdCrossing`: The time until the next event.
   - `drs_ThresholdCrossingLevelOrTimerNumber`: The index of the variable that will cross.
   - `drs_ThresholdIsCrossedByTimer`: Flag (0 for level, 1 for timer).
   - `drs_DirectionOfThresholdCrossing`: Direction of change (-1 or 1).

```python
model.characterize_thresholds()
print(f"Next event in {model.drs_DurationUntilThresholdCrossing} days")
```

## Data Formatting Guide

Whether loading from JSON or Excel, the data must follow these structures:

### Scalars (Strings)
Attributes like `confExString_TerminatingCondition` expect a single string.

### Vectors (1D Lists of Strings)
Initial value arrays must have a length equal to the corresponding dimension.
- **Example**: `confExString_InitialLevelValue` should be `["val1", "val2", ...]` with length `dim_NumberOfLevels`.

### Matrices (2D Lists of Strings)
Most configuration strings are stored in matrices where rows correspond to a variable index and columns correspond to a **Rate Configuration**.
- **Format**: `List[List[str]]`
- **Shape**: `[VariableDimension][dim_NumberOfRateConfigurations]`
- **Example (`confExString_LevelRate`)**:
  ```json
  [
    ["L0_RC0", "L0_RC1", "L0_RC2"],
    ["L1_RC0", "L1_RC1", "L1_RC2"]
  ]
  ```

### Assignment Sequence
`confExString_AssignmentSequence` has a unique shape: `[dim_MaxLengthOfAssignmentSequence][dim_NumberOfAssignmentSequenceAddresses]`.

## Installation

Ensure you have Python 3.8+ installed. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running Tests

The project uses `pytest` for unit testing. The test suite covers state initialization and variable aliasing.

To run all tests:

```bash
pytest
```

To run a specific test file:

```bash
pytest tests/test_drs_model.py
```

### Coverage
- `tests/test_drs_init.py`: Verifies correct initialization of all state vectors, scalar variables, and the complex configuration expression string matrices.
- `tests/test_drs_aliases.py`: Ensures that properties correctly map to and mutate the underlying NumPy arrays.
- `tests/test_drs_config.py`: Validates the `load_configuration` method and its shape validation logic.
- `tests/test_drs_expressions.py`: Tests the Arena-to-Python expression translation and safe evaluation engine.
- `tests/test_drs_model.py`: Comprehensive suite verifying matrix initialization, configuration loading, and robust expression evaluation (math, Arena functions, and state variables).
- `tests/test_characterize_thresholds.py`: Verifies the logic for predicting next event times based on level and timer threshold crossings.
