#!/usr/bin/env python

import pytest
import re
import itertools

def is_open(time, index, offset, size):
    """Check if the disk is open."""
    return (time + index + offset) % size == 0

@pytest.mark.parametrize("time, index, offset, size, open",[
    (0, 1, 4, 5, True),
    (0, 2, 1, 2, False),
    (5, 1, 4, 5, True),
    (5, 2, 1, 2, True),
])
def test_disk_open(time, index, offset, size, open):
    assert is_open(time, index, offset, size) == open

DRE = re.compile(r'Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).')
def parse_disk(line):
    """docstring for parse_disk"""
    m = DRE.match(line)
    if not m:
        raise ValueError(f"Can't parse line {line}")
    return (int(m.group(1)), int(m.group(3)), int(m.group(2)))
    
def parse_disks(lines):
    """Parse all the disks."""
    for line in lines:
        yield parse_disk(line)
    
def find_opening(disks):
    """Find the first available opening."""
    for i in itertools.count():
        if all(is_open(i, *disk) for disk in disks):
            return i
    

EXAMPLE = """Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1."""

def test_example_q():
    disks = list(parse_disks(EXAMPLE.splitlines()))
    opening = find_opening(disks)
    assert opening == 5
    
INPUT = """\
Disc #1 has 13 positions; at time=0, it is at position 1.
Disc #2 has 19 positions; at time=0, it is at position 10.
Disc #3 has 3 positions; at time=0, it is at position 2.
Disc #4 has 7 positions; at time=0, it is at position 1.
Disc #5 has 5 positions; at time=0, it is at position 3.
Disc #6 has 17 positions; at time=0, it is at position 5."""
    
def puzzle1():
    """Puzzle 1"""
    print("Puzzle #1")
    disks = list(parse_disks(INPUT.splitlines()))
    opening = find_opening(disks)
    print(f"Push the button at time={opening:d}")
    
def puzzle2():
    """Puzzle 2"""
    print("Puzzle #2")
    disks = list(parse_disks(INPUT.splitlines())) + [(7, 0, 11)]
    opening = find_opening(disks)
    print(f"Push the button at time={opening:d}")
    
    
if __name__ == '__main__':
    puzzle1()
    puzzle2()