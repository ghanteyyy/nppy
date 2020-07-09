from stack_ds import Stack

stack = Stack()
pairs = {'(': ')', '{': '}', '[': ']'}
test = '(((((((((())))))))))'

def valid_paren():
	for t in test:
		if t in pairs:
			stack.push(t)
			
		else:
			if not pairs[stack.pop()] == t:
				return False
	
	if not stack.is_empty():
		return False
				
	return True
	

print(valid_paren())