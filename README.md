# DES-milene: Discrete Rate Simulation (DRS) Framework

A Python-based framework for Discrete Rate Simulation, designed to emulate complex system behaviors often modeled in tools like Arena. This project provides a structured state machine for tracking levels, timers, and variables in a mining system context.

## Core Concepts

The simulation is built around the `DRSModel`, which manages the state of the system through several vectors:

- **Levels (`drs_Level`)**: Continuous variables that change at specific rates over time (e.g., Ore Extraction, Stock levels).
- **Timers (`drs_Timer`)**: Variables that track elapsed time in various modes or subsystems (e.g., Shutdown time, Mode A active time).
- **Discrete Variables (`drs_DiscretelyDynamicalNumericalVariable`)**: Numerical values that change discretely at event points (e.g., Parcel mass, Facies flags).
- **Categorical Variables (`drs_CategoricalVariable`)**: Discrete labels or status strings.
- **Configuration Expressions (`confExString_*`)**: Dynamic formulas (as strings) that dictate rates, thresholds, and initial values based on the current "Rate Configuration".

### Pythonic Aliases
To make the code more readable and aligned with the domain (mining), the `DRSModel` uses Python properties to alias raw array indices to meaningful names:
- `model.OreExtraction_Level` maps to `model.drs_Level[0]`
- `model.TimeInShutdown_Timer` maps to `model.drs_Timer[8]`

### Dynamic Formulas
The `DRSModel` includes extensive support for configuration expression strings, which allow the simulation logic to be defined dynamically:
- **Scalars**: Terminating conditions and initial rate configurations.
- **Vectors**: Initial values for levels, timers, and variables.
- **Matrices**: Level-specific and timer-specific rates, thresholds, and assignment sequences, indexed by "Rate Configuration".

## Installation

Ensure you have Python 3.8+ installed. Install the required dependencies:

```bash
pip install -r requirements.txt
```

*Note: The primary dependency is `numpy`.*

## Expected Usage

You can instantiate the `DRSModel` with default dimensions or provide custom overrides.

```python
from model.drs_model import DRSModel

# Initialize with default dimensions
model = DRSModel()

# Access and modify state using domain-specific aliases
model.OreExtraction_Level = 5000.0
print(f"Current Ore Extraction: {model.OreExtraction_Level}")

# The underlying NumPy arrays are updated automatically
print(f"Raw drs_Level[0]: {model.drs_Level[0]}")

# Custom initialization
custom_model = DRSModel(dim_NumberOfLevels=10, dim_NumberOfTimers=5)
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
