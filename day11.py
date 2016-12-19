#!/usr/bin/env python

import pytest
import collections
import itertools

class Floors(object):
    """An object to represent the state of the floors."""
    def __init__(self, n):
        super(Floors, self).__init__()
        self.n = int(n)
        
        # For each item, what floor is it on?
        self.things = {}
        
        # What floor is the elevator on?
        self.elevator = 1
        
        self.previous = None
    
    def __repr__(self):
        return f"<Floors with {self.n:d} floors, {len(self.things)} items and E{self.elevator:d}>"
        
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.floors()[key]
        return self.things[key]
        
    def __setitem__(self, key, value):
        self.things[key] = int(value)
        
    def _paired_items(self):
        """Paired items."""
        for item, floor in self.things.items():
            if item[1] == "G":
                if self.things[item[0] + "M"] == floor:
                    yield "-P", floor
                else:
                    yield item, floor
            if item[1] == "M" and self.things[item[0] + "G"] != floor:
                yield item, floor
            
        
    def _thing_state(self):
        """State of things"""
        if not hasattr(self, '_thing_state_cache'):
            self._thing_state_cache = list(sorted(self._paired_items()))
        return self._thing_state_cache
        
    def __eq__(self, other):
        return (other.elevator == self.elevator) and (other._thing_state() == self._thing_state())
        
    def __hash__(self):
        return hash((self.elevator, tuple(self._thing_state())))
        
    def done(self):
        """Is this state complete?"""
        return all(v == 4 for v in self.things.values())
        
    def floors(self):
        """Return a mapping from floor number to items."""
        if not hasattr(self, '_floors_cache'):
            floors = collections.defaultdict(set)
            for item, floor in self.things.items():
                floors[floor].add(item)
            self._floors_cache = floors
        return self._floors_cache
    
    def dangerops(self):
        """Is the current state dangerous?"""
        for floor in self.floors().values():
            generators = { thing[0] for thing in floor if thing[1] == "G" }
            if not generators:
                # floor isn't radiating, continue.
                continue
            for thing in floor:
                if thing[1] == "G":
                    # Its a generator, can't be destroyed.
                    continue
                if thing[0] not in generators:
                    # Not plugged in
                    return True
        return False
        
    def to_string(self):
        """Convert the map to a string."""
        n_items = len(self.things)
        output = []
        for fnum in range(1, self.n+1):
            output.append([f"F{fnum:d}", "| |"] + ["__"] * n_items + ["|"])
        for i, (label, f) in enumerate(self.things.items()):
            output[f-1][i+2] = label
        output[self.elevator - 1][1] = "|E "
        return "\n".join(" ".join(floor) for floor in reversed(output))
        
    def copy(self):
        """Copy the floors to a new state object."""
        fnew = self.__class__(self.n)
        fnew.elevator = self.elevator
        fnew.things = dict(self.things)
        return fnew
    
    def moves(self):
        """Iterate over possible moves from this state."""
        floors = self.floors()
        on_this_floor = floors[self.elevator]
        
        # We are at the final floor, don't move any finished pairs off of this floor?
        if self.elevator == self.n:
            # generators = { thing[0] for thing in on_this_floor if thing[1] == "G" }
            for thing in list(on_this_floor):
                if thing[1] == "M" and (thing[0] + "G") in on_this_floor:
                    on_this_floor.remove(thing)
                    on_this_floor.remove(thing[0] + "G")
        
        to_move = [ [t] for t in on_this_floor]
        for things in itertools.chain(to_move, itertools.combinations(on_this_floor, 2)):
            destinations = []
            if self.elevator > 1:
                if any(len(floors[f]) for f in range(1,self.elevator)):
                    destinations.append(self.elevator - 1)
            if self.elevator < self.n:
                destinations.append(self.elevator + 1)
            for destination in destinations:
                new = self.copy()
                new.previous = self
                new.elevator = destination
                for thing in things:
                    new.things[thing] = destination
                if self.previous and new == self.previous:
                    continue
                if not new.dangerops():
                    yield new
        
    def search(self):
        """Search for a done state."""
        to_check = collections.deque()
        seen = set([hash(self)])
        for m in self.moves():
            seen.add(hash(m))
            to_check.append(m)
        generation = 0
        try:
            for gen in itertools.count(1):
                next_to_check = []
                while len(to_check):
                    move = to_check.popleft()
                    if move.done():
                        return move
                    for m in move.moves():
                        hm = hash(m)
                        if hm not in seen:
                            seen.add(hm)
                            next_to_check.append(m)
                to_check.extend(next_to_check)
                print(f"Generation {gen:d}, seen {len(seen):,d} states, queued {len(to_check):,d}.")
                if not len(to_check):
                    break
        except KeyboardInterrupt:
            print("-" * 10)
            print(move.to_string())
            raise
        raise ValueError("Exhausted search, can't find a solution.")
        
    def pathlength(self):
        """Length of the path."""
        if self.previous is None:
            return 0
        return 1 + self.previous.pathlength()
    
    def iterpath(self):
        """Iterate path."""
        if self.previous is not None:
            yield from self.previous.iterpath()
        yield self
    
def test_floors():
    """Test floors basics"""
    f = Floors(4)
    assert f.to_string().splitlines()[0] == "F4 | | |"
    assert f.to_string().splitlines()[-1] == "F1 |E  |"
    assert not f.dangerops()

EXAMPLE_MAP = """F4 | | __ __ __ __ |
F3 | | __ __ LG __ |
F2 | | HG __ __ __ |
F1 |E  __ HM __ LM |"""

def test_example():
    """Example setup from problem statment."""
    f = Floors(4)
    f['HG'] = 2
    f['HM'] = 1
    f['LG'] = 3
    f['LM'] = 1
    assert f.to_string() == EXAMPLE_MAP
    assert f[1] == {"HM","LM"}
    assert f[2] == {"HG"}
    assert f[3] == {"LG"}
    assert not f.dangerops()
    assert f.search().pathlength() == 11
    
PUZZLE_INPUT = """
The first floor contains a strontium generator, a strontium-compatible microchip, a plutonium generator, and a plutonium-compatible microchip.
The second floor contains a thulium generator, a ruthenium generator, a ruthenium-compatible microchip, a curium generator, and a curium-compatible microchip.
The third floor contains a thulium-compatible microchip.
The fourth floor contains nothing relevant.
"""

PUZZLE_FLOORS = Floors(4)
PUZZLE_FLOORS['SG'] = 1
PUZZLE_FLOORS['SM'] = 1
PUZZLE_FLOORS['PG'] = 1
PUZZLE_FLOORS['PM'] = 1
PUZZLE_FLOORS['RG'] = 2
PUZZLE_FLOORS['RM'] = 2
PUZZLE_FLOORS['CG'] = 2
PUZZLE_FLOORS['CM'] = 2
PUZZLE_FLOORS['TG'] = 2
PUZZLE_FLOORS['TM'] = 3

def puzzle1():
    """The first puzzle."""
    print("Puzzle #1")
    print(PUZZLE_FLOORS.to_string())
    end = PUZZLE_FLOORS.search()
    npath = end.pathlength()
    print(f"It will take {npath:d} moves to finish.")
    print(end.to_string())
    
def puzzle2():
    """docstring for puzzle2"""
    print("Puzzle #2")
    pf = PUZZLE_FLOORS.copy()
    pf['EG'] = 1
    pf['EM'] = 1
    pf['DG'] = 1
    pf['DM'] = 1
    print(pf.to_string())
    end = pf.search()
    npath = end.pathlength()
    print(f"It will take {npath:d} moves to finish.")
    print(end.to_string())
    
if __name__ == '__main__':
    puzzle1()
    puzzle2()
        