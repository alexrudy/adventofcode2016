#!/usr/bin/env python
import re
import pytest

class Output(object):
    """An output bin."""
    def __init__(self, num):
        super(Output, self).__init__()
        self.num = int(num)
        self.chips = set()
        
    def __repr__(self):
        return f"<Bin {self.num} {self.chips!r}>"

class Bot(object):
    """A bot"""
    def __init__(self, num):
        super(Bot, self).__init__()
        self.num = int(num)
        self.chips = set()
        self._rule = None
        
    def __repr__(self):
        return f"<Bot {self.num} {self.chips!r}>"
        
    def set_rule(self, low_destination, high_destination):
        """docstring for set_rule"""
        self._rule = (low_destination, high_destination)
    
    def give(self):
        """Give my chips away."""
        for dest, chip in zip(self._rule, sorted(self.chips)):
            dest.chips.add(chip)
        comapred = tuple(sorted(self.chips))
        self.chips.clear()
        return comapred
    
class Factory(object):
    """The factory floor."""
    def __init__(self):
        super(Factory, self).__init__()
        self.bots = {}
        self.bins = {}
        self.comparisons = {}
        
    def get_bot(self, number):
        """Get a bot"""
        number = int(number)
        try:
            bot = self.bots[number]
        except KeyError:
            bot = self.bots[number] = Bot(number)
        return bot
    
    def get_bin(self, number):
        """Get a bin."""
        number = int(number)
        try:
            bin = self.bins[number]
        except KeyError:
            bin = self.bins[number] = Output(number)
        return bin
    
    def initialize(self, botnumber, microchip):
        """Initialize a bot with a microchip."""
        bot = self.get_bot(botnumber)
        bot.chips.add(int(microchip))
    
    def get_destination(self, kind, number):
        """Get a destination."""
        if kind == 'output':
            return self.get_bin(number)
        elif kind == 'bot':
            return self.get_bot(number)
    
    def add_rule(self, botnumber, low, high):
        """Add a new rule."""
        bot = self.get_bot(botnumber)
        low = self.get_destination(*low)
        high = self.get_destination(*high)
        bot.set_rule(low, high)
    
    def step(self):
        """Take the next move."""
        for bot in self.bots.values():
            if len(bot.chips) == 2:
                self.comparisons[bot.give()] = bot.num
                break
        
    
    def run(self):
        """Run the factory."""
        while any(len(bot.chips) == 2 for bot in self.bots.values()):
            self.step()
        
    
_VALUE = re.compile(r"value (\d+) goes to (bot|output) (\d+)")
_RULE = re.compile(r"bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)")
def parse_instruction(instruction):
    """docstring for parse_instruction"""
    vm = _VALUE.match(instruction)
    if vm:
        return ('value', int(vm.group(3)), int(vm.group(1)))
    rm = _RULE.match(instruction)
    if rm:
        return ('rule', int(rm.group(1)), (rm.group(2), int(rm.group(3))), (rm.group(4), int(rm.group(5))))
    raise ValueError(f"Can't understand instruction {instruction}")

def build(instructions):
    """Build a factory for some instructions."""
    f = Factory()
    for instruction in instructions:
        (rule, *args) = parse_instruction(instruction.strip())
        if rule == 'value':
            f.initialize(*args)
        elif rule == 'rule':
            f.add_rule(*args)
    return f

INSTRUCTIONS="""value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2"""

def test_factory_run():
    """Test factory."""
    f = build(INSTRUCTIONS.splitlines())
    assert f.bots[0].chips == set()
    assert f.bots[1].chips == {3}
    assert f.bots[2].chips == {2, 5}
    f.step()
    assert f.bots[0].chips == {5}
    assert f.bots[1].chips == {2, 3}
    assert f.bots[2].chips == set()
    f.step()
    assert f.bots[0].chips == {3, 5}
    assert f.bots[1].chips == set()
    assert f.bots[2].chips == set()
    assert f.bins[1].chips == {2}
    f.step()
    assert f.bins[0].chips == {5}
    assert f.bins[2].chips == {3}

def puzzle1():
    """First puzzle."""
    print("Puzzle #1")
    with open("day10_input.txt") as f:
        factory = build(f)
    factory.run()
    b = factory.comparisons[(17, 61)]
    print(f"Bot {b:d} compared 17 and 61")

def puzzle2():
    """Second puzzle."""
    print("Puzzle #2")
    with open("day10_input.txt") as f:
        factory = build(f)
    factory.run()
    v = 1
    for i in range(3):
        v *= factory.bins[i].chips.pop()
    print(f"The product is {v:d}")

if __name__ == '__main__':
    puzzle1()
    puzzle2()