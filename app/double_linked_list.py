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
        """
        Добавляет элемент со значением **data** влево списка

        :param data: Значение, которое будет добавлено
        """
        item = DoubleLinkedList.Node(data)
        if self.head is None:
            self.head = self.tail = item
        else:
            item.prev, item.next = None, self.head
            self.head.prev = item
            self.head = item

    def shift(self, index: int = None):
        """
        Удаляет элемент на **index** позиции слева. Без указания индекса
        удалит самый левый элемент

        :param index: (опционально) Номер удаляемого элемента
        :return: Значение удаленного элемента
        """
        if index is None:
            self.head.next.prev = None
            return self.head.value
        current_item = self.tail
        for _ in range(index):
            current_item = current_item.prev
        current_item.next.prev = current_item.prev
        current_item.prev.next = current_item.next
        return current_item.value

    def remove(self, node_value):
        """
         Удаляет элемент с заданным значением

         :param node_value: Значение удаляемого элемента
         :raises IndexError: если значение не было найдено
         """
        current_node = self.head
        is_found = False

        while current_node is not None:
            if current_node.value == node_value:
                if current_node.prev is not None:
                    current_node.prev.next = current_node.next
                    current_node.next.prev = current_node.prev
                else:
                    self.head = current_node.next
                    current_node.next.prev = None
                is_found = True

            current_node = current_node.next
        if not is_found:
            raise IndexError("No such element!")

    def delete(self, value):
        """
         Удаляет элемент с заданным значением

         :param value: Значение удаляемого элемента
         :raises IndexError: если значение не было найдено
         """
        return self.remove(value)

    def pop(self, index: int = ...):
        """
        Удаляет элемент на **index** позиции справа. Без указания
        индекса удалит самый правый элемент

        :param index: (опционально) Номер удаляемого элемента
        :return: Значение удаленного элемента
        """
        if index is ...:
            try:
                self.tail.prev.next = None
            except AttributeError:
                raise IndexError("The list is empty!")
            return self.tail.value
        current_item = self.head
        for _ in range(index):
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
        for _ in range(item_number):
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
