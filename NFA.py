"""
=============================================================================
NONDETERMINISTIC FINITE AUTOMATON (NFA) FORMAL DEFINITION (5-Tuple):
    M = (Q, Σ, δ, q0, F)
Where:
    1. Q   : Finite set of states                      -> set of state names
    2. Σ   : Finite set of input symbols (Alphabet)    -> set of symbols (excluding 'e')
    3. δ   : Transition function: Q × (Σ ∪ {ε}) -> P(Q) -> transitions[(state, symbol)] = {next_states}
    4. q0  : Initial / Start state (q0 ∈ Q)           -> start_state
    5. F   : Set of Final / Accept states (F ⊆ Q)     -> accept_states
=============================================================================
"""

from collections import defaultdict

class UniversalNFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.transitions = transitions  # {(state, symbol): {next_states}}
        self.start_state = start_state
        self.accept_states = set(accept_states)

    def epsilon_closure(self, states):
        """Finds all states reachable via epsilon (e) transitions."""
        stack = list(states)
        closure = set(states)
        while stack:
            state = stack.pop()
            next_states = self.transitions.get((state, 'e'), set())
            for nxt in next_states:
                if nxt not in closure:
                    closure.add(nxt)
                    stack.append(nxt)
        return closure

    def simulate(self, input_string):
        # Start state with epsilon closure
        current_states = self.epsilon_closure({self.start_state})
        history = [(current_states, None)]

        for char in input_string:
            if char not in self.alphabet:
                return False, history, f"Invalid symbol '{char}' not in alphabet."

            next_states = set()
            for state in current_states:
                # Direct transitions on symbol
                direct = self.transitions.get((state, char), set())
                # Follow epsilon transitions from destinations
                next_states.update(self.epsilon_closure(direct))

            current_states = next_states
            history.append((current_states, char))
            if not current_states:
                break  # All branches died

        is_accepted = bool(current_states & self.accept_states)
        return is_accepted, history, None

    def print_diagram(self):
        print("\n" + "=" * 55)
        print("                 NFA TRANSITION TABLE")
        print("=" * 55)
        symbols = sorted(list(self.alphabet)) + (['e'] if any(k[1] == 'e' for k in self.transitions) else [])
        header = f"{'State':^12} | " + " | ".join([f"'{s}':^8" for s in symbols])
        print(header)
        print("-" * len(header))

        for s in sorted(self.states):
            prefix = "-> " if s == self.start_state else "   "
            suffix = " *" if s in self.accept_states else "  "
            row_state = f"{prefix}{s}{suffix}"

            row_vals = []
            for sym in symbols:
                dest_set = self.transitions.get((s, sym), set())
                dest_str = "{" + ",".join(sorted(dest_set)) + "}" if dest_set else "∅"
                row_vals.append(f"{dest_str:^8}")

            print(f"{row_state:<12} | " + " | ".join(row_vals))
        print("=" * 55)
        print("Legend: '->' = Start State, '*' = Accept State, 'e' = Epsilon (ε)\n")

    def draw_execution_trace(self, history, is_accepted):
        print("\n" + "-" * 55)
        print("           PARALLEL BRANCH EXECUTION FLOW")
        print("-" * 55)

        for i, (states, symbol) in enumerate(history):
            states_str = "{" + ", ".join(sorted(states)) + "}" if states else "{ DEAD / NO PATH }"
            accept_hits = states & self.accept_states
            accept_badge = f" [ACCEPTS: {', '.join(accept_hits)}]" if accept_hits else ""

            if i == 0:
                print(f"  +---------------------------------------------+")
                print(f"  | Active States: {states_str:<29}|")
                print(f"  +---------------------------------------------+")
            else:
                print(f"                     |")
                print(f"                Read: [{symbol}]")
                print(f"                     v")
                print(f"  +---------------------------------------------+")
                print(f"  | Active States: {states_str:<29}{accept_badge}")
                print(f"  +---------------------------------------------+")

        status = "ACCEPTED (At least one active path reached accept state)" if is_accepted else "REJECTED (No path reached accept state)"
        print("-" * 55)
        print(f" Final Verdict: {status}")
        print("-" * 55 + "\n")


def run():
    print("=== Universal NFA Simulator ===")
    alphabet = input("Enter alphabet symbols (e.g. 0 1): ").split()
    states = input("Enter state names (e.g. q0 q1 q2): ").split()
    start_state = input("Enter start state: ").strip()
    accept_states = input("Enter accept state(s): ").split()

    print("\nEnter transitions. Type destination states separated by space (or press Enter if none):")
    transitions = defaultdict(set)

    symbols_to_ask = alphabet + ['e']  # 'e' for epsilon
    for s in states:
        for sym in symbols_to_ask:
            dest = input(f"  δ({s}, {'ε' if sym == 'e' else sym}) -> ").strip()
            if dest:
                transitions[(s, sym)] = set(dest.split())

    nfa = UniversalNFA(states, alphabet, transitions, start_state, accept_states)
    nfa.print_diagram()

    while True:
        test_str = input("Enter string to test (or 'exit' to quit): ").strip()
        if test_str.lower() == "exit":
            break

        accepted, history, error = nfa.simulate(test_str)
        if error:
            print(f"\n[!] Error: {error}\n")
        else:
            nfa.draw_execution_trace(history, accepted)


if __name__ == "__main__":
    run()
