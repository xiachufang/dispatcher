# dispatcher[![Build Status](https://travis-ci.org/xiachufang/dispatcher.svg?branch=master)](https://travis-ci.org/xiachufang/dispatcher)
Dispatcher 是从 Django 源码 signal 中分离出来的。 Receiver 处理函数是在 celery 异步任务中执行。Celery 被异常终止，receiver 跑异常等情况都会自动重试，直到达到最大重试次数。

所有的 receiver 处理函数必须定义在以 `receiver.py` 结尾的文件中。

```
init_dispatcher('.', '.', logger)
```

第一个参数表示要扫描 receiver 的目录，第二个参数表示项目根路径的 pythonpath。

# Usage
https://docs.djangoproject.com/en/1.10/topics/signals/#defining-and-sending-signals

# Example
1. Start celery
    
    ```bash
    celery -A task worker
    ```

2. Send the signal

    ```bash
    python test.py
    ```

