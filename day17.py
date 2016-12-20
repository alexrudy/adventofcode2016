#!/usr/bin/env python

import hashlib
import itertools
import collections
import pytest

def itermoves(position):
    """Iterate through possible moves."""
    x, y = position
    if y > 1:
        yield ("U", (x, y - 1), 0)
    if y < 4:
        yield ("D", (x, y + 1), 1)
    if x > 1:
        yield ("L", (x - 1, y), 2)
    if x < 4:
        yield ("R", (x + 1, y), 3)
    
OPEN = set("bcdef")
def unlocked(moves, path, salt):
    """Iterate over only unlocked."""
    digest = hashlib.md5(salt.encode("ascii") + path.encode("ascii")).hexdigest()
    for direction, destination, index in moves:
        if digest[index] in OPEN:
            yield (direction, destination)
        
    
@pytest.mark.parametrize("start, path, open",[
    ((1,1), "", "D"),
    ((1,2), "D", "RU"),
    ((1,1), "DU", "R"),
    ((2,1), "DUR", ""),
])
def test_unlocked(start, path, open):
    """Test the list of unlocked doors."""
    assert set(d for d, _ in unlocked(itermoves(start), path, "hijkl")) == set(open)

def search(salt, target=(4,4), start=(1,1)):
    """Search for a done state."""
    to_check = collections.deque(unlocked(itermoves(start), "", salt))
    generation = 0
    path = []
    for gen in itertools.count(1):
        next_to_check = []
        while len(to_check):
            path, position = to_check.popleft()
            if position == target:
                yield path
            else:
                for direction, destination in unlocked(itermoves(position), path, salt):
                    next_to_check.append((path + direction, destination))
        to_check.extend(next_to_check)
        if not len(to_check):
            break
        
    

@pytest.mark.parametrize("salt, path",[
    ("ihgpwlah", "DDRRRD"),
    ("kglvqrro", "DDUDRLRRUDRD"),
    ("ulqzkmiv", "DRURDRUDDLLDLUURRDULRLDUUDDDRR")
])
def test_search(salt, path):
    """Test search"""
    assert next(itertools.islice(search(salt), 1)) == path
    
INPUT = "hhhxzeay"
def puzzle1():
    print("Puzzle #1")
    print(next(search(INPUT)))
    
@pytest.mark.parametrize("salt, length",[
    ("ihgpwlah", 370),
    ("kglvqrro", 492),
    ("ulqzkmiv", 830)
])
def test_longest(salt, length):
    """Test the longest path."""
    assert max(len(p) for p in search(salt)) == length

def puzzle2():
    print("Puzzle #1")
    lp = max(len(p) for p in search(INPUT))
    print(f"The longest path is {lp:d} long.")
    

if __name__ == '__main__':
    puzzle1()
    puzzle2()