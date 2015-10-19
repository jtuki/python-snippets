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

#### `msgpack_loads_dumps.py`

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