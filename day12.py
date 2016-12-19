#!/usr/bin/env python
"""
Day 12: Assembler
"""

import collections

class Registers(dict):
    """The assembly registers"""
    
    def val(self, src):
        """docstring for val"""
        try:
            sv = self[src]
        except KeyError:
            sv = int(src)
        return sv
    
    def cpy(self, src, dest):
        """Copy."""
        self[dest] = self.val(src)
    
    def inc(self, target):
        """Increment"""
        self[target] += 1
        
    def dec(self, target):
        """Decrement"""
        self[target] -= 1
    
    
def parse(commands, registers):
    """Parse commands"""
    commands = [command.strip() for command in commands if command.strip()]
    position = 0
    n = 0
    while position < len(commands):
        command = commands[position]
        n += 1
        cmd = command[:3]
        args = command[3:].split()
        if cmd == "cpy":
            registers.cpy(*args)
        elif cmd == "inc":
            registers.inc(*args)
        elif cmd == "dec":
            registers.dec(*args)
        elif cmd == "jnz":
            if registers.val(args[0]) != 0:
                # print(command + f" | {registers} | {position}")
                position += int(args[1])
                continue
        else:
            raise ValueError(f"Can't parse command {command}")
        # print(command + f" | {registers} | {position}")
        position += 1
    return registers

EXAMPLE_CMD = """
cpy 41 a
inc a
jnz a 1
inc a
dec a
jnz a 2
dec a
"""

def test_parser():
    """Test the parser."""
    r = parse(EXAMPLE_CMD.splitlines(), Registers.fromkeys("abcd", 0))
    assert r['a'] == 42
    
PUZZLE_CMD = """
cpy 1 a
cpy 1 b
cpy 26 d
jnz c 2
jnz 1 5
cpy 7 c
inc d
dec c
jnz c -2
cpy a c
inc a
dec b
jnz b -2
cpy c b
dec d
jnz d -6
cpy 13 c
cpy 14 d
inc a
dec d
jnz d -2
dec c
jnz c -5"""

def puzzle1():
    print("Puzzle #1")
    r = parse(PUZZLE_CMD.splitlines(), Registers.fromkeys("abcd", 0))
    print(r)

def puzzle2():
    """docstring for puzzle2"""
    print("Puzzle #2")
    r = Registers.fromkeys("abcd", 0)
    r['c'] = 1
    r = parse(PUZZLE_CMD.splitlines(), r)
    print(r)

if __name__ == '__main__':
    puzzle1()
    puzzle2()
