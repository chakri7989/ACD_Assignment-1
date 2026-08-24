import math

# NFA to DFA conversion using Bitmasking

# -------------------------------
# Input
# -------------------------------

st = int(input("Enter the number of states: "))

print(f"State numbers are from 0 to {st - 1}")

fin = int(input("Enter number of final states: "))

print("Enter final states:")
f = list(map(int, input().split()))

rel = int(input("Enter the number of rules according to NFA: "))

print('\nDefine transition rule as "initial state input symbol final state"')
print("Input symbol: 0 or 1")

# dfa[state][input] = list of destination states
dfa = [[[0 for _ in range(st)] for _ in range(2)] for _ in range(st)]

for _ in range(rel):
    p, q, r = map(int, input().split())

    if q == 0:
        dfa[p][0][r] = 1
    else:
        dfa[p][1][r] = 1


# -------------------------------
# Bitmasking
# -------------------------------

# state[mask] tells whether a DFA state exists
state = [0] * (1 << st)

# go[mask][input] = destination DFA state
go = [[0, 0] for _ in range(1 << st)]

# arr stores newly discovered DFA states
arr = []

# -------------------------------
# Initial state
# -------------------------------

in_state = int(input("Enter initial state: "))

initial = 1 << in_state

# Mark individual NFA states
for i in range(st):
    state[1 << i] = 1


# -------------------------------
# Generate transitions for
# individual NFA states
# -------------------------------

print("\nSolving according to DFA")

for i in range(st):

    for j in range(2):

        stf = 0

        for k in range(st):

            if dfa[i][j][k] == 1:
                stf = stf + (1 << k)

        go[1 << i][j] = stf

        print(f"{1 << i}-{j} --> {stf}")

        if state[stf] == 0:
            arr.append(stf)

        state[stf] = 1


# -------------------------------
# Generate transitions for
# compound DFA states
# -------------------------------

i = 0

while i < len(arr):

    current = arr[i]

    print(f"for {current} ---- ", end="")

    for j in range(2):

        new_state = 0

        for k in range(st):

            # Check whether qk is present
            # in the current DFA state
            if current & (1 << k):

                h = 1 << k

                # Union of transitions
                new_state = new_state | go[h][j]

        go[current][j] = new_state

        print(f"{j} -> {new_state} ", end="")

        if state[new_state] == 0:
            arr.append(new_state)
            state[new_state] = 1

    print()

    i += 1


# -------------------------------
# Display DFA transition table
# -------------------------------

print("\nThe total number of distinct states are:\n")

print("STATE\t\t0\t1")

for mask in range(1 << st):

    if state[mask] == 1:

        # Display state names
        if mask == 0:
            print("Φ", end="")
        else:
            for j in range(st):
                if mask & (1 << j):
                    print(f"q{j}", end=" ")

        print(f"\t\t{go[mask][0]}\t{go[mask][1]}")


# -------------------------------
# Test three strings
# -------------------------------

for _ in range(3):

    string = input("\nEnter string: ")

    current = initial

    print("\nString takes the following path -->")
    print(current, end="")

    for ch in string:

        symbol = int(ch)

        current = go[current][symbol]

        print(f" -> {current}", end="")

    print()

    print(f"Final state - {current}")

    # Check whether current DFA state
    # contains at least one NFA final state

    flag = False

    for final_state in f:

        if current & (1 << final_state):
            flag = True
            break

    if flag:
        print("\nString Accepted")
    else:
        print("\nString Rejected")
