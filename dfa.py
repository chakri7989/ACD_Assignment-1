"""
=============================================================================
DETERMINISTIC FINITE AUTOMATON (DFA) FORMAL DEFINITION (5-Tuple):
    M = (Q, Σ, δ, q0, F)
Where:
    1. Q   : Finite set of states                      -> list/set of state names
    2. Σ   : Finite set of input symbols (Alphabet)    -> set of valid symbols
    3. δ   : Transition function: Q × Σ -> Q           -> transitions[(state, symbol)] = next_state
    4. q0  : Initial / Start state (q0 ∈ Q)           -> start_state
    5. F   : Set of Final / Accept states (F ⊆ Q)     -> accept_states
=============================================================================
"""
class UniversalDFA:

  def __init__(self, states, alphabet, transitions, start_state, accept_states):
    self.states = list(states)
    self.alphabet = set(alphabet)
    self.transitions = transitions  # {(state, symbol): next_state}
    self.start_state = start_state
    self.accept_states = set(accept_states)

  def simulate(self, input_string):
    current_state = self.start_state
    path = [(current_state, None)]  # (state, symbol_consumed)

    for char in input_string:
      if char not in self.alphabet:
        return False, path, f"Invalid symbol '{char}' not in alphabet."
      transition_key = (current_state, char)
      if transition_key not in self.transitions:
        return False, path, f"No transition defined for ({current_state}, {char})."

      current_state = self.transitions[transition_key]
      path.append((current_state, char))

    is_accepted = current_state in self.accept_states
    return is_accepted, path, None

  def print_diagram(self):
    print("\n" + "=" * 45)
    print("           DFA TRANSITION TABLE")
    print("=" * 45)
    sorted_alpha = sorted(list(self.alphabet))
    header = f"{'State':^12} | " + " | ".join(
        [f"Input '{a}':^10" for a in sorted_alpha]
    )
    print(header)
    print("-" * len(header))

    for s in self.states:
      prefix = "-> " if s == self.start_state else "   "
      suffix = " *" if s in self.accept_states else "  "
      row_state = f"{prefix}{s}{suffix}"

      row_vals = []
      for a in sorted_alpha:
        dest = self.transitions.get((s, a), "DEAD")
        row_vals.append(f"{dest:^10}")

      print(f"{row_state:<12} | " + " | ".join(row_vals))
    print("=" * 45)
    print("Legend: '->' = Start State, '*' = Accept State\n")

  def draw_execution_trace(self, path, is_accepted):
    print("\n" + "-" * 50)
    print("             VISUAL STATE FLOW")
    print("-" * 50)

    for i, (state, symbol) in enumerate(path):
      is_accept = " [ACCEPT]" if state in self.accept_states else ""
      is_start = " (START)" if i == 0 else ""

      if i == 0:
        print(f"  +-------------------------+")
        print(f"  | Current State: {state:<7}{is_start:<8}|")
        print(f"  +-------------------------+")
      else:
        print(f"             |")
        print(f"        Read: [{symbol}]")
        print(f"             v")
        print(f"  +-------------------------+")
        print(f"  | State: {state:<9}{is_accept:<8} |")
        print(f"  +-------------------------+")

    status = (
        " ACCEPTED (Valid Member)" if is_accepted else " REJECTED (Invalid)"
    )
    print("-" * 50)
    print(f" Final Verdict: {status}")
    print("-" * 50 + "\n")


def run():
  print("=== Universal DFA Simulator (No External Libraries) ===")
  alphabet = input("Enter alphabet symbols (e.g. 0 1): ").split()
  states = input("Enter state names (e.g. q0 q1): ").split()
  start_state = input("Enter start state: ").strip()
  accept_states = input("Enter accept state(s): ").split()

  print("\nEnter transitions:")
  transitions = {}
  for s in states:
    for a in alphabet:
      dest = input(f"  δ({s}, {a}) -> ").strip()
      transitions[(s, a)] = dest

  dfa = UniversalDFA(states, alphabet, transitions, start_state, accept_states)
  dfa.print_diagram()

  while True:
    test_str = input(
        "Enter string to test (or 'exit' to quit): "
    ).strip()
    if test_str.lower() == "exit":
      break

    accepted, path, error = dfa.simulate(test_str)
    if error:
      print(f"\n[!] Error: {error}\n")
    else:
      dfa.draw_execution_trace(path, accepted)


if __name__ == "__main__":
  run()
