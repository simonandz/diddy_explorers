# StellarXplorers Master Script

## Overview

This repository provides a **semi-automated optimization tool** for StellarXplorers mission design prompts. It loads mission parameters from a YAML configuration file, explores all valid component combinations, and finds the optimum setup based on a user-defined metric (e.g., coverage time, cost).

## Project Structure

```
├── main.py         # Core optimizer script
├── config.yaml     # User-editable mission parameters
└── README.md       # This documentation
```

## Prerequisites

* **Python 3.x**
* **PyYAML** library for YAML parsing

Install requirements via:

```bash
pip install pyyaml
```

## Configuration (`config.yaml`)

All mission-specific inputs live here. Modify fields each competition season:

### 1. `objective`

* **type**: `maximize` or `minimize`
* **metric**: the key to optimize (must match a field in each component option)

```yaml
objective:
  type: maximize        # or 'minimize'
  metric: coverage_time # e.g. coverage_time, cost, data_rate
```

### 2. `constraints`

Optional global limits:

* `max_mass`: total mass limit (same units as component masses)
* `max_cost`: total budget limit (same units as component costs)

```yaml
constraints:
  max_mass: 500  # kg
  max_cost: 50   # $M
```

### 3. `components`

Define each subsystem and its available `options`. Every option must include:

* `name`: descriptive identifier
* `mass` and `cost` fields
* Any additional metric fields referenced by `objective.metric` or future constraints

```yaml
components:
  payload:
    options:
      - name: camera_A
        mass: 50
        cost: 5
        coverage_time: 2.5
      - name: camera_B
        mass: 75
        cost: 7
        coverage_time: 3.0
  power_system:
    options:
      - name: solar_panel_small
        mass: 100
        cost: 2
        power_output: 1.5
```

*To adapt for a new year, update any of these sections: objectives, constraints, or component lists.*

## Usage

1. **Edit** `config.yaml` to match the current prompt requirements.
2. **Run** the optimizer:

   ```bash
   python main.py
   ```
3. **Review** console output for:

   * Best objective value (e.g., max coverage)
   * List of selected component options with their `name`, `mass`, and `cost`.

## How It Works (`main.py`)

1. **load\_config**: Reads YAML into a Python dict.
2. **is\_valid**: Checks each combo against `constraints`.
3. **compute\_score**: Sums the chosen `metric` across components.
4. **optimize**: Brute-forces all combinations via `itertools.product`, tracking the best combo per `objective.type`.
5. **main**: Orchestrates loading, optimizing, and printing results.

## Extending the Script

* **New Constraints**: Add checks in `is_valid` (e.g., power budget).
* **Alternative Solvers**: Replace brute force with greedy, genetic, or simulated-annealing algorithms for larger option spaces.
* **Reporting**: Integrate CSV or JSON output for downstream analysis.

---

*Last updated: May 28, 2025*
