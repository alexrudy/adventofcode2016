#!/usr/bin/env python

import pytest
import re
import math

DF_LINE = r"/dev/grid/node-x(?P<x>\d+)-y(?P<y>\d+)\s+(?P<size>\d+)T\s+(?P<used>\d+)T\s+(?P<avail>\d+)T\s+(?P<usage>\d+)%"

class Node(object):
    """A storage node."""
    def __init__(self, x, y, total, used, avail):
        super(Node, self).__init__()
        self.x = int(x)
        self.y = int(y)
        self.used = float(used)
        self.avail = float(avail)
        self.total = float(total)
        
    @property
    def empty(self):
        """Is this node empty?"""
        return self.used == 0.0
    
    @property
    def usage(self):
        """Percentage used."""
        return math.floor((self.used / self.total) * 100) / 100.0
        
    @property
    def name(self):
        """Name of this node."""
        return f"/dev/grid/node-x{self.x:d}-y{self.y:d}"
        
    @classmethod
    def parse(cls, line):
        """Make a node from a line of DF output."""
        m = re.match(DF_LINE, line)
        if not m:
            raise ValueError(f"Line '{line}' doesn't parse as DF output.")
        p = m.groupdict()
        return cls(p['x'], p['y'], p['size'], p['used'], p['avail'])
        

@pytest.mark.parametrize("s, x, y, total, used, avail, usage",[
    ("/dev/grid/node-x0-y1     90T   68T    22T   75%", 0, 1, 90, 68, 22, 0.75)
])
def test_parse_node(s, x, y, total, used, avail, usage):
    node = Node.parse(s)
    assert node.x == x
    assert node.y == y
    assert node.total == total
    assert node.used == used
    assert node.avail == avail
    assert node.usage == usage
    assert node.name == s.split()[0]
    assert node.empty ==  (usage == 0.0)

def parse_nodes(lines):
    """For each line, yeild a node."""
    for line in lines:
        yield Node.parse(line)
    
def node_pairs(nodes):
    """Iterate through all viable pairs of nodes"""
    nodes = list(nodes)
    nodes.sort(key = lambda n : -n.avail)
    for a in nodes:
        if a.empty:
            continue
        for b in nodes:
            if a.used <= b.avail:
                yield (a, b)
            else:
                break
        
    
def puzzle_input():
    """Return a slightly sanitized puzzle input."""
    with open("day22_input.txt") as f:
        for i, l in enumerate(f):
            if i >= 2:
                yield l.strip()

def puzzle1():
    """Solve the first puzzle."""
    print("Puzzle #1")
    for i, (a, b) in enumerate(node_pairs(parse_nodes(puzzle_input()))):
        pass
    print(f"There were {i+1:d} pairs of nodes.")
    
if __name__ == '__main__':
    puzzle1()