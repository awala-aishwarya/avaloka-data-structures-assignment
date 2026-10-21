import heapq


class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """Least Recently Used cache with average O(1) get and put."""

    def __init__(self, capacity):
        self.capacity = max(0, capacity)
        self.nodes = {}
        self.head = Node()  # Most-recently-used side
        self.tail = Node()  # Least-recently-used side
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _mark_recent(self, node):
        self._remove(node)
        self._add_to_front(node)

    def get(self, key):
        node = self.nodes.get(key)
        if node is None:
            return -1
        self._mark_recent(node)
        return node.value

    def put(self, key, value):
        if self.capacity == 0:
            return
        node = self.nodes.get(key)
        if node is not None:
            node.value = value
            self._mark_recent(node)
            return
        if len(self.nodes) == self.capacity:
            least_recent = self.tail.prev
            self._remove(least_recent)
            del self.nodes[least_recent.key]
        new_node = Node(key, value)
        self.nodes[key] = new_node
        self._add_to_front(new_node)


def can_attend_all(events):
    """Return True if no two events overlap; adjacent events are allowed."""
    ordered = sorted(events, key=lambda event: event[0])
    for i in range(1, len(ordered)):
        if ordered[i - 1][1] > ordered[i][0]:
            return False
    return True


def min_rooms_required(events):
    """Return the minimum rooms needed for all events."""
    if not events:
        return 0
    ordered = sorted(events, key=lambda event: event[0])
    active_end_times = []
    max_rooms = 0
    for start, end in ordered:
        while active_end_times and active_end_times[0] <= start:
            heapq.heappop(active_end_times)
        heapq.heappush(active_end_times, end)
        max_rooms = max(max_rooms, len(active_end_times))
    return max_rooms


if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put(1, 100)
    cache.put(2, 200)
    assert cache.get(1) == 100
    cache.put(3, 300)  # Evicts key 2
    assert cache.get(2) == -1
    assert cache.get(3) == 300
    cache.put(4, 400)  # Evicts key 1
    assert cache.get(1) == -1
    assert cache.get(3) == 300
    assert cache.get(4) == 400

    adjacent_events = [(9, 10), (10, 11), (11, 12)]
    overlapping_events = [(9, 11), (10, 12), (11, 13)]
    assert can_attend_all(adjacent_events) is True
    assert min_rooms_required(adjacent_events) == 1
    assert can_attend_all(overlapping_events) is False
    assert min_rooms_required(overlapping_events) == 2
    assert can_attend_all([]) is True
    assert min_rooms_required([]) == 0

    print("All assignment tests passed.")
