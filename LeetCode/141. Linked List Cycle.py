# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        HEAD = head
        visited_head = []

        if HEAD is None:
            return False

        while True:
            next_node = HEAD.next

            if next_node in visited_head:
                return True

            elif next_node == None:
                return False

            HEAD = HEAD.next
            visited_head.append(next_node)
