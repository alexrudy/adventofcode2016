#!/usr/bin/env python

import re
import pytest


ABBA = re.compile(r"([a-z])([a-z])\2\1")
def contains_abba(s):
    """Returns true if a sequence contains an abba."""
    m = ABBA.search(s)
    if m is None:
        return False
    return m.group(1) != m.group(2)
    
ABA = re.compile(r"([a-z])[a-z]\1")
def iter_aba(s):
    """Iterate over ABA sequence"""
    for i, c in enumerate(s[:-2]):
        if s[i+1] != c and s[i+2] == c:
            aba = s[i:i+3]
            bab = aba[1] + aba[0] + aba[1]
            yield (aba, bab)
        
    

IPv7 = re.compile(r"\[?([a-z]+)\]?")
def iter_segments(addr):
    """Iterate over segments"""
    for segment in IPv7.finditer(addr):
        if "[" in segment.group(0):
            yield True, segment.group(1)
        else:
            yield False, segment.group(1)
        
    
ADDRESSES = [
    ("abba[mnop]qrst", ["abba", "mnop", "qrst"], True),
    ("abcd[bddb]xyyx", ["abcd", "bddb", "xyyx"], False),
    ("aaaa[qwer]tyui", ["aaaa", "qwer", "tyui"], False),
    ("ioxxoj[asdfgh]zxcvbn", ["ioxxoj", "asdfgh", "zxcvbn"], True)
]

@pytest.mark.parametrize("address, segments, supports_TLS", ADDRESSES)
def test_segments(address, segments, supports_TLS):
    """Test the segmenter."""
    assert [s[1] for s in iter_segments(address)] == segments
    assert [s[0] for s in iter_segments(address)] == [False, True, False]
    
def check_TLS_support(address):
    """Check TLS support for an address"""
    supports_TLS = False
    for is_hypernet, segment in iter_segments(address):
        is_abba = contains_abba(segment)
        if is_abba and is_hypernet:
            return False
        elif is_abba:
            supports_TLS = True
    return supports_TLS
    
@pytest.mark.parametrize("address, segments, supports_TLS", ADDRESSES)
def test_check_tls_support(address, segments, supports_TLS):
    """Check if an address supports TLS"""
    assert check_TLS_support(address) == supports_TLS
    
def check_SSL_support(address):
    """Check for SSL support."""
    supernet_patterns = set()
    hypernet_patterns = set()
    for is_hypernet, segment in iter_segments(address):
        for aba, bab in iter_aba(segment):
            if is_hypernet:
                if bab in supernet_patterns:
                    return True
                hypernet_patterns.add(aba)
            else:
                if bab in hypernet_patterns:
                    return True
                supernet_patterns.add(aba)
    return False
    
ADDRESSES_SSL = [
    ("aba[bab]xyz", True),
    ("xyx[xyx]xyx", False),
    ("aaa[kek]eke", True),
    ("zazbz[bzb]cdb", True)
]

@pytest.mark.parametrize("address, supports_ssl", ADDRESSES_SSL)
def test_check_SSL_support(address, supports_ssl):
    """Check if an address supports SSL"""
    assert check_SSL_support(address) == supports_ssl

if __name__ == '__main__':
    print("Puzzle #1")
    with open("day07_input.txt") as f:
        n_support_TLS = sum(check_TLS_support(address.strip()) for address in f)
    print(f"{n_support_TLS:d} addresses support TLS")
    print("Puzzle #2")
    with open("day07_input.txt") as f:
        n_support_SSL = sum(check_SSL_support(address.strip()) for address in f)
    print(f"{n_support_SSL:d} addresses support TLS")    