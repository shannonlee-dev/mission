class LinkedListNode:
    """Node for a doubly linked list."""

    def __init__(self, data):
        self.prev = None
        self.next = None
        self.data = data


class DoublyLinkedList:
    """Doubly linked list with O(1) insert, remove, and move operations."""

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def size(self):
        return self._size

    def insert_front(self, data):
        node = LinkedListNode(data)
        node.next = self.head
        if self.head is not None:
            self.head.prev = node
        else:
            self.tail = node
        self.head = node
        self._size += 1
        return node

    def insert_back(self, data):
        node = LinkedListNode(data)
        node.prev = self.tail
        if self.tail is not None:
            self.tail.next = node
        else:
            self.head = node
        self.tail = node
        self._size += 1
        return node

    def remove_front(self):
        if self.head is None:
            return None
        return self.remove_node(self.head)

    def remove_back(self):
        if self.tail is None:
            return None
        return self.remove_node(self.tail)

    def remove_node(self, node):
        if node is None:
            return None
        if node.prev is not None:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next is not None:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        node.prev = None
        node.next = None
        self._size -= 1
        return node.data

    def move_to_front(self, node):
        if node is None or node is self.head:
            return node
        if node.prev is not None:
            node.prev.next = node.next
        if node.next is not None:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        node.prev = None
        node.next = self.head
        if self.head is not None:
            self.head.prev = node
        self.head = node
        if self.tail is None:
            self.tail = node
        return node

    def iter_values(self):
        current = self.head
        while current is not None:
            yield current.data
            current = current.next
