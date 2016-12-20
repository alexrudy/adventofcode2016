#!/usr/bin/env python

import pytest
import string
import itertools

trans = str.maketrans("01","10")

def bitflipr(s):
    """Bitflip a string."""
    return s.translate(trans)[::-1]

def dragon(a):
    """Dragonify"""
    yield from a
    yield "0"
    yield from bitflipr("".join(a))

def dragon_recursive(a):
    """Infinitely recurse through a dragon curve."""
    yield from a
    for i in itertools.count():
        yield "0"
        b = bitflipr("".join(a))
        yield from b
        a = a + "0" + b
        
def dragon_generator(seed, steps, reverse=True):
    """The full dragon generator."""
    if steps == 0:
        if reverse:
            yield from bitflipr(seed)
        else:
            yield from seed
    else:
        yield from dragon_generator(seed, steps - 1, reverse=False)
        yield "1" if reverse else "0"
        yield from dragon_generator(seed, steps - 1, reverse=True)

def dragon_infinite(seed):
    """Infinite dragon generator."""
    yield from seed
    for i in itertools.count():
        yield "0"
        yield from dragon_generator(seed, i, reverse=True)

def dragon_finite(seed, length):
    """Make a finite length dragon generator"""
    return itertools.islice(dragon_infinite(seed), length)

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
    return "".join(dragon_finite(seed, length))

def iterpairs(s):
    """Iterate through pairs"""
    iterator = iter(s)
    while True:
        yield next(iterator), next(iterator)
        


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
    
def checksum_depth(length):
    """Given a length, how many times must we checksum to get an odd output."""
    for i in itertools.count():
        if length % 2 == 0:
            length = length // 2
        else:
            return i - 1

def checksum_base(checksum):
    """Recursive checksum."""
    for a,b in iterpairs(checksum):
        yield "1" if a == b else "0"
    
def checksum_recursive(checksum, depth):
    """Recursive checksum"""
    if depth == 0:
        yield from checksum_base(checksum)
    else:
        yield from checksum_recursive(checksum_base(checksum), depth - 1)

def checksum_iterative(data, length):
    """Checksum iteratively over data."""
    depth = checksum_depth(length)
    return checksum_recursive(data, depth)
    
def test_checksum():
    """Test the full algorithm."""
    assert checksum("110010110100") == "100"

def test_example():
    """Test the full example."""
    data = dragon_data("10000", 20)
    assert data == "10000011110010000111"
    assert checksum(data) == "01100"
    
def test_puzzle1():
    """Test for puzzle 1"""
    length = 272
    assert "".join(checksum_iterative(dragon_data(INPUT, length), length)) == "10010010110011010"
    
INPUT = "01000100010010111"
def puzzle1():
    print("Puzzle #1")
    length = 272
    cs = "".join(checksum_iterative(dragon_data(INPUT, length), length))
    print(f"Checksum = {cs} ({len(cs)})")
    
def puzzle2():
    print("Puzzle #2")
    length = 35651584
    cs = "".join(checksum_iterative(dragon_data(INPUT, length), length))
    print(f"Checksum = {cs} ({len(cs)})")
    
if __name__ == '__main__':
    puzzle1()
    puzzle2()
