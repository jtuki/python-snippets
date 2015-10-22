# -*- encoding: utf-8 -*-
# jtuki@foxmail.com

r"""Compare the performance of big integer or ctypes for fixed size sequence.
"""

import ctypes

def test_big_integer(n):
    for i in range(n):
        s = (i % 65536)

def test_big_integer_segmented(n):
    while n > 65536:
        for i in range(65536):
            s = (i % 65536)
        n -= 65536
    for i in range(n):
        s = (i % 65536)
        
def test_ctypes(n):
    for i in range(n):
        s = ctypes.c_uint16(i)
        
def test_ctypes_segmented(n):
    while n > 65536:
        for i in range(65536):
            s = ctypes.c_uint16(i)
        n -= 65536
    for i in range(n):
        s = ctypes.c_uint16(i)
        
if __name__ == '__main__':
    import timeit
    import math
    
    t = timeit.timeit("test_big_integer(2*10**7)", "from __main__ import test_big_integer", number=2)
    print("2 times: test_big_integer(2*10**7): %f seconds" % t)
    
    t = timeit.timeit("test_ctypes(2*10**7)", "from __main__ import test_ctypes", number=2)
    print("2 times: test_ctypes(2*10**7): %f seconds" % t)
    
    t = timeit.timeit("test_big_integer_segmented(2*10**7)", "from __main__ import test_big_integer_segmented", number=2)
    print("2 times: test_big_integer_segmented(2*10**7): %f seconds" % t)
    
    t = timeit.timeit("test_ctypes_segmented(2*10**7)", "from __main__ import test_ctypes_segmented", number=2)
    print("2 times: test_ctypes_segmented(2*10**7): %f seconds" % t)
