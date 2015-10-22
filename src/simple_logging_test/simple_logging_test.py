# -*- encoding: utf-8 -*-
# jtuki@foxmail.com

r"""Logger test.
"""

import gevent
import gevent.monkey
gevent.monkey.patch_all()

# logging use threading module, so we use gevent's monkey patch to make it coroutine-able.
import logging
import logging.config

# configuration of logger, we use stream and rotating file.
# stream logging (=> sys.stderr) is info level; while rotating file logging (=> logger file) is debug level.
logging.config.fileConfig("./logger.conf")
logger = logging.getLogger("stream_and_rotating_file")

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
    
    t = timeit.timeit("single_write_log(100000)", "from __main__ import single_write_log", number=1)
    print ("single_write_log(100000): %f seconds" % (t,))
    
    t = timeit.timeit("multi_write_log(5, 100000)", "from __main__ import multi_write_log", number=1)
    print ("multi_write_log(5, 100000): %f seconds" % (t,))