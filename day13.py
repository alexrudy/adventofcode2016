#!/usr/bin/env python
import collections
import pytest

def binary_ones(num):
    """ones"""
    return bin(num)[2:].count('1')
    
def is_wall(x, y, special):
    """Is this a wall?"""
    n = x*x + 3*x + 2*x*y + y + y*y + special
    return (binary_ones(n) % 2) == 1

@pytest.mark.parametrize("x,y,special,result",
    [(i, 0, 10, c == "#") for i, c in enumerate(".#.####.##")]
)
def test_is_wall(x, y, special, result):
    assert is_wall(x, y, special) == result

def moves(x, y):
    """Possible moves from x, y"""
    if x > 0:
        yield (x - 1, y)
    if y > 0:
        yield (x, y - 1)
    yield (x + 1, y)
    yield (x, y + 1)
    
def open_moves(x, y, special):
    """Yield only available moves."""
    for nx, ny in moves(x, y):
        if not is_wall(nx, ny, special):
            yield (nx, ny)
        
    
def forward_moves(x, y, special, path):
    """Prevent backtracking."""
    for nx, ny in open_moves(x, y, special):
        if (nx, ny) not in path:
            yield (nx, ny)
        
    
def walk(special, target, start=(1,1)):
    """Walk an area searching for a target."""
    paths = {start:[start]}
    to_check = collections.deque([start])
    while len(to_check):
        position = to_check.popleft()
        path = paths[position]
        for move in forward_moves(*position, special, path):
            if move not in path:
                paths[move] = path + [move]
                to_check.append(move)
            elif len(paths[move]) > len(path) + 1:
                paths[move] = path + [move]
        if target in paths:
            return paths[target]
        
    
def explore(special, distance, start=(1,1)):
    """Explore"""
    paths = {start:[start]}
    to_check = collections.deque([start])
    while len(to_check):
        position = to_check.popleft()
        path = paths[position]
        if len(path) > distance:
            continue
        for move in forward_moves(*position, special, path):
            if move not in path:
                paths[move] = path + [move]
                to_check.append(move)
            elif len(paths[move]) > len(path) + 1:
                paths[move] = path + [move]
    return paths
    
def test_example():
    """Test the example"""
    assert len(walk(10, (7, 4))) - 1 == 11
    
def puzzle1():
    """First puzzle."""
    print("Puzzle #1")
    nsteps = len(walk(1362, (31,39))) - 1
    print(f"It takes {nsteps:,d} steps to reach 31,39 with a magic number of 1362.")
    
def puzzle2():
    """Second puzzle, explore."""
    print("Puzzle #2")
    nstops = len(explore(1362, 50))
    print(f"You can visit {nstops:,d} stops in 50 steps with a magic number of 1362.")
    
    
if __name__ == '__main__':
    puzzle1()
    puzzle2()
