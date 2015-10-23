## RESULTS

### `mapping.py`

测试环境：
```
Intel(R) Core(TM) i7-4510U CPU @ 2.00GHz(2601 MHz)
8.00 GB (1600 MHz)
500 GB Seagate ST500LM000-SSHD-8GB
Windows 8.1 (64-bits)
```

结果：
```
4.530440549502606 seconds (10 times) - excluding create_mapping().
```

### `json_loads_dumps.py`

测试环境：
```
Intel(R) Core(TM) i7-4510U CPU @ 2.00GHz(2601 MHz)
8.00 GB (1600 MHz)
500 GB Seagate ST500LM000-SSHD-8GB
Windows 8.1 (64-bits)
```

结果：
```
10 times - create_mapping_list(100000): 57.816073 seconds
10 times - test_json_dumps(): 44.095459 seconds
10 times - test_json_loads(): 47.297207 seconds
```

### `msgpack_loads_dumps.py`

测试环境：
```
Intel(R) Core(TM) i7-4510U CPU @ 2.00GHz(2601 MHz)
8.00 GB (1600 MHz)
500 GB Seagate ST500LM000-SSHD-8GB
Windows 8.1 (64-bits)
```

结果：unpackb (loads) 的效果比 json 提升了 61%，效果不错。
```
10 times - create_mapping_list(100000): 56.848185 seconds
10 times - test_msgpack_dumps(): 36.445297 seconds
10 times - test_msgpack_loads(): 18.364738 seconds
```

### `simple_logging_test`

测试环境：
```
Intel(R) Core(TM) i7-4510U CPU @ 2.00GHz(2601 MHz)
8.00 GB (1600 MHz)
500 GB Seagate ST500LM000-SSHD-8GB
Windows 8.1 (64-bits)
```

logging 配置文件：
见 `logger.conf` 文件。
整体来说，`StreamHandler` 的级别设置为 ERROR，打印过程中仅打印 debug 或者 info 级别的，触发不到打印至屏幕的操作。
`handlers.RotatingFileHandler` 的级别设置为可以打印的级别，如 debug 或者 info。

#### `/simple_logging_test.py`

结果：

1. 在没有任何打印输出的情况下，居然空载也会运行这么久。让人很惊讶……
```
StreamHandler: ERROR; handlers.RotatingFileHandler: ERROR;
(==> nothing output to screen; nothing output to file)
single_write_log(100000): 2.769530 seconds
multi_write_log(5, 100000): 14.080553 seconds 
```
2. 使用 `formatter_complete_form` 打印至文件。
```
StreamHandler: ERROR; handlers.RotatingFileHandler: INFO (formatter_complete_form);
(==> nothing output to screen; output to file)
single_write_log(100000): 9.001150 seconds
multi_write_log(5, 100000): 43.990715 seconds
```
3. 使用 `formatter_simple_form` 打印至文件。
```
StreamHandler: ERROR; handlers.RotatingFileHandler: INFO (formatter_simple_form);
(==> nothing output to screen; output to file)
single_write_log(100000): 7.849485 seconds
multi_write_log(5, 100000): 38.619185 seconds
```
相对于 `formatter_complete_form` 的情况，要稍微快一些。

#### `/simple_logging_wrapper_test.py`

做了一个简单的封装，通过设定基本的 `simple_logging_wrapper.LOG_LEVEL_xyz` 参数，做一个基本的过滤，缓解「不输出（空载）也会消耗较多时间」的情况。

```
LOG_LEVEL_DEBUG   
LOG_LEVEL_INFO    
LOG_LEVEL_ERROR   
LOG_LEVEL_CRITICAL
```
空载的运行结果：速度提升了将近30倍（2.769 => 0.093）。
```
10 times - single_write_log(100000): 0.928845 seconds
10 times - multi_write_log(5, 100000): 4.610774 seconds
```

### `big_integer_or_ctypes.py`

测试环境：
```
Intel(R) Core(TM) i7-4510U CPU @ 2.00GHz(2601 MHz)
8.00 GB (1600 MHz)
500 GB Seagate ST500LM000-SSHD-8GB
Windows 8.1 (64-bits)
```

结果：在这里的递增序列取模应用上，ctypes 比 pure python 操作要慢。将大数分割成一个个段 `test_big_integer_segmented` 比直接操作大数 `test_big_integer` 要快一倍多。
```
2 times: test_big_integer(2*10**7): 6.858736 seconds
2 times: test_ctypes(2*10**7): 10.698558 seconds
2 times: test_big_integer_segmented(2*10**7): 3.050504 seconds
2 times: test_ctypes_segmented(2*10**7): 10.599173 seconds
```

### `simple_persistence_shelve/simple_persistence_shelve.py`

测试环境：
```
Intel(R) Core(TM) i7-4510U CPU @ 2.00GHz(2601 MHz)
8.00 GB (1600 MHz)
500 GB Seagate ST500LM000-SSHD-8GB
Windows 8.1 (64-bits)

Python 3.3
```

结果：注意其中的 `writeback=True` 的操作。文件里的注释描述了其含义。

```
r"""Below are the writeback=True version.
Note:
db['key_name'] = [1]        # assignment operation: always update 'key_name' in @db
del db['key_name']          # delete operation: always delete 'key_name' in @db if 'key_name' in db == True
db['key_name'].append(2)    # only work if "writeback=True" option is enabled when open @db
db.sync()                   # only work if "writeback=True" option is enabled when open @db
db.close()                  # automatically call db.sync() when close @db
"""
```

注意其中 `read` 和 `read_faster` 两个版本的差别。因为 `writeback` 测试里，每次 read 都需要读取很大的一个字典，因此读取操作占据了很多时间；如果只是一开始读取（全程只是 r 没有 w），之后从最开始读取的结果里进行查询，就快很多了。
```
create_keywords(10000): 0.008155 seconds
create_unordered_list(10000): 0.051670 seconds
## writeback not used => only assignment or del
test_shelve_insert_new(10000): 3.304961 seconds
test_shelve_random_update(10000): 3.360600 seconds
5 times - test_shelve_random_read(10000): 5.669415 seconds
test_shelve_random_delete(10000): 177.601023 seconds
## writeback used => list append or new map member assignment etc.
test_shelve_insert_new_writeback(10000): 0.019627 seconds
test_shelve_random_update_writeback(10000): 0.042391 seconds
test_shelve_random_read_writeback(10000): 228.622498 seconds
test_shelve_random_read_writeback_faster(10000): 0.026705 seconds
test_shelve_random_delete_writeback(10000): 0.034166 seconds
```

以上是在 windows 下做的测试。其 dbm engine 是 `dbm.dumb` 即最一般化（Python distribution 自带，各个系统可移植）的实现。


以下是在 linux 虚拟机上做的测试（ubuntu 64-bits vmware CPU-virtualization enabled），linux 上的 dbm 是 gnu dbm，从测试结果来看比 dumb dbm 速度要快。
```
create_keywords(10000): 0.008049 seconds
create_unordered_list(10000): 0.034875 seconds
## writeback not used => only assignment or del
test_shelve_insert_new(10000): 0.283538 seconds
test_shelve_random_update(10000): 0.325672 seconds
5 times - test_shelve_random_read(10000): 0.274825 seconds
test_shelve_random_delete(10000): 0.175219 seconds
## writeback used => list append or new map member assignment etc.
test_shelve_insert_new_writeback(10000): 0.050947 seconds
test_shelve_random_update_writeback(10000): 0.041354 seconds
test_shelve_random_read_writeback(10000): 139.833156 seconds
test_shelve_random_read_writeback_faster(10000): 0.020831 seconds
test_shelve_random_delete_writeback(10000): 0.035511 seconds
```
