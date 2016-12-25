#!/usr/bin/env python
"""
Day 12: Assembler
"""

import collections

class Registers(dict):
    """The assembly registers"""
    
    def __init__(self, *args, **kwargs):
        super(Registers, self).__init__(*args, **kwargs)
        self.p = 0
    
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
        
    def add(self, src, dest):
        """Add to the target"""
        self[dest] += self[src]
        self[src] = 0
        
    def mul(self, mul, src, dest):
        """Multiply target."""
        self[dest] += (self[src] * self[mul])
        self[src] = 0
        self[mul] = 0
    
S_INC_DEC = set(["inc", "dec"])
def optimize_add(command, commands, position):
    """Optimize an addition command."""
    if position + 3 > len(commands):
        return command
    
    # Check for the correct pattern of next commands.
    n3_cmds = [c[0] for c in commands[position:position+3]]
    if n3_cmds[2] != "jnz":
        return command
    if set(n3_cmds[:2]) != S_INC_DEC:
        return command
    
    # Check the jump argument
    jnz_args = commands[position+2][1:]
    if jnz_args[1] != "-2":
        return command
    
    # locate the add arguments
    predicate = jnz_args[0]
    if n3_cmds[0] == "inc":
        src = commands[position + 1][1]
        dest = commands[position][1]
    else:
        src = commands[position][1]
        dest = commands[position + 1][1]
    
    # Ensure the arguments make sense
    if src == dest or src != predicate:
        return command
    
    # Return optimized command
    return "add", src, dest
    
def optimize_mul(command, commands, position):
    """Optimize a multiplication loop."""
    if command[0] != "add":
        return command
    if position + 5 > len(commands):
        return command
    n2_cmds = [c[0] for c in commands[position+3:position+5]]
    if n2_cmds[1] != "jnz":
        return command
    if n2_cmds[0] != "dec":
        return command
    
    # Check the jump argument
    jnz_args = commands[position+4][1:]
    if jnz_args[1] != "-5":
        return command
    mul = commands[position+3][1]
    if mul in command[1:]:
        return command
    return "mul", mul, command[1], command[2]

def optimizer(commands, position):
    """A command optimizer."""
    command = optimize_add(commands[position], commands, position)
    command = optimize_mul(command, commands, position)
    if command != commands[position]:
        print(command)
    return command

def toggle(commands, target):
    """Toggle some command"""
    if not (0 <= target < len(commands)):
        return
    trg = commands[target]
    cmd = trg[0]
    args = trg[1:]
    nargs = len(args)
    if nargs == 1:
        if cmd == "inc":
            commands[target] = ("dec", *args)
        else:
            commands[target] = ("inc", *args)
    elif nargs == 2:
        if cmd == "jnz":
            commands[target] = ("cpy", *args)
        else:
            commands[target] = ("jnz", *args)

def parse(commands, registers):
    """Parse commands"""
    commands = [command.strip().split() for command in commands if command.strip()]
    position = 0
    n = 0
    while position < len(commands):
        command = optimizer(commands,position)
        n += 1
        cmd = command[0]
        args = command[1:]
        if cmd == "cpy":
            registers.cpy(*args)
        elif cmd == "inc":
            registers.inc(*args)
        elif cmd == "dec":
            registers.dec(*args)
        elif cmd == "jnz":
            if registers.val(args[0]) != 0:
                position += registers.val(args[1])
                continue
        elif cmd == "tgl":
            target = registers.val(args[0]) + position
            toggle(commands, target)
        elif cmd == "add":
            registers.add(*args)
            position += 3
            continue
        elif cmd == "mul":
            registers.mul(*args)
            position += 5
            continue
        else:
            raise ValueError(f"Can't parse command {command}")
        position += 1
    return registers

EXAMPLE_CMD = """
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
"""

def test_parser():
    """Test the parser."""
    r = parse(EXAMPLE_CMD.splitlines(), Registers.fromkeys("abcd", 0))
    assert r['a'] == 3
    
PUZZLE_CMD = """
cpy a b
dec b
cpy a d
cpy 0 a
cpy b c
inc a
dec c
jnz c -2
dec d
jnz d -5
dec b
cpy b c
cpy c d
dec d
inc c
jnz d -2
tgl c
cpy -16 c
jnz 1 c
cpy 81 c
jnz 94 d
inc a
inc d
jnz d -2
inc c
jnz c -5"""

def puzzle1():
    print("Puzzle #1")
    r = Registers.fromkeys("abcd", 0)
    r['a'] = 7
    r = parse(PUZZLE_CMD.splitlines(), r)
    print(r)

def puzzle2():
    print("Puzzle #2")
    r = Registers.fromkeys("abcd", 0)
    r['a'] = 12
    r = parse(PUZZLE_CMD.splitlines(), r)
    print(r)

if __name__ == '__main__':
    puzzle1()
    puzzle2()
