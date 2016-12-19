#!/usr/bin/env python

import pytest
import re

def rotate(seq, by):
    by = len(seq) - (by % len(seq))
    return seq[by:] + seq[:by]

@pytest.mark.parametrize("sequence, by, result",[
    ("abcdefg", 1, "gabcdef"),
    ("abcdefg", 4, "defgabc"),
    ("abcdefg", 0, "abcdefg"),
    ([1, 2, 3, 4, 5], 3, [3, 4, 5, 1, 2]),])    
def test_rotate(sequence, by, result):
    assert rotate(sequence, by) == result

COMMANDS = [
    (r"rect (\d+)x(\d+)", "rect"),
    (r"rotate column x=(\d+) by (\d+)", "rotate_column"),
    (r"rotate row y=(\d+) by (\d+)", "rotate_row")
]

class Screen(object):
    """A screen"""
    def __init__(self, width, height):
        super(Screen, self).__init__()
        self.width = width
        self.height = height
        self.pixels = [["."] * width for i in range(height)]
        
    def rect(self, A, B):
        """Turn on a rectangle of pixels."""
        for i in range(B):
            for j in range(A):
                self.pixels[i][j] = "#"
            
    def rotate_row(self, A, B):
        """Rotate a row around."""
        self.pixels[A] = rotate(self.pixels[A], B)
        
    def rotate_column(self, A, B):
        """Rotate a column around."""
        transposed = list(zip(*self.pixels))
        transposed[A] = rotate(transposed[A], B)
        self.pixels = list(list(a) for a in zip(*transposed))
        
    @property
    def on(self):
        """Number of on pixels"""
        return sum(p == "#" for r in self.pixels for p in r)
    
    def to_string(self):
        """Put this screen into a string"""
        return "\n".join("".join(row) for row in self.pixels)
        
    def execute(self, text):
        """Parse and execute a command."""
        for pattern, command in COMMANDS:
            m = re.match(pattern, text)
            if m:
                getattr(self, command)(*[int(d) for d in m.groups()])
                return
        raise ValueError(f"Can't parse command {command}")
    
class TestSreen(object):
    """Tests for the screen class."""
        
    @pytest.fixture
    def s(self):
        """A screen."""
        return Screen(4,4)
        
    def assert_listiness(self, s):
        """Ensure that things are listish"""
        assert isinstance(s.pixels, list)
        assert all(isinstance(r, list) for r in s.pixels)
        
        
    def test_basic(self, s):
        assert s.on == 0
        assert s.to_string() == "\n".join(["." * 4] * 4)
        self.assert_listiness(s)
    
    def test_rect(self, s):
        s.rect(2, 2)
        assert s.on == 4
        assert s.to_string() == "\n".join([
            "##..", "##..", "....", "...."
        ])
        self.assert_listiness(s)
        

    def test_rotate_row(self, s):
        s.rect(2, 2)
        s.rotate_row(1, 3)
        assert s.on == 4
        assert s.to_string() == "\n".join([
            "##..", "#..#", "....", "...."
        ])
        self.assert_listiness(s)
        
        
    def test_rotate_col(self, s):
        s.rect(2, 2)
        s.rotate_column(1, 3)
        assert s.on == 4
        assert s.to_string() == "\n".join([
            "##..", "#...", "....", ".#.."
        ])
        self.assert_listiness(s)
        
    

def execute(commands, screen):
    """Execute commands."""
    for line in commands:
        for pattern, command in COMMANDS:
            m = re.match(pattern, line)
            if m:
                getattr(screen, command)(*m.groups())
                break
        print(screen.to_string())
    

SCREENS = [
("rect 3x2",
"""###....
###....
.......""",),
("rotate column x=1 by 1",
"""#.#....
###....
.#.....""",),
("rotate row y=0 by 4",
"""....#.#
###....
.#.....""",),
("rotate column x=1 by 1",
""".#..#.#
#.#....
.#.....""",),
]
def test_execute():
    """Test execute commands."""
    screen = Screen(7, 3)
    for command, output in SCREENS:
        screen.execute(command)
        assert screen.to_string() == output
        
if __name__ == '__main__':
    print("Puzzle #1")
    with open('day08_input.txt') as f:
        screen = Screen(50, 6)
        for line in f:
            screen.execute(line.strip())
    print(f"{screen.on:d} pixels are illuminated")
    print(screen.to_string().replace("."," "))
            