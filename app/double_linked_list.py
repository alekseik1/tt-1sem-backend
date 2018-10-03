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

    def pop(self, index: int = ...):
        if index is ...:
            self.tail.prev.next = None
            return self.tail.value
        else:
            current_item = self.head
            for i in range(index):
                current_item = current_item.next
            current_item.prev.next = current_item.next
            current_item.next.prev = current_item.prev
            return current_item.value

    def __getitem__(self, item_number):
        curr_item = self.head
        for i in range(item_number):
            curr_item = curr_item.next
        return curr_item.value

    def __len__(self):
        curr_item = self.head
        length = 0
        while curr_item is not None:
            length += 1
            curr_item = curr_item.next
        return length
