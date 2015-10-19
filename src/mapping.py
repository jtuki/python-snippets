# -*- encoding: utf-8 -*-
# jtuki@foxmail.com

import random

gl_bytes_mapping = dict()
gl_bytes_list = list()

def generate_multiple_bytes(n):
    assert n > 0
    # local cache
    generate_multiple_bytes.cached_bytes = set()
    
    while True:
        bytes_seq = bytes([random.randint(0, 255) for i in range(n)])
        if bytes_seq not in generate_multiple_bytes.cached_bytes:
            generate_multiple_bytes.cached_bytes.add(bytes_seq)
            break
        
    return bytes_seq
    
def get_mapping_value(bytes_seq):
    assert bytes_seq in gl_bytes_mapping
    return gl_bytes_mapping[bytes_seq]
    
def test_get_mapping():
    i = 0
    for b in gl_bytes_list:
        v = gl_bytes_mapping[b]
        i += 1
    return i
    
def create_mapping(n):
    global gl_bytes_list
    global gl_bytes_mapping
    
    gl_bytes_list = list()
    gl_bytes_mapping = dict()
 
    for i in range(n):
        b = generate_multiple_bytes(12)
        gl_bytes_list.append(b)
        gl_bytes_mapping[b] = b*5
    
if __name__ == '__main__':
    import timeit
    create_mapping(1000000)
    gl_bytes_list.sort()
    
    t = timeit.timeit('assert 1000000 == test_get_mapping()', 'from __main__ import test_get_mapping', number=10)
    print ('%f seconds (10 times) - excluding create_mapping().' % (t,))
    
