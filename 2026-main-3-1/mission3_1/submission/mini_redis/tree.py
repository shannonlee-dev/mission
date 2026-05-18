from .linked_list import DoublyLinkedList


class BinaryTreeNode:
    """Node for binary tree traversal exercises."""

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class BinaryTree:
    """Binary tree with common traversal algorithms."""

    def __init__(self, root=None):
        self.root = root

    def preorder(self):
        result = []
        self._preorder(self.root, result)
        return result

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def postorder(self):
        result = []
        self._postorder(self.root, result)
        return result

    def level_order(self):
        result = []
        if self.root is None:
            return result
        queue = DoublyLinkedList()
        queue.insert_back(self.root)
        while queue.size() > 0:
            node = queue.remove_front()
            result.append(node.value)
            if node.left is not None:
                queue.insert_back(node.left)
            if node.right is not None:
                queue.insert_back(node.right)
        return result

    def _preorder(self, node, result):
        if node is None:
            return
        result.append(node.value)
        self._preorder(node.left, result)
        self._preorder(node.right, result)

    def _inorder(self, node, result):
        if node is None:
            return
        self._inorder(node.left, result)
        result.append(node.value)
        self._inorder(node.right, result)

    def _postorder(self, node, result):
        if node is None:
            return
        self._postorder(node.left, result)
        self._postorder(node.right, result)
        result.append(node.value)


class BinarySearchTree:
    """Binary search tree supporting insert, search, delete, and sorted traversal."""

    def __init__(self):
        self.root = None

    def insert(self, value):
        self.root = self._insert(self.root, value)

    def contains(self, value):
        current = self.root
        while current is not None:
            if value == current.value:
                return True
            if value < current.value:
                current = current.left
            else:
                current = current.right
        return False

    def delete(self, value):
        self.root = self._delete(self.root, value)

    def inorder(self):
        return BinaryTree(self.root).inorder()

    def _insert(self, node, value):
        if node is None:
            return BinaryTreeNode(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        return node

    def _delete(self, node, value):
        if node is None:
            return None
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            successor = self._minimum(node.right)
            node.value = successor.value
            node.right = self._delete(node.right, successor.value)
        return node

    def _minimum(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

