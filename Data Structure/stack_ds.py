class Stack:
    '''Stack is a data structure where data are stored in a list such that the
      last stored elements are accessible at first and the first data is accessible
      at the last i.e First In Last Out(FILO) or Last In First Out(LIFO))'''

    def __init__(self):
        self.stack = []

    def push(self, value):
        '''Appends "value" to the list'''

        self.stack.append(value)

    def pop(self):
        '''Removes and returns the last element fr the list

        Raises IndexError: stack is empty  -> if the list is empty'''

        if self.is_empty():
            raise IndexError('Stack is empty')

        return self.stack.pop()

    def get_stack(self):
        '''Returns the whole list'''

        return self.stack

    def peek(self):
        '''Returns the last element of the list

          Raises IndexError: stack index is out of range   -> if the list is empty'''

        if self.is_empty():
            raise IndexError('Stack index out of range')

        return self.stack[-1]

    def length(self):
        '''Returns the length of the list'''

        return len(self.stack)

    def is_empty(self):
        '''Returns True if the length of the list is zero (i.e Empty) else False (i.e Non-Empty)'''

        if self.length() == 0:
            return True

        return False

    def is_exists(self, value):
        '''Returns True if the given value is in list else return False'''

        if value in self.stack:
            return True

        return False

    def get_index(self, value):
        '''Returns the index of the given value.

          If the given value is repeated then list of the indexes of that value is returned

          Raises ValueError: "value" is not in stack      -> if the given value does not exists in the list'''

        if self.is_exists(value):
            index = []
            count = 0

            for val in self.stack:
                if val == value:
                    index.append(count)

                count += 1

            if count == 1:
                return index[0]

            return index

        raise ValueError(f'{value} is not in stack')
