#!/usr/bin/env python

import pytest
import re

def decompress(s):
    """Decompress a string."""
    return "".join(s * i for i, s in operate(re.sub("\s", "", s)))

AXB = re.compile(r"\((\d+)x(\d+)\)")
def operate(s):
    """Operate on a substring"""
    i = 0
    while i < len(s):
        m = AXB.search(s, i)
        if not m:
            break
        yield 1, s[i:m.start()]
        substrsize = int(m.group(1))
        repeats = int(m.group(2))
        substr = s[m.end():m.end() + substrsize]
        yield repeats, substr
        i = m.end() + substrsize
    yield 1, s[i:]

CSTRINGS = [
    ("ADVENT","ADVENT","ADVENT"),
    ("A(1x5)BC","ABBBBBC","ABBBBBC"),
    ("(3x3)XYZ","XYZXYZXYZ","XYZXYZXYZ"),
    ("(6x1)(1x3)A","(1x3)A", "AAA"),
    ("X(8x2)(3x3)ABCY","X(3x3)ABC(3x3)ABCY", "XABCABCABCABCABCABCY")
]

@pytest.mark.parametrize("source,output,full_output",CSTRINGS)
def test_decompress(source,output,full_output):
    assert decompress(source) == output
 
@pytest.mark.parametrize("source,output,full_output",CSTRINGS)
def test_full_decompress(source,output,full_output):
    assert "".join(full_decompress(source)) == full_output

def full_decompress(s):
    """Fully decompress a string."""
    for i, segment in operate(s):
        if "(" in segment:
            for _ in range(i):
                yield from full_decompress(segment)
        else:
            yield i * segment
            
    
def full_decompress_length(s):
    """Compute only the length after decompression"""
    for i, segment in operate(s):
        if "(" in segment:
            yield i * sum(full_decompress_length(segment))
        else:
            yield i * len(segment)
    

@pytest.mark.parametrize("source,output,full_output",CSTRINGS)
def test_full_decompress_length(source,output,full_output):
    assert len(full_output) == sum(full_decompress_length(source))

if __name__ == '__main__':
    print("Puzzle #1")
    with open("day09_input.txt") as f:
        decompressed = decompress(f.read().strip())
    print(f"The file is {len(decompressed):,d} characters long.")
    print("Puzzle #2")
    with open("day09_input.txt") as f:
        decompressed_length = sum(full_decompress_length(f.read().strip()))
    print(f"The file is {decompressed_length:,d} characters long.")