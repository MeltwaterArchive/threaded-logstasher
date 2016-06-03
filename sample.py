#!/usr/bin/env python

if __name__ == "__main__":
    import logging
    from logstasher import LogstashHandler, LogstashFormatterExtra
    import sys

    logger = logging.getLogger('')
    logger.setLevel(logging.INFO)
    handler = LogstashHandler('192.168.99.100', 4560,
                              threads=3, queue_size=100)
    formatter = LogstashFormatterExtra(source_host='example.com',
                                       python=tuple(sys.version_info))
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.info('See what you get', extra=dict(param1='value1'))
