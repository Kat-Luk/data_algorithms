class SequentialList:

    # O(capacity) 
    #creates a fixed-size array filled with None
    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self.data = [None] * capacity
        self.length = 0

    # O(1) just compares length to 0
    def is_empty(self):
        return self.length == 0

    # O(1) returns the stored counter
    def size(self):
        return self.length

    # O(n) worst case, loop runs length - index times
    # Elements from index onward are shifted to the right
    def insert(self, index, value):
        if self.length >= self.capacity:
            raise OverflowError("List is full")
        if index < 0 or index > self.length:
            raise IndexError("Index out of bounds")
        for i in range(self.length, index, -1):
            self.data[i] = self.data[i - 1]
        self.data[index] = value
        self.length += 1

    # O(1) loop runs length - length = 0 times
    def append(self, value):
        self.insert(self.length, value)

    # O(n) loop runs length - 0 = length times
    def prepend(self, value):
        self.insert(0, value)

    # O(n) worst case, loop runs length - 1 - index times
    # Elements after index are shifted to the left
    def delete(self, index):
        if index < 0 or index >= self.length:
            raise IndexError("Index out of bounds")
        removed = self.data[index]
        for i in range(index, self.length - 1):
            self.data[i] = self.data[i + 1]
        self.data[self.length - 1] = None
        self.length -= 1
        return removed

    # O(n) find() searches, then delete() shifts
    def delete_by_value(self, value):
        index = self.find(value)
        if index == -1:
            return False
        self.delete(index)
        return True

    # O(n) every remaining element shifts left
    def delete_head(self):
        return self.delete(0)

    # O(1) loop runs 0 times, nothing shifts
    def delete_tail(self):
        return self.delete(self.length - 1)

    # O(1) direct indexing
    def get(self, index):
        if index < 0 or index >= self.length:
            raise IndexError("Index out of bounds")
        return self.data[index]

    # O(1) direct indexing
    def update(self, index, value):
        if index < 0 or index >= self.length:
            raise IndexError("Index out of bounds")
        self.data[index] = value

    # O(n) checks each element until a match
    def find(self, value):
        for i in range(self.length):
            if self.data[i] == value:
                return i
        return -1

    # O(n) visits each element once
    def display(self):
        text = "["
        for i in range(self.length):
            if i > 0:
                text += ", "
            text += str(self.data[i])
        text += "]"
        print(text)

    # O(n) swaps from both ends toward the middle, n/2 swaps
    def reverse(self):
        left = 0
        right = self.length - 1
        while left < right:
            self.data[left], self.data[right] = self.data[right], self.data[left]
            left += 1
            right -= 1

    # O(n) sets every used slot back to None
    def clear(self):
        for i in range(self.length):
            self.data[i] = None
        self.length = 0


#test cases
if __name__ == "__main__":
    sl = SequentialList(5)
    print("empty:", sl.is_empty(), "size:", sl.size()) # True 0

    sl.append(20)
    sl.append(30)
    sl.prepend(10)
    sl.insert(3, 40)
    sl.display() # [10, 20, 30, 40]
    print("size:", sl.size()) # 4

    print("get(1):", sl.get(1)) # 20
    sl.update(1, 25)
    sl.display() # [10, 25, 30, 40]
    print("find(30):", sl.find(30), "find(99):", sl.find(99)) # 2 -1

    print("delete(1):", sl.delete(1)) # 25
    print("delete_head:", sl.delete_head()) # 10
    print("delete_tail:", sl.delete_tail()) # 40
    sl.display() # [30]

    sl.append(50)
    sl.append(60)
    print("delete_by_value(50):", sl.delete_by_value(50)) # True
    print("delete_by_value(99):", sl.delete_by_value(99)) # False
    sl.display() # [30, 60]

    sl.append(70)
    sl.reverse()
    sl.display() # [70, 60, 30]

    sl.clear()
    print("after clear:", sl.is_empty()) # True