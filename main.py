import yaml
import itertools

# Load configuration from YAML file
def load_config(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

# Check constraints (mass, cost) for a given combination
def is_valid(combo, constraints):
    total_mass = sum(item['mass'] for item in combo)
    total_cost = sum(item['cost'] for item in combo)
    if 'max_mass' in constraints and total_mass > constraints['max_mass']:
        return False
    if 'max_cost' in constraints and total_cost > constraints['max_cost']:
        return False
    return True

# Compute score based on objective metric (e.g., coverage_time, cost, etc.)
def compute_score(combo, metric):
    return sum(item.get(metric, 0) for item in combo)

# Brute-force optimizer over all component options
def optimize(config):
    components = config['components']
    constraints = config.get('constraints', {})
    objective = config['objective']
    metric = objective['metric']  # e.g., 'coverage_time', 'cost'

    # Gather all option lists in order
    option_lists = [components[name]['options'] for name in components]

    best_score = None
    best_combo = None

    # Try every combination (for small sets this is fine)
    for combo in itertools.product(*option_lists):
        if not is_valid(combo, constraints):
            continue
        score = compute_score(combo, metric)
        if best_score is None:
            best_score = score
            best_combo = combo
        else:
            if objective['type'] == 'maximize' and score > best_score:
                best_score = score
                best_combo = combo
            elif objective['type'] == 'minimize' and score < best_score:
                best_score = score
                best_combo = combo

    return best_score, best_combo

# Entry point
def main():
    config = load_config('config.yaml')  # path to your YAML file
    best_score, best_combo = optimize(config)
    print(f"Best {config['objective']['type']} of '{config['objective']['metric']}': {best_score}")
    print("Selected components:")
    for comp in best_combo:
        print(f"- {comp['name']} (mass={comp['mass']}, cost={comp['cost']})")

if __name__ == '__main__':
    main()
