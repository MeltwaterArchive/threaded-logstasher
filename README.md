# DEPRECATED
This repository is no longer activiely maintained.

If you are looking for similar functionality but for more uptodate versions of Python, we recommend you take a look at https://github.com/vklochan/python-logstash as an alternative.

# threaded-logstasher
This library is provided to allow standard python logging to send log data
as json objects to logstash.

## Installing
Pip:

    pip install git+https://github.com/meltwater/threaded-logstasher.git

## Usage
```python
    import logging
    from logstasher import LogstashHandler, LogstashFormatterExtra

    logger = logging.getLogger('')
    logger.setLevel(logging.INFO)
    handler = LogstashHandler('192.168.1.100', 4560,
                              threads=3, queue_size=100)
    formatter = LogstashFormatterExtra(source_host='example.com', always='value')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.info('See what you get', extra=dict(param1='value1'))
```

The library provides a handler and a formatter class:
``LogstashHandler`` and ``LogstashFormatterExtra``. The handler implements a
threadpool to separate network communication from the application logic, thus
the calling thread is not blocked by any socket call.

The messages are formatted and put immediately to an internal
[queue](https://docs.python.org/3.4/library/queue.html#queue.Queue).
The worker threads deliver messages to the logstash daemon using a slightly
modified version of [``logging.handlers.SocketHandler``](https://docs.python.org/3.4/library/logging.handlers.html#logging.handlers.SocketHandler).

``LogstashHandler`` takes the following parameters:
  * ``host``: hostname of the logstash receiver daemon.
  * ``port``: port of the logstash receiver daemon.
  * ``level``: the threshold level for this handler (default=INFO)
  * ``threads``: the number of worker threads connecting to logstash daemon.
  * ``queue_size``: size of the queue used for buffering log messages.
  * ``timeout``: floating point number specifying a timeout for sending remaining messages to logstash receiver when the handler is closed. Timeout is specified in seconds.

``LogstashFormatterExtra`` is a wrapper class above ``LogstashFormatterV1`` from
[logstash_formatter](https://github.com/exoscale/python-logstash-formatter) library.
It is added to this library for convenience and may take the following named
parameters other than what is inherited from its super class:
  * ``source_host``: custom hostname of your application.
  * any additional keyword arguments will be added as an extra field to every JSON log.

## Sample output

The result of the ``logger.info`` call in the example above:

```javascript
    {
               "filename" => "test_logstasher.py",
            "processName" => "MainProcess",
               "funcName" => "<module>",
               "pathname" => "test_logstasher.py",
                   "args" => [],
             "@timestamp" => "2016-01-12T13:17:14.177Z",
                "levelno" => 20,
                 "param1" => "value1",
                "process" => 15852,
            "source_host" => "example.com",
             "stack_info" => nil,
                 "thread" => 140735093338112,
             "threadName" => "MainThread",
                 "always" => "value",
                  "msecs" => 177.3838996887207,
                "message" => "See what you get",
              "levelname" => "INFO",
                   "name" => "root",
                "created" => 1452604634.177384,
                 "lineno" => 13,
               "@version" => 1,
                 "module" => "test_logstasher",
        "relativeCreated" => 10.72382926940918,
                   "host" => "192.168.99.1"
    }
```
