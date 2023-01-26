'''
Draw olympics flag
'''


import turtle

tut = turtle.Turtle()
tut.shape('turtle')
tut.pensize(5)

tut.right(180)
tut.penup()
tut.forward(230)
tut.right(90)
tut.forward(100)
tut.pendown()

# First Circle
tut.color('blue')
tut.circle(50)
tut.left(90)
tut.penup()

# Second Circle
tut.forward(30)
tut.left(90)
tut.forward(20)
tut.pendown()
tut.color('yellow')
tut.right(40)
tut.circle(50)

# Third Circle
tut.color('black')
tut.penup()
tut.left(110)
tut.forward(90)
tut.pendown()
tut.circle(50)

# Fourth Circle
tut.color('green')
tut.penup()
tut.right(33)
tut.forward(50)
tut.pendown()
tut.circle(50)

# Fifth Circle
tut.penup()
tut.left(63)
tut.forward(120)
tut.pendown()
tut.color('red')
tut.circle(50)

# Writing on the screen
tut.right(160)
tut.penup()
tut.forward(300)
tut.left(150)
tut.pendown()
tut.color('black')
tut.write('Olympic Flag', font=("Arial", 50, 'normal'))
