#!/usr/bin/env python
from logstash_formatter import LogstashFormatterV1, _default_json_default

class LogstashFormatterExtra(LogstashFormatterV1):
    def __init__(self,
                 datefmt=None,
                 json_cls=None,
                 json_default=_default_json_default,
                 source_host=None, **extra):
        super(LogstashFormatterExtra, self).__init__(None, datefmt, json_cls, json_default)
        self.defaults.update(extra)
        if source_host:
            self.source_host = source_host

