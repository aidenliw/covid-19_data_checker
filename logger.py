"""
The logger function is using the chain of responsibility pattern

Chain of Responsibility is behavioral design pattern that allows passing request
along the chain of potential handlers until one of them handles request.

reference: https://refactoring.guru/design-patterns/chain-of-responsibility/python/example
"""
from model import *
from abc import ABC, abstractmethod


class Logger(ABC):

    def __init__(self, next_handler):
        self._next_handler = next_handler

    @abstractmethod
    def handle_request(self, message):
        pass

    def log(self, message):
        self.handle_request(message)

        if self._next_handler is not None:
            self._next_handler.log(message)


# save the logs into the local text file
class FileLogHandler(Logger):

    def handle_request(self, message):
        # write the log to the text file
        location = "log.txt"
        output_file = open(location, "a")
        output_file.write(message)
        output_file.close()


# save the logs onto Redis labs database
class RedisLogHandler(Logger):

    def handle_request(self, message):
        # write the log to the redis labs
        r_db = Redis().redis
        counter = r_db.get("log_count")
        if counter is None:
            r_db.set("log_count", 0)
            counter = 0

        index = int(counter) + 1
        r_db.set("log_count", index)
        r_db.set("log" + str(index), message)


# Create chained logger object
chain = FileLogHandler(RedisLogHandler(None))



