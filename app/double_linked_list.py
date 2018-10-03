class DoubleLinkedList:
    class Item:

        def __init__(self, value=None, prev=None, next=None):
            self.value = value
            self.prev = prev
            self.next = next

    def __init__(self, inital_value=None):
        self.length = 0
        self.start_item = DoubleLinkedList.Item()