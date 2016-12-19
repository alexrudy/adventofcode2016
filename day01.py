#!/usr/bin/env python

import pytest

def steps(directions):
    """Parse a set of directions into steps."""
    for step in directions.split(","):
        step = step.strip()
        yield step[0], int(step[1:])
    
def test_steps():
    """Test steps"""
    assert list(steps("R1, L3, R10, L20")) == [("R", 1),("L", 3), ("R", 10), ("L", 20)]
    
MATRIX = {}
MATRIX['R'] = [[0, -1], [  1, 0]]
MATRIX['L'] = [[0,  1], [ -1, 0]]

def vdot(v, m):
    """Vector dot product"""
    vx, vy = v
    ox = (vx * m[0][0]) + (vy * m[1][0])
    oy = (vx * m[0][1]) + (vy * m[1][1])
    return [ox, oy]
    
def walk(directions):
    """Walk through some directions."""
    x, y = (0, 0)
    v = [0, 1]
    for turn, distance in steps(directions):
        v = vdot(v, MATRIX[turn])
        for i in range(distance):
            x += v[0]
            y += v[1]
            yield (x, y)
    
def final_place(directions):
    for x, y in walk(directions):
        pass
    return x, y
    
@pytest.mark.parametrize("directions,result", [
    ("R2, L3", (2, 3)),
    ("R2, R2, R2", (0, -2)),
    ("R5, L5, R5, R3", (10, 2)),
])
def test_final_place(directions, result):
    assert final_place(directions) == result
    
def distance_to(position):
    return abs(position[0]) + abs(position[1])
    
# Puzzle 1
final = final_place(open('day01_input.txt').read().strip())
print(f"Puzzle 1: {final}, therefore {distance_to(final)}")
    
def first_duplicate(places):
    """Break on the first place we visit twice."""
    visited = set()
    for place in places:
        if place in visited:
            return place
        visited.add(place)
    else:
        raise ValueError(f"Didn't visit anywhere twice. Visited {visited}")
    
def test_first_duplicate():
    assert first_duplicate(walk("R8, R4, R4, R8")) == (4, 0)
    
# Puzzle 2
duplicate = first_duplicate(walk(open('day01_input.txt').read().strip()))
print(f"Puzzle 2: {duplicate}, therefore {distance_to(duplicate)}")