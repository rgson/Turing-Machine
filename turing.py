#!/usr/bin/env python3

################################################################################
# Turing Machine - Prototype                                                   #
# A virtual Turing Machine, with it's own basic programming language.          #
################################################################################


import argparse
import collections
import re


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("codefile",
                        help="executes the specified program",
                        type=argparse.FileType('r'))
    parser.add_argument("input",
                        help="the initial state of the tape",
                        nargs='?',
                        default="")
    return parser.parse_args()


def parse_code(codefile):
    states = {}
    start = None
    halt = None
    first = None
    last = None
    alphabet = set()
    states_referenced = set()
    for nr, line in enumerate(args.codefile):
        # Strip comments
        line = re.sub(r'//.*', '', line)
        # Clean up spaces
        line = re.sub(r'\s+', ' ', line)
        line = line.strip()
        # Skip empty lines
        if len(line) == 0:
            continue
        # Check for state definition
        match = re.match(r'^(\w+)( \[(\w+)\])?$', line)
        if match is not None:
            name, _, tag = match.groups()
            if name in states:
                raise Exception("Error (line {}): Duplicate state '{}'".format(nr, name))
            states[name] = {}
            last = name
            if first is None:
                first = name
            if tag == 'start':
                if start is not None:
                    raise Exception("Error (line {}): Duplicate [start] tag".format(nr))
                start = name
            elif tag == 'halt':
                if halt is not None:
                    raise Exception("Error (line {}): Duplicate [halt] tag".format(nr))
                halt = name
            continue
        # Check for instruction
        match = re.match(r'^(.) -> (.) ([LNR]) (\w+)$', line)
        if match is not None:
            read, write, move, transition = match.groups()
            alphabet |= {read, write}
            if last is None:
                raise Exception("Error (line {}): Orphan instruction".format(nr))
            if read in states[last]:
                raise Exception("Error (line {}): Duplicate instruction for symbol '{}' in state '{}'".format(nr, read, last))
            states[last][read] = (write, move, transition)
            states_referenced.add(transition)
            continue
        # No match
        raise Exception("Error (line {}): Invalid line".format(nr))
    # Implicit [start]
    if start is None:
        start = first
    # Implicit [halt]
    if halt is None:
        halt = 'halt'
        if halt in states:
            raise Exception("Error: cannot create implicit halt state due to name collision")
        states[halt] = {}
    # Sanity checks
    if start is None:
        raise Exception("Error: No start state")
    undefined_states = states_referenced - set(states)
    if len(undefined_states) > 0:
        raise Exception("Error: References to undefined states ({})".format(', '.join(undefined_states)))
    unused_states = set(states) - states_referenced
    if len(unused_states) > 0:
        print("Warning: Unused states ({})".format(', '.join(unused_states)))
    print("States:  {}".format(len(states)))
    print("Symbols: {}".format(len(alphabet)))
    return (states, start, halt)


def run_program(program, user_input):
    states, start_state, halt_state = program
    tape = collections.defaultdict(lambda: '_')
    if start_state is not None:
        tape.update(enumerate(user_input))
    position = 0
    state = start_state
    while state != halt_state:
        read = tape[position]
        if read not in states[state]:
            raise Exception("Reject (no instruction for symbol '{}' in state '{}')".format(read, state))
        write, move, transition = states[state][read]
        tape[position] = write
        position += 1 if move == 'L' else -1 if move == 'R' else 0
        state = transition
    return ''.join(item[1] for item in sorted(tape.items()))


if __name__ == "__main__":
    try:
        args = parse_args()
        print("Parsing code...")
        program = parse_code(args.codefile)
        print("Done!")
        print("Running program...")
        output = run_program(program, args.input)
        print("Done!")
        print("Output:")
        print(output)
    except Exception as e:
        print(e)
