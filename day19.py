#!/usr/bin/env python
"""
Elf White Elephant
"""

import pytest
import collections
import itertools

def last_elf(n):
    """Last elf remaining."""
    e = collections.deque(range(1, n+1))
    while len(e) > 1:
        i = e.popleft()
        e.popleft()
        e.append(i)
    return e.popleft()

def last_elf_closed(n):
    """Last elf in closed form."""
    return int("0b" + bin(n)[3:] + "1", 2)

@pytest.mark.parametrize("n, l",[
    (5, 3)
])
def test_last_elf(n,l):
    """Test the last elf."""
    assert last_elf(n) == l
    
@pytest.mark.parametrize("n",[
    5, 6, 20, 50, 64, 65
])
def test_closed(n):
    """docstring for test_closed"""
    assert last_elf(n) == last_elf_closed(n)
    

def try_last_elf():
    """Try a bunch of last elf."""
    for i in range(1, 20):
        e = last_elf(i)
        print(f"N={i:2d}, E={e:2d} {bin(i-1):10s} -> {bin(e-1):10s} ~> {'0b'+bin(i)[3:]+'0':10s}")
        
INPUT = 3004953
def puzzle1():
    """docstring for puzzle1"""
    print("Puzzle #1")
    print(f"Last Elf is {last_elf_closed(INPUT):d}")
    
def elf_circle(n):
    """Elf stealing circle"""
    e = collections.deque(range(1, n+1))
    while len(e) > 1:
        s = (len(e) // 2)
        del e[s]
        e.rotate(-1)
        if len(e) % 10000 == 0:
            print(f"{len(e)}")
    return e.popleft()
    
def elf_circle_list(n):
    """Handle the elf circle from a list"""
    left = collections.deque()
    right = collections.deque()
    for e in range(1, n+1):
        if e < (n//2 + 1):
            left.append(e)
        else:
            right.appendleft(e)
    while left and right:
        if len(left) > len(right):
            left.pop()
        else:
            right.pop()
        right.appendleft(left.popleft())
        left.append(right.pop())
    return left[0] or right[0]
    
class Node(object):
    """docstring for Node"""
    def __init__(self, arg):
        super(Node, self).__init__()
        self.arg = arg
        
    
@pytest.mark.parametrize("n, l",[
    (5, 2)
])
def test_elf_circle(n, l):
    assert elf_circle(n) == l
    
@pytest.mark.parametrize("n",[
    3, 5, 6, 20, 50, 64, 65
])
def test_elf_circle_list(n):
    assert elf_circle(n) == elf_circle_list(n)
    
def try_elf_circle():
    """See if there is a binary pattern here."""
    for i in range(1, 20):
        e = elf_circle(i)
        g = '0b1'+bin(i-1)[:2:-1]
        c = "✓" if int(g, 2) == e - 1 else "𐄂"
        print(f"N={i:2d}, E={e:2d} {bin(i-1):10s} -> {bin(e - 1):10s} ~> {g:10s} {c:s}")
        
    
def puzzle2():
    print("Puzzle #2")
    print(f"Last Elf is {elf_circle_list(INPUT):d}")

if __name__ == '__main__':
    puzzle1()
    puzzle2()