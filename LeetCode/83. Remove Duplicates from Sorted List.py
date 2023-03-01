# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = new_head = last_node = None

        while head is not None:
            if head.val != prev:
                value = prev = head.val
                new_node = ListNode(value)

                if new_head is None:
                    new_head = last_node = new_node

                else:
                    last_node.next = new_node
                    last_node = new_node

            head = head.next

        return new_head
