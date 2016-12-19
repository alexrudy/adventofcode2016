#!/usr/bin/env python
import pytest

def is_triangle(sides):
    """For sides, is it a triangle."""
    longest = max(sides)
    return sum(sides) > 2 * longest

@pytest.mark.parametrize("sides, result", [
    ((5,10,25), False),
    ((5,10,12), True)
])
def test_is_triangle(sides, result):
    """Test is triangle"""
    assert is_triangle(sides) == result

with open("day03_input.txt") as f:
    n_valid = sum(is_triangle([int(s) for s in l.split()]) for l in f)
print(f"There are {n_valid} valid triangles")

def split_triangles(lines):
    liter = iter(lines)
    while True:
        yield from zip(*[next(liter) for i in range(3)])
    
TRIANGLES="""101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603"""

def test_split_triangles():
    """Test splitting the triangles"""
    for sides in split_triangles((l.split() for l in TRIANGLES.splitlines())):
        assert len(set(s[0] for s in sides)) == 1
    
def stripped(lines):
    """docstring for stripped"""
    for line in lines:
        yield line.strip().split()
    
with open("day03_input.txt") as f:
    n_valid = sum(is_triangle([int(s) for s in l]) for l in split_triangles(stripped(f)))
print(f"There are {n_valid} valid triangles")