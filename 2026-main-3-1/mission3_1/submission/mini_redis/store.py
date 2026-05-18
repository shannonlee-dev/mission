import time

from .hash_map import HashMap
from .linked_list import DoublyLinkedList
from .min_heap import HeapItem, MinHeap


class StoreEntry:
    """Value object stored in the custom hash map."""

    def __init__(self, value):
        self.value = value


class ChannelState:
    """In-memory channel state for the Pub/Sub command pair."""

    def __init__(self):
        self.subscribers = 0
        self.messages = DoublyLinkedList()


class MiniRedisStore:
    """String key-value store with TTL, LRU eviction, and memory accounting."""

    def __init__(self, clock=None):
        self._data = HashMap()
        self._expires = HashMap()
        self._expire_heap = MinHeap()
        self._lru = DoublyLinkedList()
        self._lru_nodes = HashMap()
        self._channels = HashMap()
        self._maxmemory = 0
        self._used_memory = 0
        self._evicted_keys = 0
        self._clock = clock if clock is not None else time.time

    def set(self, key, value):
        self._delete_expired()
        entry_size = self._entry_size(key, value)
        if self._maxmemory > 0 and entry_size > self._maxmemory:
            return "(error) OOM command not allowed when used_memory > 'maxmemory'"
        existing = self._data.get(key)
        old_value = existing.value if existing is not None else None
        old_size = self._entry_size(key, old_value) if old_value is not None else 0
        projected = self._used_memory - old_size + entry_size
        if existing is None:
            self._data.put(key, StoreEntry(value))
            self._used_memory += entry_size
            self._add_lru(key)
        else:
            existing.value = value
            self._used_memory = projected
            self._touch_lru(key)
        self._expires.remove(key)
        self._evict_if_needed()
        return "OK"

    def get(self, key):
        if self._is_expired(key):
            self._delete_key(key)
            return None
        entry = self._data.get(key)
        if entry is None:
            return None
        self._touch_lru(key)
        return entry.value

    def delete(self, key):
        self._delete_expired()
        if not self._data.contains(key):
            return 0
        self._delete_key(key)
        return 1

    def exists(self, key):
        if self._is_expired(key):
            self._delete_key(key)
            return 0
        return 1 if self._data.contains(key) else 0

    def dbsize(self):
        self._delete_expired()
        return self._data.size()

    def keys(self):
        self._delete_expired()
        return self._data.keys()

    def config_set_maxmemory(self, value_text):
        value = self._parse_non_negative_integer(value_text)
        if value is None:
            return "(error) ERR value is not an integer or out of range"
        self._maxmemory = value
        self._evict_if_needed()
        return "OK"

    def info_memory(self):
        self._delete_expired()
        return [
            "used_memory:%d" % self._used_memory,
            "maxmemory:%d" % self._maxmemory,
            "evicted_keys:%d" % self._evicted_keys,
        ]

    def expire(self, key, seconds_text):
        self._delete_expired()
        seconds = self._parse_integer(seconds_text)
        if seconds is None:
            return "(error) ERR value is not an integer or out of range"
        if not self._data.contains(key):
            return "(integer) 0"
        if seconds <= 0:
            self._delete_key(key)
            return "(integer) 1"
        expire_at = self._clock() + seconds
        self._expires.put(key, expire_at)
        self._expire_heap.push(HeapItem(expire_at, key))
        return "(integer) 1"

    def ttl(self, key):
        if self._is_expired(key):
            self._delete_key(key)
            return -2
        if not self._data.contains(key):
            return -2
        expire_at = self._expires.get(key)
        if expire_at is None:
            return -1
        remaining = int(expire_at - self._clock())
        if remaining < 0:
            remaining = 0
        return remaining

    def publish(self, channel, message):
        state = self._channels.get(channel)
        if state is None:
            return 0
        state.messages.insert_back(message)
        return state.subscribers

    def subscribe(self, channel):
        state = self._channels.get(channel)
        if state is None:
            state = ChannelState()
            self._channels.put(channel, state)
        state.subscribers += 1
        return state.subscribers

    def used_memory(self):
        self._delete_expired()
        return self._used_memory

    def maxmemory(self):
        return self._maxmemory

    def evicted_keys(self):
        return self._evicted_keys

    def _delete_expired(self):
        now = self._clock()
        while self._expire_heap.size() > 0:
            item = self._expire_heap.peek()
            if item.expire_at > now:
                break
            self._expire_heap.pop()
            current_expire = self._expires.get(item.key)
            if current_expire is not None and current_expire <= now and current_expire == item.expire_at:
                self._delete_key(item.key)

    def _is_expired(self, key):
        expire_at = self._expires.get(key)
        return expire_at is not None and expire_at <= self._clock()

    def _delete_key(self, key):
        entry = self._data.remove(key)
        if entry is None:
            self._expires.remove(key)
            self._remove_lru(key)
            return False
        self._used_memory -= self._entry_size(key, entry.value)
        self._expires.remove(key)
        self._remove_lru(key)
        return True

    def _add_lru(self, key):
        node = self._lru.insert_front(key)
        self._lru_nodes.put(key, node)

    def _touch_lru(self, key):
        node = self._lru_nodes.get(key)
        if node is None:
            self._add_lru(key)
            return
        new_node = self._lru.move_to_front(node)
        self._lru_nodes.put(key, new_node)

    def _remove_lru(self, key):
        node = self._lru_nodes.remove(key)
        if node is not None:
            self._lru.remove_node(node)

    def _evict_if_needed(self):
        if self._maxmemory <= 0:
            return
        while self._used_memory > self._maxmemory and self._lru.tail is not None:
            lru_key = self._lru.tail.data
            if self._delete_key(lru_key):
                self._evicted_keys += 1

    def _entry_size(self, key, value):
        return len(str(key).encode("utf-8")) + len(str(value).encode("utf-8"))

    def _parse_integer(self, text):
        try:
            return int(text)
        except (TypeError, ValueError):
            return None

    def _parse_non_negative_integer(self, text):
        value = self._parse_integer(text)
        if value is None or value < 0:
            return None
        return value

