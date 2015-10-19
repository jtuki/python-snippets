# -*- encoding: utf-8 -*-
# jtuki@foxmail.com

r"""Refer to msgpack-python:
https://pypi.python.org/pypi/msgpack-python/
"""

import msgpack
from msgpack import loads, dumps # alias(es) for unpackb and packb

gl_mapping_list = list()
gl_serialize_dumps_list = list()

def create_mapping_list(n):
    global gl_mapping_list
    gl_mapping_list = list()
    for i in range(n):
        s = dict()
        for j in range(100):
            s['hello' + str(j)] = i
        gl_mapping_list.append(s)

def test_msgpack_dumps():
    global gl_mapping_list
    global gl_serialize_dumps_list
    
    gl_serialize_dumps_list = list()
    for s in gl_mapping_list:
        s_serialized = dumps(s)
        gl_serialize_dumps_list.append(s_serialized)

def test_msgpack_loads():
    global gl_mapping_list
    global gl_serialize_dumps_list
    assert len(gl_serialize_dumps_list) > 0
    
    gl_mapping_list = list()
    
    for s_serialized in gl_serialize_dumps_list:
        s = loads(s_serialized)
        gl_mapping_list.append(s)
        
if __name__ == '__main__':
    import timeit
    
    t = timeit.timeit('create_mapping_list(100000)', 'from __main__ import create_mapping_list', number=10)
    print ('10 times - create_mapping_list(100000): %f seconds' % (t,))
    
    t = timeit.timeit('test_msgpack_dumps()', 'from __main__ import test_msgpack_dumps', number=10)
    print ('10 times - test_msgpack_dumps(): %f seconds' % (t,))
    
    t = timeit.timeit('test_msgpack_loads()', 'from __main__ import test_msgpack_loads', number=10)
    print ('10 times - test_msgpack_loads(): %f seconds' % (t,))
