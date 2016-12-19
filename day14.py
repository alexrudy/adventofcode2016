#!/usr/bin/env python

import hashlib
import re
import itertools
import collections
import pytest
import heapq

TRIPLE = re.compile(r"(\w)\1\1")
FIVES = re.compile(r"(\w)\1\1\1\1")
def iter_triples(s):
    """Does the string have a triple letter sequence."""
    m = TRIPLE.search(s)
    if m:
        yield m.group(1)
    
def get_triple(s):
    """Get the triple"""
    m = TRIPLE.search(s)
    if m:
        return m.group(1)
    else:
        raise ValueError(f"No triple found in {s!r}")
    
def iter_fives(s):
    """Iterate through five matches."""
    for m in FIVES.finditer(s):
        yield m.group(1)
        
def stretch_hash(digest, n):
    """Stretch a hash n times."""
    for i in range(n):
        digest = hashlib.md5(digest.encode('ascii')).hexdigest()
    return digest
    
def _gen_hash(hashbase, index, stretch=0):
    """Generate a hash"""
    h = hashbase.copy()
    h.update(f"{index:d}".encode('ascii'))
    return stretch_hash(h.hexdigest(), stretch)
    
def gen_hash(salt, index, stretch=0):
    """Generate a single hash"""
    hbase = hashlib.md5(salt.encode('ascii'))
    return _gen_hash(hbase, index, stretch=stretch)
    
@pytest.mark.parametrize("index, hash_part",[
    (18, "cc38887a5"),
    (39, "eee"),
    (816, "eeeee"),
    (92, "999"),
    (200, "99999"),
])
def test_hashes(index, hash_part):
    """Test constructing hashes."""
    digest = gen_hash("abc", index)
    assert hash_part in digest

@pytest.mark.parametrize("digest, triple",[
    ("888a777", "8"),
    ("abeeecd", "e"),
])
def test_find_first_triple(digest, triple):
    """Assert that we can find only the first triple"""
    assert set(iter_triples(digest)) == set([triple])

@pytest.mark.parametrize("index, pattern",[
    (18, "8"),
    (39, "e"),
    (816, "e"),
    (92, "9"),
    (200, "9"),
])
def test_find_triples(index, pattern):
    """Test finding triples in each of these."""
    for match in iter_triples(gen_hash("abc", index)):
        pass
    assert match == pattern
    
@pytest.mark.parametrize("index, pattern",[
    (816, "e"),
    (200, "9"),
])
def test_find_fives(index, pattern):
    """Test finding five patterns."""
    assert pattern in set(iter_fives(gen_hash("abc", index)))

def enum_hashes(salt, stretch=0):
    """docstring for enum_hashes"""
    hbase = hashlib.md5(salt.encode('ascii'))
    for i in itertools.count():
        yield i, _gen_hash(hbase, i, stretch=stretch)
    
def test_enum_hashes():
    """Test enumerate hashes."""
    for i, digest in itertools.islice(enum_hashes("abc"), 19):
        pass
    assert "cc38887a5" in digest


def iter_keys(salt, stretch=0, verbose=False):
    """Iterate through keys."""
    candidates = collections.defaultdict(list)
    keys = []
    for i, digest in enum_hashes(salt, stretch=stretch):
        for match in iter_triples(digest):
            candidates[match].append((i, digest))
        for match in iter_fives(digest):
            if match in candidates:
                triples = candidates[match]
                for index, key in triples[:]:
                    if (index + 1000) >= i > index:
                        heapq.heappush(keys, (index, key, i, digest))
                        triples.remove((index, key))
                    elif (index + 1000) <= i:
                        triples.remove((index, key))
        if len(keys) and keys[0][0] + 1000 <= i:
            yield heapq.heappop(keys)
        if verbose and i % 10000 == 0:
            print(f"Index {i:,d}, N={len(candidates)}")

def keygen(salt, keys, stretch=0):
    """Generate a set number of keys."""
    for index, key, vindex, vdigest in itertools.islice(iter_keys(salt, stretch=stretch), keys):
        yield index, key

def test_find_first_key():
    """Test the example salt."""
    for i, key in keygen("abc", 1):
        print(f"{i:,d}: {key}")
    assert i == 39
    assert "eee" in key

def test_example_salt():
    """Test the example salt."""
    keys = []
    for i, key, vindex, vdigest in itertools.islice(iter_keys("abc"), 64):
        keys.append(i)
        triple = get_triple(key)
        assert triple * 5 in vdigest
    print(keys[-10:])
    assert len(keys) == 64
    assert max(keys) == 22728
    
@pytest.mark.parametrize("index, result",[
    (0, "a107ff634856bb300138cac6568c0f24")
])
def test_stretched_hash(index, result):
    """Test the stretched hash."""
    assert gen_hash("abc", index, 2016) == result
    
def test_find_first_key_streched():
    """Test the first key."""
    for i, key in keygen("abc", 1, 2016):
        print(f"{i:,d}: {key}")
    assert i == 10
    assert "eee" in key
    
def test_example_salt_streched():
    keys = []
    for i, key, vindex, vdigest in itertools.islice(iter_keys("abc", stretch=2016), 64):
        keys.append(i)
        triple = get_triple(key)
        assert triple * 5 in vdigest
        assert i < vindex <= (i + 1000)
    print(keys[-10:])
    assert len(keys) == 64
    assert max(keys) == 22551

SALT = "qzyelonm"
def puzzle1():
    """First puzzle"""
    print("Puzzle #1")
    for i, key in keygen(SALT, 64):
        pass
    print(f"index {i:,d} produces the 64th key.")

def puzzle2():
    """Second puzzle"""
    print("Puzzle #2")
    for n, (i, key) in enumerate(keygen(SALT, 64, stretch=2016)):
        print(f"Key {n:d} is at index {i:d} and is {key:s}")
    print(f"index {i:,d} produces the 64th key.")
    
    
if __name__ == '__main__':
    puzzle1()
    puzzle2()
    
        