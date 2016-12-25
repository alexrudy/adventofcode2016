#!/usr/bin/env python

import pytest
import re
import math
import collections
import hashlib
import copy
import itertools

DF_LINE = r"/dev/grid/node-x(?P<x>\d+)-y(?P<y>\d+)\s+(?P<size>\d+)T\s+(?P<used>\d+)T\s+(?P<avail>\d+)T\s+(?P<usage>\d+)%"

class Node(object):
    """A storage node."""
    def __init__(self, x, y, total, used, avail):
        super(Node, self).__init__()
        self.x = int(x)
        self.y = int(y)
        self.used = float(used)
        self.total = float(total)
        assert self.total - self.used == float(avail)
        
    @property
    def pos(self):
        """Position tuple"""
        return self.x, self.y
        
    def __repr__(self):
        """Represent this node."""
        return f"<Node {self.x},{self.y}>"
    
    @property
    def avail(self):
        """Return available space."""
        return self.total - self.used
    
    @property
    def kind(self):
        """What kind of node are we?"""
        if self.used > 89:
            return "X"
        if self.empty:
            return "_"
        else:
            return "#"
    
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
        
    
class Grid(object):
    """A grid of nodes"""
    def __init__(self):
        super(Grid, self).__init__()
        self.nodes = {}
        self.goal = ()
        
    def _add_node(self, node):
        """Add a new node"""
        self.nodes[node.x, node.y] = node.kind
        
    def _set_limits(self):
        """Set node limits."""
        coords = self.nodes.keys()
        self._xmax = max(x for x, y in coords)
        self._ymax = max(y for x, y in coords)
        self.nodes[(self._xmax, 0)] = "G"
        self.goal = (self._xmax, 0)
        
    @classmethod
    def parse(cls, lines):
        """docstring for parse"""
        grid = cls()
        for node in parse_nodes(lines):
            grid._add_node(node)
        grid._set_limits()
        return grid
        
    
    def iter_moves(self):
        """Iterate over available places to move data from (a->b)"""
        for (sx, sy), node in self.nodes.items():
            if node == "X":
                continue
            for dx, dy in self.iter_neighbors(sx, sy):
                if self.nodes[dx, dy] == "_":
                    yield ((sx, sy), (dx, dy))
    
    def copy(self):
        """Copy the grid."""
        grid = self.__class__()
        grid.nodes = copy.copy(self.nodes)
        grid.goal = self.goal
        grid._xmax = self._xmax
        grid._ymax = self._ymax
        return grid
    
    def moves(self):
        """Iterate through grids with moves."""
        for src, dest in self.iter_moves():
            grid = self.copy()
            grid.nodes[dest] = grid.nodes[src]
            grid.nodes[src] = "_"
            if grid.goal == src:
                grid.goal = dest
            yield grid
    
    def fingerprint(self):
        """Fingerprint the nodes."""
        return hashlib.md5("".join(s for (x, y), s in sorted(self.nodes.items())).encode('ascii')).hexdigest()
    
    def to_string(self):
        """Convert the grid to a string."""
        r = []
        for x in range(self._xmax+1):
            r.append(" ".join(self.nodes[x, y] for y in range(self._ymax+1)))
        return "\n".join(r)
    
    def gdist(self, target):
        """Distance to goal"""
        tx, ty = target
        gx, gy = self.goal
        return (tx - gx)**2 + (ty - gy)**2
    
    def iter_neighbors(self, x, y):
        """Iterate over neighboring nodes."""
        if x > 0:
            yield (x-1, y)
        if y > 0:
            yield (x, y - 1)
        if x < self._xmax:
            yield (x + 1, y)
        if y < self._ymax:
            yield (x, y + 1)
            
    
    def walk(self, target = (0, 0)):
        """A walker."""
        squeue = collections.deque([self])
        svisited = set([self.fingerprint()])
        sdist = self.gdist(target)
        try:
            for gen in itertools.count(0):
                nqueue = []
                while len(squeue):
                    grid = squeue.popleft()
                    if grid.goal == target:
                        return gen
                    if grid.gdist(target) < sdist:
                        sdist = grid.gdist(target)
                    for g in grid.moves():
                        f = g.fingerprint()
                        if f not in svisited:
                            svisited.add(f)
                            if g.gdist(target) <= sdist:
                                nqueue.append(g)
                squeue.extend(nqueue)
                print(f"Generation {gen:d}, seen {len(svisited):,d} states, queued {len(squeue):,d}.")
                if not len(squeue):
                    break
        except KeyboardInterrupt:
            print("")
            print(grid.to_string())
            raise
        raise ValueError("Exhausted search, can't find a solution.")
                
    
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
    
def puzzle2():
    """Second puzzle."""
    print("Puzzle #2")
    grid = Grid.parse(puzzle_input())
    print(grid.walk())

    
if __name__ == '__main__':
    puzzle1()
    puzzle2()
