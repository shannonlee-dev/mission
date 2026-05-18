class DynamicArray:
    """A small growable array used by bonus exercises and tests."""

    def __init__(self, initial_capacity=4):
        self._capacity = max(1, initial_capacity)
        self._size = 0
        self._items = [None] * self._capacity

    def __len__(self):
        return self._size

    def capacity(self):
        return self._capacity

    def append(self, value):
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        self._items[self._size] = value
        self._size += 1

    def get(self, index):
        self._check_index(index)
        return self._items[index]

    def set(self, index, value):
        self._check_index(index)
        self._items[index] = value

    def remove(self, index):
        self._check_index(index)
        value = self._items[index]
        for pos in range(index, self._size - 1):
            self._items[pos] = self._items[pos + 1]
        self._size -= 1
        self._items[self._size] = None
        return value

    def to_list(self):
        result = []
        for index in range(self._size):
            result.append(self._items[index])
        return result

    def _resize(self, new_capacity):
        new_items = [None] * new_capacity
        for index in range(self._size):
            new_items[index] = self._items[index]
        self._items = new_items
        self._capacity = new_capacity

    def _check_index(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")

