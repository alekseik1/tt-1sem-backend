class DoubleLinkedList(list):
    class Node:

        def __init__(self, value=None, prev=None, next=None):
            self.value = value
            self.prev = prev
            self.next = next

    def __init__(self, seq=()):
        self.head = None
        self.tail = None
        super().__init__(seq)

    def append(self, data):
        item = DoubleLinkedList.Node(data)
        if self.head is None:
            self.head = self.tail = item
        else:
            item.prev, item.next = self.tail, None
            self.tail.next = item
            self.tail = item

    def push(self, data):
        return self.append(data)

    def unshift(self, data):
        item = DoubleLinkedList.Node(data)
        if self.head is None:
            self.head = self.tail = item
        else:
            item.prev, item.next = None, self.head
            self.head.prev = item
            self.head = item

    def shift(self, index: int = None):
        if index is None:
            self.head.next.prev = None
            return self.head.value
        else:
            current_item = self.tail
            for i in range(index):
                current_item = current_item.prev
            current_item.next.prev = current_item.prev
            current_item.prev.next = current_item.next
            return current_item.value

    def remove(self, node_value):
        current_node = self.head

        while current_node is not None:
            if current_node.data == node_value:
                if current_node.prev is not None:
                    current_node.prev.next = current_node.next
                    current_node.next.prev = current_node.prev
                else:
                    self.head = current_node.next
                    current_node.next.prev = None

            current_node = current_node.next

    def delete(self, value):
        return self.remove(value)

    def pop(self, index: int = ...):
        if index is ...:
            try:
                self.tail.prev.next = None
            except AttributeError as e:
                raise IndexError("The list is empty!")
            return self.tail.value
        else:
            current_item = self.head
            for i in range(index):
                current_item = current_item.next
            current_item.prev.next = current_item.next
            current_item.next.prev = current_item.prev
            return current_item.value

    def contains(self, value):
        return value in self

    def first(self):
        return self.head

    def last(self):
        return self.tail

    def __getitem__(self, item_number):
        curr_item = self.head
        if curr_item is None:
            # Такое бывает, когда пытаемся что-то получить из пустого списка
            raise IndexError("Empty list")
        for i in range(item_number):
            if curr_item.next is None:
                raise IndexError("Reached end of the list")
            curr_item = curr_item.next
        return curr_item.value

    def __len__(self):
        curr_item = self.head
        length = 0
        while curr_item is not None:
            length += 1
            curr_item = curr_item.next
        return length

    def __contains__(self, value):
        curr_item = self.head
        while curr_item is not None:
            if curr_item.value == value:
                return True
            curr_item = curr_item.next
