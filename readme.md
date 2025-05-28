# StellarXplorers Master Script

## Overview

This repository provides a **semi-automated optimization tool** for StellarXplorers mission prompts. It loads mission parameters from a YAML file, explores valid component combinations, and finds the best setup based on a chosen metric (e.g., coverage time, cost).

## Project Structure

```text
├── main.py         # Core optimizer (brute-force & greedy)
├── config.yaml     # Editable mission parameters
└── README.md       # This documentation
```

## Prerequisites

* **Python 3.x**
* **PyYAML** for YAML parsing:

  ```bash
  pip install pyyaml
  ```
* (Built-in) **argparse** and **csv**

## Configuration (`config.yaml`)

All mission inputs live here. To add a new subsystem, simply add a **component key** under `components` with its own `options` list.

### 1. `objective`

```yaml
objective:
  type: maximize        # or 'minimize'
  metric: coverage_time # any field present in options
```

### 2. `constraints`

```yaml
constraints:
  max_mass: 500  # total mass limit (kg)
  max_cost: 50   # total cost limit ($M)
```

### 3. `components`

Under this key, define each subsystem by its **component key** (e.g. `payload`, `power_system`, `comms`). Each must include:

* `options`: a list of choices
* Every option needs `name`, `mass`, `cost` and any metric fields (e.g. `coverage_time`)

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
      - name: camera_C     # add here without modifying main.py
        mass: 60
        cost: 6
        coverage_time: 2.8
  power_system:
    options:
      - name: solar_panel_small
        mass: 100
        cost: 2
        power_output: 1.5
```

## Usage

1. **Edit** `config.yaml` (objectives, constraints, components).
2. **Run**:

   ```bash
   python main.py \
     [--solver {brute_force,greedy}] \
     [--config config.yaml] \
     [--output results.csv]
   ```

   * `--solver greedy` uses a simple heuristic; default is exhaustive brute force.
3. **Inspect**

   * Console will show the best score and selections.
   * `results.csv` will contain a row per component plus summary.

## Winning Strategy

### Organizational Best Practices

* **Define Team Roles**: Assign a project lead, data analyst, mission designer, and script maintainer.
* **Schedule Regular Checkpoints**: Break preparation into milestones (e.g., prompt review, YAML setup, script validation).
* **Use Version Control**: Track changes to `config.yaml` and `main.py` with Git to revert if needed.
* **Conduct Mock Runs**: Simulate practice rounds on a strict timer to mirror competition constraints.
* **Document Decisions**: Record rationale for component choices and constraint settings for quick reviews during finals.

### Technical Methods

* **Analyze Past Prompts**: Review previous seasons’ rulebooks to anticipate scenario patterns.
* **Parameter Sensitivity**: Use the script to sweep key variables (e.g., max\_mass, objectives) and chart performance trends.
* **YAML Templates**: Maintain a library of reusable config snippets (e.g., typical payload setups).
* **Continuous Testing**: Automate unit tests for `is_valid` and `compute_score` to catch config typos early.
* **Hybrid Solver Approach**: Start with the greedy solver for quick baselines, then refine with brute force for critical subsystems.

## How It Works (`main.py`)

1. **load\_config**: reads YAML.
2. **is\_valid**: enforces `constraints`.
3. **compute\_score**: sums your chosen `metric`.
4. **brute\_force\_optimize**: checks all combos via `itertools.product`.
5. **greedy\_optimize**: picks top options per subsystem in metric order, respecting constraints.
6. **optimize**: dispatches to the chosen solver.
7. **main**: handles CLI args, runs optimization, prints & writes CSV.

## Extending

* **New Constraints**: add checks in `is_valid`.
* **Alternative Solvers**: drop in your own under `optimize()`.
* **Output Formats**: modify the CSV writer for JSON or other reports.

*Last updated: May 28, 2025*
