#!/usr/bin/env python
import pytest

import hashlib
import itertools
import random

def iter_digests(door_id, counter=False):
    """Iterate through the passwords."""
    m = hashlib.md5(door_id.encode('ascii'))
    for i in itertools.count():
        h = m.copy()
        h.update(f"{i:d}".encode('ascii'))
        digest = h.hexdigest()
        if digest.startswith("00000"):
            yield digest
        if counter and i % counter == 0:
            yield None
            
def iter_simple_codes(door_id):
    """Iterate through simple door codes."""
    for digest in iter_digests(door_id):
        yield digest[5]
    
def find_password(door_id, length):
    """Find the first n items."""
    return "".join(itertools.islice(iter_simple_codes(door_id), length))
    
def test_find_password():
    """A test for finding the password."""
    assert find_password("abc", 8) == "18f47a30"
    
    
def show_password(password):
    """Make a random-ish looking password."""
    hexlet = "0123456789abcdef" + "_" * 16
    output = []
    for i, c in enumerate(password):
        if c == "_":
            output.append(random.choice(hexlet))
        else:
            output.append(c)
    print(" Decrypting " + ("".join(output)) + "\r", end="")
    
def find_complex_door_codes(door_id, length, show=True):
    """Iterate through complex door codes which appear."""
    password = ["_"] * length
    if show:
        print(" Decrypting " + "".join(password) + "\r", end="")
    for digest in iter_digests(door_id, counter=10000):
        if digest is None:
            if show:
                show_password(password)
            continue
        if digest[5] in "01234567":
            index = int(digest[5])
            if password[index] == "_":
                password[index] = digest[6]
            if not any(p == "_" for p in password):
                break
    if show:
        show_password(password)
        print("")
    return "".join(password)
    
def test_complex_password():
    """Test a complex password."""
    assert find_complex_door_codes("abc", 8, show=False) == "05ace8e3"

if __name__ == '__main__':
    print("Puzzle #1")
    door_id = "wtnhxymk"
    password = find_password(door_id, 8)
    print(f"The password for {door_id} is {password}")
    
    print("Puzzle #2")
    password = find_complex_door_codes(door_id, 8, show=True)
    print(f"The password for {door_id} is {password}")
    
    
    