#!/usr/bin/env python

import collections

def signal(lines, index=0):
    """Find the signal from a series of lines."""
    counters = None
    for line in lines:
        if not counters:
            counters = [collections.Counter() for _ in line.strip()]
        for i, c in enumerate(line.strip()):
            counters[i][c] += 1
    return "".join(counter.most_common()[index][0] for counter in counters)

SIGNAL="""eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
"""

def test_signal():
    """Test constructing a signal."""
    assert signal(SIGNAL.splitlines()) == "easter"
    
def test_signal_modified():
    """Test the modified signal"""
    assert signal(SIGNAL.splitlines(), -1) == "advent"
    

if __name__ == '__main__':
    
    print("Puzzle #1")
    with open("day06_input.txt") as f:
        print(signal(f))
    
    print("Puzzle #2")
    with open("day06_input.txt") as f:
        print(signal(f, -1))