#!/usr/bin/env python

import pytest

def parse_range(s):
    """Parse a range."""
    a, b = s.rstrip().split("-")
    return int(a), int(b)

@pytest.mark.parametrize("s, r",[
    ("5-8", (5, 8)),
    ("0-2", (0, 2)),
    ("4-7\n", (4, 7))
])
def test_parse_ranges(s, r):
    assert parse_range(s) == r

def clip_range(rng, clip):
    """Clip a range into two."""
    if rng[0] > clip[1] or rng[1] < clip[0]:
        yield rng
    else:
        if rng[0] < clip[0]:
            yield (rng[0], clip[0] - 1)
        if rng[1] > clip[1]:
            yield (clip[1] + 1, rng[1])
            
@pytest.mark.parametrize("i, s, rs",[
    ((0, 9), "5-8", [(0, 4), (9, 9)]),
    ((0, 2), "0-2", []),
    ((0, 7), "4-7\n", [(0, 3)])
])
def test_clip(i, s, rs):
    assert list(clip_range(i, parse_range(s))) == rs
    
def block(ranges, clip):
    """Block various clips in ranges"""
    riter = iter(ranges)
    for rng in riter:
        yield from clip_range(rng, clip)
        if clip[1] < rng[0]:
            break
    yield from riter

def blockmany(ranges, clips):
    for clip in clips:
        ranges = block(ranges, clip)
    return ranges

def parser(clips):
    """docstring for parser"""
    for clip in clips:
        yield parse_range(clip)

CLIPS = ["5-8","0-2","4-7"]

def test_parser():
    """Test the parser"""
    assert list(parser(CLIPS)) == [(5, 8), (0, 2), (4, 7)]

def test_block():
    assert list(blockmany([(0, 9)], parser(CLIPS))) == [(3, 3), (9, 9)]

def lowest(ranges, clips):
    return next(blockmany(ranges, clips))[0]
    
def test_lowest():
    assert lowest([(0, 9)], parser(CLIPS)) == 3
    
def nopen(ranges, clips):
    return sum(rng[1] - rng[0] + 1 for rng in blockmany(ranges, clips))
    
def test_nopen():
    assert 2 == nopen([(0, 9)], parser(CLIPS))
    
HIGHEST = 4294967295
FULLRANGE = [(0, HIGHEST)]
def puzzle1():
    print("Puzzle #1")
    with open("day20_input.txt") as f:
        l = lowest(FULLRANGE, parser(f))
    print(f"The lowest open IP address is {l:d}")
    
def puzzle2():
    """Open IPs"""
    print("Puzzle #1")
    with open("day20_input.txt") as f:
        n = nopen(FULLRANGE, parser(f))
    print(f"There are {n:d} open IP addresses.")

if __name__ == '__main__':
    puzzle1()
    puzzle2()

    