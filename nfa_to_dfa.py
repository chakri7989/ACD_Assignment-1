"""NFA TO DFA CONVERTER (SUBSET CONSTRUCTION)"""
from collections import deque

class NFAToDFAConverter:
    def __init__(self, nfa_states, alphabet, transitions, start_state, accept_states):
        self.nfa_states = set(nfa_states)
        self.alphabet = set(alphabet) - {'e'}  # Alphabet excludes epsilon
        self.nfa_transitions = transitions     # {(state, symbol): {next_states}}
        self.nfa_start = start_state
        self.nfa_accepts = set(accept_states)

    def epsilon_closure(self, states):
        """Finds all NFA states reachable via epsilon (e) transitions from a set of states."""
        stack = list(states)
        closure = set(states)
        while stack:
            state = stack.pop()
            next_states = self.nfa_transitions.get((state, 'e'), set())
            for nxt in next_states:
                if nxt not in closure:
                    closure.add(nxt)
                    stack.append(nxt)
        return frozenset(closure)

    def move(self, states, symbol):
        """Finds all NFA states reachable from a set of states on a given alphabet symbol."""
        result = set()
        for state in states:
            destinations = self.nfa_transitions.get((state, symbol), set())
            result.update(destinations)
        return frozenset(result)

    def convert(self):
        """Performs subset construction to convert NFA to DFA."""
        dfa_transitions = {}
        dfa_accept_states = set()

        # 1. The start state of DFA is the epsilon closure of NFA's start state
        dfa_start = self.epsilon_closure({self.nfa_start})

        unprocessed_states = deque([dfa_start])
        dfa_states = {dfa_start}

        # Mapping to give clean names to DFA subset states (e.g., A, B, C...)
        state_name_map = {dfa_start: "A"}
        counter = 1

        while unprocessed_states:
            current_subset = unprocessed_states.popleft()
            current_name = state_name_map[current_subset]

            # Check if this subset contains any NFA accept state
            if current_subset & self.nfa_accepts:
                dfa_accept_states.add(current_name)

            for symbol in sorted(list(self.alphabet)):
                # Compute transition: closure(move(current_subset, symbol))
                move_result = self.move(current_subset, symbol)
                next_subset = self.epsilon_closure(move_result)

                if not next_subset:
                    # Optional: Handle dead/trap states if needed, or skip empty sets
                    continue

                if next_subset not in dfa_states:
                    dfa_states.add(next_subset)
                    unprocessed_states.append(next_subset)
                    counter += 1
                    state_name_map[next_subset] = chr(ord('A') + (counter - 1) % 26) + (str(counter // 26) if counter > 26 else "")

                next_name = state_name_map[next_subset]
                dfa_transitions[(current_name, symbol)] = next_name

        # Format clean output states dictionary
        formatted_states = sorted(list(state_name_map.values()))
        formatted_accepts = sorted(list(dfa_accept_states))
        formatted_start = state_name_map[dfa_start]

        return formatted_states, sorted(list(self.alphabet)), dfa_transitions, formatted_start, formatted_accepts, state_name_map


def run():
    print("=== NFA to DFA Converter (Subset Construction) ===")
    alphabet = input("Enter NFA alphabet symbols (e.g. 0 1): ").split()
    states = input("Enter NFA state names (e.g. q0 q1 q2): ").split()
    start_state = input("Enter NFA start state: ").strip()
    accept_states = input("Enter NFA accept state(s): ").split()

    print("\nEnter NFA transitions. Type destination states separated by space (or press Enter if none):")
    transitions = {}
    symbols_to_ask = alphabet + ['e']
    for s in states:
        for sym in symbols_to_ask:
            dest = input(f"  δ({s}, {'ε' if sym == 'e' else sym}) -> ").strip()
            if dest:
                transitions[(s, sym)] = set(dest.split())

    converter = NFAToDFAConverter(states, alphabet, transitions, start_state, accept_states)
    dfa_states, dfa_alphabet, dfa_trans, dfa_start, dfa_accepts, mapping = converter.convert()

    print("\n" + "=" * 50)
    print("                 EQUIVALENT DFA RESULT")
    print("=" * 50)
    print(f"DFA States:     {dfa_states}")
    print(f"DFA Alphabet:   {dfa_alphabet}")
    print(f"DFA Start State:{dfa_start}")
    print(f"DFA Accept States: {dfa_accepts}")
    print("\nSubset Mapping (DFA State Name -> NFA State Subsets):")
    for subset, name in sorted(mapping.items(), key=lambda x: x[1]):
        sub_str = "{" + ", ".join(sorted(list(subset))) + "}" if subset else "{∅}"
        print(f"  {name} = {sub_str}")

    print("\nDFA Transition Table:")
    for s in dfa_states:
        for sym in dfa_alphabet:
            dest = dfa_trans.get((s, sym), "TRAP")
            print(f"  δ({s}, {sym}) -> {dest}")
    print("=" * 50)


if __name__ == "__main__":
    run()
