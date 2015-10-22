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

#### `simple_logging_wrapper_test.py`

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
