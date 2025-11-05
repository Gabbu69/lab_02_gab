# Mealy to Moore Machine Conversion and Simulation
# Author: Edgardo Gariel L. Paclibar
# Course: 3/BSCS/A

from collections import defaultdict

# Step 1: Define the Mealy machine
mealy = {
    'A': {'0': ('A', 'A'), '1': ('A', 'B')},
    'B': {'0': ('B', 'C'), '1': ('A', 'D')},
    'C': {'0': ('C', 'D'), '1': ('C', 'B')},
    'D': {'0': ('D', 'B'), '1': ('B', 'C')},
    'E': {'0': ('E', 'D'), '1': ('C', 'E')},
}

initial_state = 'A'
inputs = ["00110", "11001", "1010110", "101111"]

# Step 2: Determine unique outputs entering each state
incoming_outputs = defaultdict(set)
for state, transitions in mealy.items():
    for inp, (next_state, output) in transitions.items():
        incoming_outputs[next_state].add(output)

# Step 3: Build Moore states (state_output) and their outputs
moore_states = []
moore_output = {}
for state, outputs in incoming_outputs.items():
    for out in outputs:
        new_state = f"{state}_{out}"
        moore_states.append(new_state)
        moore_output[new_state] = out

# Add the special start state
start_state = "S0"
moore_states.insert(0, start_state)
moore_output[start_state] = None

# Step 4: Create Moore transitions
moore_transitions = {s: {} for s in moore_states}

# Transitions from the start state
for inp, (next_state, output) in mealy[initial_state].items():
    moore_transitions[start_state][inp] = f"{next_state}_{output}"

# Transitions for all other Moore states
for moore_state in moore_states:
    if moore_state == start_state:
        continue
    state, _ = moore_state.split('_', 1)
    for inp, (next_state, output) in mealy[state].items():
        moore_transitions[moore_state][inp] = f"{next_state}_{output}"

# Step 5: Simulation function
def simulate_moore(input_string):
    current = start_state
    output_sequence = []
    for ch in input_string:
        current = moore_transitions[current][ch]
        output_sequence.append(moore_output[current])
    return "".join(output_sequence)

# Step 6: Run simulations
print("=== Mealy to Moore Machine Simulation ===")
for seq in inputs:
    print(f"Input: {seq}  ->  Output: {simulate_moore(seq)}")
