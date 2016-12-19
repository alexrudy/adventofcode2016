#!/usr/bin/env python

import pytest
import collections
import re

def most_common_5(s):
    """Most common 5 letters"""
    c = collections.Counter(s.replace("-",""))
    letters = c.most_common()
    letters.sort(key=lambda v : (-v[1], v[0]))
    return "".join((l[0] for l in letters[:5]))

@pytest.mark.parametrize("name,checksum",[
    ("aaaaa-bbb-z-y-x", "abxyz"),
    ("a-b-c-d-e-f-g-h", "abcde"),
    ("not-a-real-room", "oarel")
])
def test_most_common_5(name, checksum):
    """Test the mostcommon5 name."""
    assert most_common_5(name) == checksum
    
    
PARSER = re.compile(r"(?P<name>[A-Za-z\-]+)(?P<sector>\d+)\[(?P<checksum>\w+)\]")
def parse_room(text):
    """Parse a room from text."""
    m = PARSER.match(text)
    assert m
    return m.groupdict()
    
def parse_rooms(lines):
    """Parse rooms."""
    for line in lines:
        line = line.strip()
        if line:
            yield parse_room(line)

ROOMS="""aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]"""

def valid_rooms(lines):
    """Only the valid rooms."""
    return (r for r in parse_rooms(lines) if most_common_5(r['name']) == r['checksum'])

def sectorsum(lines):
    """Sector sum many lines."""
    return sum(int(r['sector']) for r in valid_rooms(lines))
    

def test_rooms():
    """Test the list of given rooms"""
    assert sectorsum(ROOMS.splitlines()) == 1514
    
with open("day04_input.txt") as f:
    print(sectorsum(f))

A_OFFSET = ord("a")

def rotate_letter(c, offset):
    """Rotate letter through."""
    return chr(A_OFFSET + ((ord(c) - A_OFFSET + offset) % 26))

def decrypt_string(s, offset):
    """Decrypt a string."""
    return "".join(rotate_letter(c, offset) if re.match("[a-z]", c) else " " for c in s)

def test_decrypt():
    """Test the decryption"""
    assert decrypt_string("qzmt-zixmtkozy-ivhz", 343) == "very encrypted name"

def decrypted_rooms(rooms):
    """Return decrypted room names"""
    for room in rooms:
        room['decrypted'] = decrypt_string(room['name'].lower(), int(room['sector']))
        yield room
    
with open("day04_input.txt") as f:
    for room in decrypted_rooms(valid_rooms(f)):
        if "NorthPole".lower() in room['decrypted']:
            print(room["decrypted"], room['sector'])
