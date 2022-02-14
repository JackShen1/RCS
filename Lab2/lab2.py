import networkx as nx
import numpy as np
from itertools import product


def format_path_value(value: int) -> str:
    if value == 0:
        return "\tIN"
    elif value == len(table) - 1:
        return "OUT"
    return f"E{value}"


def get_data(filename: str) -> tuple[np.ndarray, np.ndarray]:
    all_data = np.loadtxt(filename, dtype=float, delimiter=",", skiprows=1)

    return all_data[:-1], all_data[-1]


def get_states(paths: list[list[int]]) -> list[list[int]]:
    all_working_states = []
    all_states = [list(x) for x in product(range(2), repeat=len(table))]
    for state in all_states:
        for path in paths:
            count = 0
            for n in path:
                if state[n] == 1:
                    count += 1

            if count == len(path):
                all_working_states.append(state)
                break

    return all_working_states


def get_probs(all_working_states: list[list[int]], probs: np.ndarray) -> list[float]:
    probability = []
    for binary_state in all_working_states:
        state_prob = 1
        for i, state in enumerate(binary_state):
            state_prob *= abs(1 - state - probs[i])
        probability.append(state_prob)
    return probability


table, probabilities = get_data(filename="topology.txt")
G = nx.DiGraph(table)

all_paths = list(nx.all_simple_paths(G, source=0, target=len(G) - 1))
print(f"\033[1mКількість можливих шляхів\033[0m: {len(all_paths)}\n\033[1mМожливі шляхи\033[0m:")
for path in all_paths:
    print(" -> ".join(map(format_path_value, path)))

working_states = get_states(paths=all_paths)
print(f"\n\033[1mКількість можливих робочих станів\033[0m: {len(working_states)}")

probabilities = get_probs(all_working_states=working_states, probs=probabilities)
header = "| " + " | ".join([f"E{i}" for i in range(1, len(table) - 1)] + [""]) + "P".center(10) + "|"
print(f'\033[1mВсі робочі стани та їх ймовірність\033[0m:\n{"-" * len(header)}\n{header}\n{"-" * len(header)}')
for bin_state, st_prob in zip(working_states, probabilities):
    print("| " + "  | ".join(list(map(str, bin_state[1:-1])) + [""]) + f"{st_prob:.6f}".center(10) + "|")

print(f'{"-" * len(header)}\n\n'
      f'\033[1mЙмовірність безвідмовної роботи системи\033[0m: {sum(probabilities):.6f}')
