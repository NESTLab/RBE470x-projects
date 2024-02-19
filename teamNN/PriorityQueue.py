import heapq

class PriorityQueue:

    def __init__(self):
        """
        Class constructor.
        """
        self.elements = []

    def empty(self):
        """
        Returns True if the queue is empty, False otherwise.
        """
        return len(self.elements) == 0

    def put(self, element, priority):
        """
        Puts an element in the queue.
        :param element  [any type]     The element.
        :param priority [int or float] The priority.
        """
        for i in range(0, len(self.elements)):
            it = self.elements[i]
            if (it[1] == element):
                if (it[0] > priority):
                    self.elements[i] = (priority, element)
                    heapq.heapify(self.elements)
                return
        heapq.heappush(self.elements, (priority, element))

    def get(self):
        """
        Returns the element with the top priority.
        """
        return heapq.heappop(self.elements)[1]

    def get_queue(self):
        """
        Returns the content of the queue as a list.
	"""
        return self.elements