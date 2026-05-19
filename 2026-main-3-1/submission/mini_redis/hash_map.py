from .linked_list import DoublyLinkedList


class HashMapEntry:
    """Single chaining entry for the custom hash map."""

    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashMap:
    """A separate-chaining hash map with a simple deterministic hash."""

    def __init__(self, initial_capacity=8):
        self._capacity = max(2, initial_capacity)
        self._buckets = [None] * self._capacity
        self._size = 0

    def size(self):
        return self._size

    def put(self, key, value):
        if (self._size + 1) / self._capacity > 0.75:
            self._resize(self._capacity * 2)
        return self._put_no_resize(key, value)

    def get(self, key, default=None):
        node = self._find_node(key)
        if node is None:
            return default
        return node.data.value

    def remove(self, key):
        bucket = self._bucket_for(key)
        if bucket is None:
            return None
        current = bucket.head
        while current is not None:
            if current.data.key == key:
                entry = bucket.remove_node(current)
                self._size -= 1
                return entry.value
            current = current.next
        return None

    def contains(self, key):
        return self._find_node(key) is not None

    def keys(self):
        result = []
        for bucket in self._buckets:
            if bucket is not None:
                for entry in bucket.iter_values():
                    result.append(entry.key)
        return result

    def items(self):
        result = []
        for bucket in self._buckets:
            if bucket is not None:
                for entry in bucket.iter_values():
                    result.append((entry.key, entry.value))
        return result

    def _put_no_resize(self, key, value):
        index = self._index_for(key)
        if self._buckets[index] is None:
            self._buckets[index] = DoublyLinkedList()
        current = self._buckets[index].head
        while current is not None:
            if current.data.key == key:
                old = current.data.value
                current.data.value = value
                return old
            current = current.next
        self._buckets[index].insert_back(HashMapEntry(key, value))
        self._size += 1
        return None

    def _resize(self, new_capacity):
        old_items = self.items()
        self._capacity = new_capacity
        self._buckets = [None] * self._capacity
        self._size = 0
        for key, value in old_items:
            self._put_no_resize(key, value)

    def _hash(self, key):
        text = str(key)
        value = 2166136261
        for char in text:
            value = value ^ ord(char)
            value = (value * 16777619) & 0xFFFFFFFF
        return value

    def _index_for(self, key):
        return self._hash(key) % self._capacity

    def _bucket_for(self, key):
        return self._buckets[self._index_for(key)]

    def _find_node(self, key):
        bucket = self._bucket_for(key)
        if bucket is None:
            return None
        current = bucket.head
        while current is not None:
            if current.data.key == key:
                return current
            current = current.next
        return None

