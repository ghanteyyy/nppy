# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def UpdateNode(self, val):
        temp = self.new_head
        newNode = ListNode(val)

        if temp == None:
            self.new_head = self.lastNode = newNode

        else:
            self.lastNode.next = newNode
            self.lastNode = newNode

    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        self.new_head = self.lastNode = None

        while list1 and list2:
            val1 = list1.val
            val2 = list2.val

            if val1 == val2:
                self.UpdateNode(val1)
                self.UpdateNode(val1)

                list1 = list1.next
                list2 = list2.next

            elif val1 < val2:
                self.UpdateNode(val1)
                list1 = list1.next

            else:
                self.UpdateNode(val2)
                list2 = list2.next

        while list1:
            self.UpdateNode(list1.val)
            list1 = list1.next

        while list2:
            self.UpdateNode(list2.val)
            list2 = list2.next

        return self.new_head
