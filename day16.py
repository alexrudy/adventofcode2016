#!/usr/bin/env python

import pytest
import string
import itertools

trans = str.maketrans("01","10")

def bitflip(s):
    """Bitflip a string."""
    return s.translate(trans)

def dragon(a):
    """Dragonify"""
    yield from a
    yield "0"
    yield from bitflip("".join(reversed(a)))

def dragon_recursive(a):
    """Infinitely recurse through a dragon curve."""
    yield from a
    for i in itertools.count():
        yield "0"
        b = bitflip("".join(reversed(a)))
        yield from b
        a = a + "0" + b

@pytest.mark.parametrize("source, dragonified",[
    ("1", "100"),
    ("0", "001"),
    ("11111", "11111000000"),
    ("111100001010", "1111000010100101011110000")
])
def test_dragon(source, dragonified):
    """Test dragon curve"""
    assert "".join(dragon(source)) == dragonified

def dragon_data(seed, length):
    """Generate data up to a certain length."""
    return "".join(itertools.islice(dragon_recursive(seed), length))

def iterpairs(s):
    """Iterate through pairs"""
    for i in range(len(s) // 2):
        yield s[i*2:i*2+2]

def checksumpairs(s):
    """For a string, checksum the pairs."""
    for cs in iterpairs(s):
        if cs[0] == cs[1]:
            yield "1"
        else:
            yield "0"

@pytest.mark.parametrize("source, result",[
    ("1001", "00"),
    ("0111", "01"),
    ("11111000000", "11011"),
    ("1111000010100101011110000", "111100000101"),
    ("110010110100", "110101")
])
def test_checksumpairs(source, result):
    """Test checksum pairs."""
    assert "".join(checksumpairs(source)) == result

def checksum(data):
    """Checksum the data."""
    check = "".join(checksumpairs(data))
    while len(check) % 2 == 0:
        check = "".join(checksumpairs(check))
    return check
    
def test_checksum():
    """Test the full algorithm."""
    assert checksum("110010110100") == "100"

def test_example():
    """Test the full example."""
    data = dragon_data("10000", 20)
    assert data == "10000011110010000111"
    assert checksum(data) == "01100"
    
INPUT = "01000100010010111"
def puzzle1():
    print("Puzzle #1")
    cs = checksum(dragon_data(INPUT, 272))
    print(f"Checksum = {cs} ({len(cs)})")
    
def puzzle2():
    print("Puzzle #2")
    cs = checksum(dragon_data(INPUT, 35651584))
    print(f"Checksum = {cs} ({len(cs)})")
    
if __name__ == '__main__':
    puzzle1()
    puzzle2()
