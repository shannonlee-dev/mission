class HeapItem:
    """Comparable heap item used for TTL expiration records."""

    def __init__(self, expire_at, key):
        self.expire_at = expire_at
        self.key = key

    def less_than(self, other):
        if self.expire_at == other.expire_at:
            return self.key < other.key
        return self.expire_at < other.expire_at


class MinHeap:
    """Array-backed minimum heap with explicit heapify operations."""

    def __init__(self):
        self._items = []

    def size(self):
        return len(self._items)

    def push(self, item):
        self._items.append(item)
        self._heapify_up(len(self._items) - 1)

    def pop(self):
        if not self._items:
            return None
        minimum = self._items[0]
        last = self._items.pop()
        if self._items:
            self._items[0] = last
            self._heapify_down(0)
        return minimum

    def peek(self):
        if not self._items:
            return None
        return self._items[0]

    def _heapify_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if not self._items[index].less_than(self._items[parent]):
                break
            self._swap(index, parent)
            index = parent

    def _heapify_down(self, index):
        size = len(self._items)
        while True:
            left = index * 2 + 1
            right = left + 1
            smallest = index
            if left < size and self._items[left].less_than(self._items[smallest]):
                smallest = left
            if right < size and self._items[right].less_than(self._items[smallest]):
                smallest = right
            if smallest == index:
                break
            self._swap(index, smallest)
            index = smallest

    def _swap(self, left, right):
        self._items[left], self._items[right] = self._items[right], self._items[left]

