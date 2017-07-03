#!/usr/bin/env python3

################################################################################
# Turing Machine - Prototype                                                   #
# A virtual Turing Machine, with it's own basic programming language.          #
################################################################################

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("codefile",
                    help="executes the specified program",
                    type=argparse.FileType('r'))
parser.add_argument("input",
                    help="the initial state of the tape")
args = parser.parse_args()

# Parse

states = {}
start = None
halt = None
first = None
last = None
alphabet = set()

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
    match = re.match(r'^(.) -> (.) ([LSR]) (\w+)$', line)
    if match is not None:
        read, write, move, transition = match.groups()
        alphabet |= {read, write}
        if last is None:
            raise Exception("Error (line {}): Orphan instruction".format(nr))
        if read in states[last]:
            raise Exception("Error (line {}): Duplicate instruction for symbol '{}' in state '{}'".format(nr, read, last))
        states[last][read] = (write, move, transition)
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

# Sanity check
if start is None:
    raise Exception("Error: No start state")

print("States:  {}".format(len(states)))
print("Symbols: {}".format(len(alphabet)))
