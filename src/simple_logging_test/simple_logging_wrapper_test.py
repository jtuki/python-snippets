# -*- encoding: utf-8 -*-
# jtuki@foxmail.com

r"""Logger test.
"""

import gevent
import gevent.monkey
gevent.monkey.patch_all()

import simple_logging_wrapper

logger = simple_logging_wrapper.get_simple_logger(simple_logging_wrapper.LOG_LEVEL_ERROR)

def write_log(n):
    for i in range(n):
        if i % 4 == 0:
            logger.info("%d: Test logging module using stream and rotating file!" % i)
        elif i % 4 == 1:
            logger.info("%d: Everything can be taken from a man but one thing; the freedom to choose his attitude in any given set of circumstances!" % i)
        elif i % 4 == 2:
            logger.info("%d: - (Leonhard Frand , German novelist)!" % i)
        elif i % 4 == 3:
            logger.info("%d: The Python Module of the Week series, or PyMOTW, is a tour of the Python standard library through short examples.!" % i)
        else:
            assert False

def single_write_log(n):
    write_log(n)
    
def multi_write_log(n_w, n):
    greenlets = []
    for i in range(n_w):
        greenlets.append(gevent.spawn(single_write_log, n))
    gevent.joinall(greenlets)
            
if __name__ == '__main__':
    import timeit
    
    t = timeit.timeit("single_write_log(100000)", "from __main__ import single_write_log", number=10)
    print ("10 times - single_write_log(100000): %f seconds" % (t,))
    
    t = timeit.timeit("multi_write_log(5, 100000)", "from __main__ import multi_write_log", number=10)
    print ("10 times - multi_write_log(5, 100000): %f seconds" % (t,))