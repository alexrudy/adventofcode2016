#!/usr/bin/env python

import pytest

MOTION = {
    'U' : (0, -1),
    'D' : (0, 1),
    'L' : (-1, 0),
    'R' : (1, 0)
}


class Keypad(object):
    """A keypad object."""
    def __init__(self, keys, start):
        super(Keypad, self).__init__()
        self.keys = [s.strip("\n") for s in keys.splitlines()]
        self.position = self.find_key(start)
        
    def find_key(self, key):
        """Return the position of a key."""
        for y, row in enumerate(self.keys):
            try:
                x = row.index(key)
            except ValueError:
                pass
            else:
                return (x, y)
        
    def walk(self, line):
        """Walk around the keypad given a line."""
        x, y = self.position
        key = self.keys[y][x]
        for direction in line:
            dx, dy = MOTION[direction]
            new_x = (x + (dx * 2))
            new_y = (y + dy)
            
            if new_x < 0:
                new_x = 0
            if new_y < 0:
                new_y = 0
            
            try:
                key = self.keys[new_y][new_x]
            except IndexError:
                pass
            else:
                if key != " ":
                    x, y = new_x, new_y
        self.position = (x, y)
        return self.keys[y][x]
    
    def decoder(self, code):
        """Decode the secret bathroom code."""
        for line in code:
            yield self.walk(line.strip())
        
    

KEYPAD1TO9 = """
1 2 3
4 5 6
7 8 9
"""[1:-1]

@pytest.mark.parametrize("line, result",[
    ("ULL", 1),
    ("RRDDD", 9),
    ("LURDL", 4),
    ("UUUUD", 5)
])
def test_button(line, result):
    """Test walks to a single button."""
    assert Keypad(KEYPAD1TO9, "5").walk(line) == str(result)

BUTTON_CODE = """ULL
RRDDD
LURDL
UUUUD"""

def test_buttons():
    """Test a bunch of buttons."""
    keypad = Keypad(KEYPAD1TO9, "5")
    assert list(keypad.decoder(BUTTON_CODE.splitlines())) == ["1", "9", "8", "5"]

INPUT = open("day02_input.txt")
keypad = Keypad(KEYPAD1TO9, "5")
code = "".join(["{}".format(b) for b in keypad.decoder(INPUT)])
print(f"The code is {code}")

KEYPAD2 = """
    1        
  2 3 4      
5 6 7 8 9    
  A B C      
    D        
"""

def test_wacky_buttons():
    """Test a bunch of buttons."""
    keypad = Keypad(KEYPAD2, "5")
    assert list(keypad.decoder(BUTTON_CODE.splitlines())) == ["5", "D", "B", "3"]

INPUT = open("day02_input.txt")
keypad = Keypad(KEYPAD2, "5")
code = "".join(["{}".format(b) for b in keypad.decoder(INPUT)])
print(f"The code is {code}")