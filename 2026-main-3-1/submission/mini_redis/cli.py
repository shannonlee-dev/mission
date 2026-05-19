import shlex
import sys

from .store import MiniRedisStore


class MiniRedisCLI:
    """Command parser and REPL for Mini Redis."""

    def __init__(self, store=None, output=None):
        self.store = store if store is not None else MiniRedisStore()
        self.output = output if output is not None else sys.stdout

    def execute_line(self, line):
        try:
            parts = shlex.split(line)
        except ValueError:
            return "(error) ERR invalid syntax"
        if not parts:
            return None
        command = parts[0].upper()
        if command == "EXIT" or command == "QUIT":
            return "__QUIT__"
        if command == "SET":
            return self._require(command, parts, 3, self._set)
        if command == "GET":
            return self._require(command, parts, 2, self._get)
        if command == "DEL":
            return self._require(command, parts, 2, self._del)
        if command == "EXISTS":
            return self._require(command, parts, 2, self._exists)
        if command == "DBSIZE":
            return self._require(command, parts, 1, self._dbsize)
        if command == "KEYS":
            return self._require(command, parts, 1, self._keys)
        if command == "CONFIG":
            return self._config(parts)
        if command == "INFO":
            return self._info(parts)
        if command == "EXPIRE":
            return self._require(command, parts, 3, self._expire)
        if command == "TTL":
            return self._require(command, parts, 2, self._ttl)
        if command == "PUBLISH":
            return self._require(command, parts, 3, self._publish)
        if command == "SUBSCRIBE":
            return self._require(command, parts, 2, self._subscribe)
        return "(error) ERR unknown command '%s'" % parts[0]

    def run(self, input_stream=None):
        stream = input_stream if input_stream is not None else sys.stdin
        interactive = stream.isatty()
        while True:
            self.output.write("mini-redis> ")
            self.output.flush()
            line = stream.readline()
            if line == "":
                self.output.write("\n")
                self.output.flush()
                break
            result = self.execute_line(line.strip())
            if result == "__QUIT__":
                break
            if result is not None:
                self._write_result(result)
            if not interactive:
                self.output.flush()

    def _write_result(self, result):
        if isinstance(result, list):
            for line in result:
                self.output.write(str(line) + "\n")
        else:
            self.output.write(str(result) + "\n")

    def _require(self, command, parts, expected, handler):
        if len(parts) != expected:
            return "(error) ERR wrong number of arguments for '%s' command" % command
        return handler(parts)

    def _set(self, parts):
        return self.store.set(parts[1], parts[2])

    def _get(self, parts):
        value = self.store.get(parts[1])
        if value is None:
            return "(nil)"
        return '"%s"' % value

    def _del(self, parts):
        return "(integer) %d" % self.store.delete(parts[1])

    def _exists(self, parts):
        return "(integer) %d" % self.store.exists(parts[1])

    def _dbsize(self, parts):
        return "(integer) %d" % self.store.dbsize()

    def _keys(self, parts):
        keys = self.store.keys()
        if not keys:
            return "(empty array)"
        lines = []
        number = 1
        for key in keys:
            lines.append('%d. "%s"' % (number, key))
            number += 1
        return lines

    def _config(self, parts):
        if len(parts) != 4 or parts[1].upper() != "SET" or parts[2].lower() != "maxmemory":
            return "(error) ERR wrong number of arguments for 'CONFIG' command"
        return self.store.config_set_maxmemory(parts[3])

    def _info(self, parts):
        if len(parts) != 2 or parts[1].lower() != "memory":
            return "(error) ERR wrong number of arguments for 'INFO' command"
        return self.store.info_memory()

    def _expire(self, parts):
        return self.store.expire(parts[1], parts[2])

    def _ttl(self, parts):
        return "(integer) %d" % self.store.ttl(parts[1])

    def _publish(self, parts):
        return "(integer) %d" % self.store.publish(parts[1], parts[2])

    def _subscribe(self, parts):
        count = self.store.subscribe(parts[1])
        return 'subscribed to "%s" (%d)' % (parts[1], count)

