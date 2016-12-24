#!/usr/bin/env python

import pytest
import re
import itertools

def swap_position(s, x, y):
    """Swap two positions in S."""
    s[x], s[y] = s[y], s[x]
    return s

@pytest.mark.parametrize("s, x, y, r",[
    ("abcdefgh", 3, 0, "dbcaefgh"),
    ("abcdefgh", 0, 3, "dbcaefgh")
])
def test_swap_positions(s, x, y, r):
    assert "".join(swap_position(list(s), x, y)) == r

def swap_letters(s, a, b):
    """Swap two letters"""
    t = str.maketrans(f"{a}{b}",f"{b}{a}")
    return [ si.translate(t) for si in s ]
    
@pytest.mark.parametrize("s, a, b, r",[
    ("abcdefgh", "d", "a", "dbcaefgh"),
    ("abcdefgh", "a", "d", "dbcaefgh")
])
def test_swap_letters(s, a, b, r):
    assert "".join(swap_letters(list(s), a, b)) == r
    
def rotate_left(s, n):
    """Rotate the string."""
    n = n % len(s)
    return s[n:] + s[:n]

@pytest.mark.parametrize("s, n, r",[
    ("abcdefgh", 4, "efghabcd"),
    ("abcdefgh", 9, "bcdefgha")
])
def test_rotate_left(s, n, r):
    assert "".join(rotate_left(list(s), n)) == r
    
# abcd -> dabc
def rotate_right(s, n):
    """Rotate to the right."""
    n = n % len(s)
    return s[-n:] + s[:-n]
    
@pytest.mark.parametrize("s, n, r",[
    ("abcdefgh", 4, "efghabcd"),
    ("abcdefgh", 9, "habcdefg"),
    ("abcd", 1, "dabc"),
])
def test_rotate_right(s, n, r):
    assert "".join(rotate_right(list(s), n)) == r

def rotate_letter(s, l):
    """Rotate according to a letter."""
    n = s.index(l) + 1
    if n >= 5:
        n += 1
    return rotate_right(s, n)

@pytest.mark.parametrize("s, l, r",[
    ("abcdefgh", "c", "fghabcde"),
    ("abcdefgh", "f", "bcdefgha"),
])
def test_rotate_letter(s, l, r):
    assert "".join(rotate_letter(list(s), l)) == r

def invert_rotate_letter(s, l):
    """Invert an action which rotates based on the index of a letter."""
    so = s[:]
    for i in itertools.count():
        if so == rotate_letter(s, l):
            return s
        s = rotate_left(s, 1)
    return s

@pytest.mark.parametrize("s, l, r",[
    ("abcdefgh", "c", "fghabcde"),
    ("abcdefgh", "f", "bcdefgha"),
    ("ecabd", "d", "decab"),
])
def test_invert_rotate_letter(s, l, r):
    assert "".join(invert_rotate_letter(list(r), l)) == s

def reverse_positions(s, x, y):
    """Reverse a series of positions."""
    return s[:x] + s[x:y+1][::-1] + s[y+1:]
    
@pytest.mark.parametrize("s, x, y, r",[
    ("abcdefgh", 3, 4, "abcedfgh"),
    ("abcdefgh", 2, 6, "abgfedch"),
    ("edcba",0, 4,"abcde")
])
def test_reverse_positions(s, x, y, r):
    assert "".join(reverse_positions(list(s), x, y)) == r

def move_position(s, x, y):
    """Move the item at x to y"""
    e = s.pop(x)
    s.insert(y, e)
    return s

@pytest.mark.parametrize("s, x, y, r",[
    ("abcdefgh", 3, 0, "dabcefgh"),
    ("abcdefgh", 0, 3, "bcdaefgh"),
    ("abcdefgh", 3, 4, "abcedfgh"),
    ("abcdefgh", 2, 6, "abdefgch"),
])
def test_move_position(s, x, y, r):
    assert "".join(move_position(list(s), x, y)) == r
    
def invert_move_position(s, x, y):
    """Invert a move position"""
    e = s.pop(y)
    s.insert(x, e)
    return s

@pytest.mark.parametrize("r, x, y, s",[
    ("abcdefgh", 3, 0, "dabcefgh"),
    ("abcdefgh", 0, 3, "bcdaefgh"),
    ("abcdefgh", 3, 4, "abcedfgh"),
    ("abcdefgh", 2, 6, "abdefgch"),
])
def test_invert_move_position(s, x, y, r):
    assert "".join(invert_move_position(list(s), x, y)) == r

PARSERS = [
    (r"swap position (?P<x>\d+) with position (?P<y>\d+)", swap_position, swap_position),
    (r"swap letter (?P<a>\w+) with letter (?P<b>\w+)", swap_letters, swap_letters),
    (r"rotate left (?P<n>\d+) steps?", rotate_left, rotate_right),
    (r"rotate right (?P<n>\d+) steps?", rotate_right, rotate_left),
    (r"rotate based on position of letter (?P<l>\w+)", rotate_letter, invert_rotate_letter),
    (r"reverse positions? (?P<x>\d+) through (?P<y>\d+)", reverse_positions, reverse_positions),
    (r"move position (?P<x>\d+) to position (?P<y>\w+)", move_position, invert_move_position),
]

PARSERS = [(re.compile(p[0]), *p[1:]) for p in PARSERS]

def parse(s, line, reverse=False):
    """Parse a line"""
    for expr, func, rfunc in PARSERS:
        match = expr.match(line)
        if match:
            kwargs = match.groupdict()
            for key in "xyn":
                if key in kwargs:
                    kwargs[key] = int(kwargs[key])
            if reverse:
                func = rfunc
            return func(s, **kwargs)
    raise ValueError(f"No match found for line '{line}'")


EXAMPLE = [
    ("abcde", "swap position 4 with position 0", "ebcda"),
    ("ebcda", "swap letter d with letter b", "edcba"),
    ("edcba", "reverse positions 0 through 4", "abcde"),
    ("abcde", "rotate left 1 step", "bcdea"),
    ("bcdea", "move position 1 to position 4", "bdeac"),
    ("bdeac", "move position 3 to position 0", "abdec"),
    ("abdec", "rotate based on position of letter b", "ecabd"),
    ("ecabd", "rotate based on position of letter d", "decab")
]

@pytest.mark.parametrize("s, l, r", EXAMPLE)
def test_parse(s, l, r):
     assert "".join(parse(list(s), l)) == r
     

@pytest.mark.parametrize("s, l, r", EXAMPLE)
def test_revparse(s, l, r):
    assert "".join(parse(list(r), l, reverse=True)) == s

def puzzle1():
    """First puzzle."""
    print("Puzzle #1")
    input_password = "abcdefgh"
    password = list(input_password)
    with open("day21_input.txt") as f:
        for line in f:
            password = parse(password, line.strip())
    scrambled_password = "".join(password)
    print(f"Password {input_password} is scrambled to {scrambled_password}")

def puzzle2():
    """Second puzzle, unwind."""
    print("Puzzle #2")
    scrambled_password = "fbgdceah"
    password = list(scrambled_password)
    with open("day21_input.txt") as f:
        for line in reversed(f.read().splitlines()):
            password = parse(password, line.strip(), reverse=True)
    input_password = "".join(password)
    print(f"Password {input_password} is scrambled to {scrambled_password}")
    

if __name__ == '__main__':
    puzzle1()
    puzzle2()
    