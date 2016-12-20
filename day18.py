#!/usr/bin/env python

import pytest
import itertools

def iter_triples(row):
    """Iterate over triplets for a tile row."""
    yield ".", row[0], row[1]
    for i in range(len(row) - 2):
        yield row[i], row[i+1], row[i+2]
    yield row[i+1], row[i+2], "."
    

def apply_rules(left, center, right):
    """Apply the rules to the tiles."""
    if ((left == "^") ^ (right == "^")):
        return "^"
    return "."

@pytest.mark.parametrize("left, center, right, tile",[
    "^^.^",
    ".^^^",
    "^..^",
    "..^^",
    "....",
    "^^^.",
    "^.^."
])
def test_rules(left, center, right, tile):
    assert apply_rules(left, center, right) == tile

def iter_next_row(row):
    """Iterate, producing the next row."""
    for left, center, right in iter_triples(row):
        yield apply_rules(left, center, right)
    
def pytest_split_map(room):
    """For lines in a map, return pairs"""
    iterator = iter(room)
    previous = next(iterator).strip()
    for row in iterator:
        yield previous, row.strip()
        previous = row.strip()

BIGMAP = """
.^^.^.^^^^
^^^...^..^
^.^^.^.^^.
..^^...^^^
.^^^^.^^.^
^^..^.^^..
^^^^..^^^.
^..^^^^.^^
.^^^..^.^^
^^.^^^..^^
"""[1:-1]

@pytest.mark.parametrize("row, next_row",[
    ("..^^.", ".^^^^"),
    (".^^^^", "^^..^")
] + list(pytest_split_map(BIGMAP.splitlines())))
def test_next_row(row, next_row):
    assert "".join(iter_next_row(row)) == next_row

def rows_infinite(row):
    """Rows, infinitely"""
    for i in itertools.count():
        yield row
        row = "".join(iter_next_row(row))

def iter_safe(row):
    """Iterate over the number of safe tiles."""
    for row in rows_infinite(row):
        yield row.count(".")

def count_safe(row, nrows):
    """Count safe tiles"""
    return sum(itertools.islice(iter_safe(row), nrows))

def test_example_map():
    """Test the example map"""
    start = BIGMAP.splitlines()[0]
    assert count_safe(start, 10) == 38

INPUT = "^.^^^..^^...^.^..^^^^^.....^...^^^..^^^^.^^.^^^^^^^^.^^.^^^^...^^...^^^^.^.^..^^..^..^.^^.^.^......."
def puzzle1():
    """Number of safe spaces in 40 rows."""
    print("Puzzle #1")
    print(f"{count_safe(INPUT, 40):d} safe spaces in 40 rows.")

def puzzle2():
    """Number of safe spaces in 40 rows."""
    print("Puzzle #2")
    print(f"{count_safe(INPUT, 400000):d} safe spaces in 400000 rows.")


if __name__ == '__main__':
    puzzle1()
    puzzle2()