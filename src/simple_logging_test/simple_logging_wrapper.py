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

LOG_LEVEL_DEBUG     = 0
LOG_LEVEL_INFO      = 1
LOG_LEVEL_ERROR     = 2
LOG_LEVEL_CRITICAL  = 3

_log_level = [LOG_LEVEL_DEBUG, LOG_LEVEL_INFO, LOG_LEVEL_ERROR, LOG_LEVEL_CRITICAL]

class SimpleLoggingWrapper(object):
    def __init__(self, log_level):
        assert log_level in _log_level
        self.log_level = log_level
        self.logger = logging.getLogger("stream_and_rotating_file")
        
    def debug(self, log_msg):
        if self.log_level > LOG_LEVEL_DEBUG:
            return
        else:
            self.logger.debug(log_msg)
            
    def info(self, log_msg):
        if self.log_level > LOG_LEVEL_INFO:
            return
        else:
            self.logger.info(log_msg)
            
    def error(self, log_msg):
        if self.log_level > LOG_LEVEL_ERROR:
            return
        else:
            self.logger.error(log_msg)
            
    def critical(self, log_msg):
        self.logger.critical(log_msg)
        
def get_simple_logger(log_level):
    return SimpleLoggingWrapper(log_level)