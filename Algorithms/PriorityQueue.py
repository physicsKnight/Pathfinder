class MinHeap:
    def __init__(self, arr = []):
        self.heap = arr
        self.size = len(arr)

    # the heap is an array so parent is i / 2
    # left node is 2 * i + 1, right node is 2 * i + 2
    def getParentIndex(self, i): return (i - 1) // 2
    def getLeftIndex(self, i): return 2*i+1
    def getRightIndex(self, i): return 2*i+2
    def hasParent(self, i): return self.getParentIndex(i) >= 0
    def hasLeft(self, i): return self.getLeftIndex(i) < self.size
    def hasRight(self, i): return self.getRightIndex(i) < self.size
    def parent(self, i): return self.heap[self.getParentIndex(i)]
    def left(self, i): return self.heap[self.getLeftIndex(i)]
    def right(self, i): return self.heap[self.getRightIndex(i)]

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def heapify_up(self):
        i = self.size - 1
        # while the inserted item is still smaller
        # than its parent, swap them. Keep doing this until
        # it bubbles up to the root or as far as it can go.
        while self.hasParent(i) and self.heap[i][0] < self.parent(i)[0]:
            j = self.getParentIndex(i)
            self.swap(i, j)
            i = j

    def heapify_down(self):
        i = 0
        while self.hasLeft(i):
            # find the smallest child index, left or right
            smallest = self.getLeftIndex(i)
            if self.hasRight(i) and self.right(i)[0] < self.left(i)[0]:
                smallest = self.getRightIndex(i)
            
            # if the parent is smaller than both children
            # then we can stop here since its a min heap
            if self.heap[i][0] <= self.heap[smallest][0]:
                break
            # if parent is larger then swap it with smallest
            self.swap(i, smallest)
            # set current index to smallest child and repeat
            i = smallest
            

    # Push an item to the end of an array
    # and adjust the array by bubbling up
    def push(self, item):
        self.heap.append(item)
        self.size += 1
        self.heapify_up()

    # Pop the item at the front of the array
    def pop(self):
        if self.size == 0:
            return None
        
        front = self.heap[0]
        if self.size == 1:
            self.size -= 1
            return self.heap.pop()
        
        self.heap[0] = self.heap.pop()
        self.size -= 1
        self.heapify_down()
        return front
    