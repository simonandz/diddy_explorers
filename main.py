import yaml
import itertools
import csv
import argparse

def load_config(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def is_valid(combo, constraints):
    total_mass = sum(item['mass'] for item in combo)
    total_cost = sum(item['cost'] for item in combo)
    if 'max_mass' in constraints and total_mass > constraints['max_mass']:
        return False
    if 'max_cost' in constraints and total_cost > constraints['max_cost']:
        return False
    return True

def compute_score(combo, metric):
    return sum(item.get(metric, 0) for item in combo)

def brute_force_optimize(config):
    components = config['components']
    constraints = config.get('constraints', {})
    objective = config['objective']
    metric    = objective['metric']

    option_lists = [components[name]['options'] for name in components]
    best_score, best_combo = None, None

    for combo in itertools.product(*option_lists):
        if not is_valid(combo, constraints):
            continue
        score = compute_score(combo, metric)
        if best_score is None \
           or (objective['type'] == 'maximize' and score > best_score) \
           or (objective['type'] == 'minimize' and score < best_score):
            best_score, best_combo = score, combo

    return best_score, best_combo

def greedy_optimize(config):
    components = config['components']
    constraints = config.get('constraints', {})
    objective = config['objective']
    metric    = objective['metric']

    used_mass = 0
    used_cost = 0
    combo = []

    for name, comp in components.items():
        opts = comp['options']
        # sort by metric (high→low for maximize, low→high for minimize)
        reverse = objective['type'] == 'maximize'
        opts_sorted = sorted(opts, key=lambda x: x.get(metric, 0), reverse=reverse)

        for opt in opts_sorted:
            if used_mass + opt['mass'] <= constraints.get('max_mass', float('inf')) \
               and used_cost + opt['cost'] <= constraints.get('max_cost', float('inf')):
                combo.append(opt)
                used_mass += opt['mass']
                used_cost += opt['cost']
                break

    score = compute_score(combo, metric)
    return score, combo

def optimize(config, solver):
    if solver == 'greedy':
        return greedy_optimize(config)
    return brute_force_optimize(config)

def main():
    p = argparse.ArgumentParser(
        description="Optimize StellarXplorers mission design"
    )
    p.add_argument('--config', default='config.yaml',
                   help="path to YAML config")
    p.add_argument('--solver', choices=['brute_force','greedy'],
                   default='brute_force',
                   help="choose 'brute_force' or 'greedy' solver")
    p.add_argument('--output', default='results.csv',
                   help="CSV file to write results to")
    args = p.parse_args()

    config = load_config(args.config)
    best_score, best_combo = optimize(config, args.solver)
    metric = config['objective']['metric']
    objtype = config['objective']['type']

    # Print summary
    print(f"Best {objtype} of '{metric}': {best_score}")
    for item in best_combo:
        print(f"- {item['name']} (mass={item['mass']}, cost={item['cost']})")

    # Write CSV
    with open(args.output, 'w', newline='') as csvf:
        w = csv.writer(csvf)
        # header
        w.writerow(['component', 'selection', 'mass', 'cost', metric])
        for comp_name, item in zip(config['components'], best_combo):
            w.writerow([
                comp_name,
                item['name'],
                item['mass'],
                item['cost'],
                item.get(metric, '')
            ])
        w.writerow([])
        w.writerow([f"Objective ({objtype} {metric})", best_score])

    print(f"\nResults saved to {args.output}")

if __name__ == '__main__':
    main()
