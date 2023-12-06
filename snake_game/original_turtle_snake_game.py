import turtle
import math
import random
import time

segments = []
score = 0
high_score = 0
delay = 0.01

colors = ['forestgreen','limegreen','darkgreen', 'green','springgreen','greenyellow','lawngreen', 'palegreen','seagreen']
n_color = len(colors)
c = 0

wn = turtle.Screen()
wn.title('Snake Game')
wn.bgcolor('black')
wn.setup(width=600, height=600)

head = turtle.Turtle()
head.speed(1)
head.shape('square')
head.color('white')
head.penup()
head.goto(0, 0)
head.direction = 'right'

# Snake food: Apple 
food = turtle.Turtle()
wn.register_shape('apple.gif')
food.shape('apple.gif')
food.penup()
food.goto(0, 100)

# Scoring text 
pen = turtle.Turtle()
pen.color('green')
pen.penup()
pen.hideturtle()
pen.goto(0,260)
pen.write('Score 0 High Score 0', align='center', font=24)


def go_up():
    if head.direction != 'down':
        print("Go up")
        head.direction = 'up'

def go_down():
    if head.direction != 'up':
        print("Go down")
        head.direction = 'down'

def go_right():
    if head.direction != 'left':
        print("Go right")
        head.direction = 'right'

def go_left():
    if head.direction != 'right':
        print("Go left")
        head.direction = 'left'

wn.listen()
wn.onkeypress(go_up, 'w')
wn.onkeypress(go_down, 's')
wn.onkeypress(go_right, 'd')
wn.onkeypress(go_left, 'a')

def distance(t1, t2):
    t1_x = head.xcor()
    t1_y = head.ycor()

    t2_x = food.xcor()
    t2_y = food.ycor()

    dist = math.sqrt((t1_x-t2_x)*(t1_x-t2_x) + (t1_y-t2_y)*(t1_y-t2_y))
    return dist

def move(): 
    if head.direction == 'up':
          y = head.ycor()
          head.sety(y + 10)

    if head.direction == 'down':
         y = head.ycor()
         head.sety(y - 10)

    if head.direction == 'right':
          x = head.xcor()
          head.setx(x + 10)

    if head.direction == 'left':
          x = head.xcor()
          head.setx(x - 10) 

while True:

    wn.update()
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
          time.sleep(1)
          head.goto(0, 0)
          head.direction = 'stop'
          for segment in segments:
            segment.goto(1000, 1000)
          segments.clear()
          score = 0
          pen.clear()
          pen.write('Score: {} High Score: {}'.format(score, high_score), align='center', font=24)

    #1) What's the last thing that is missing to this game? It looks like we have everything down, but what if we have a very looong snake. What would be the wrong move? We don't want to have tail to collide into itself. What have we been using to go through all of the segments? 
    #2) We have been using a for loop to go through each of the segments of the tail. Lets create a for loop like so: 
    for segment in segments:
        if segment.distance(head) < 2:
            time.sleep(1)
            head.goto(0,0)
            head.direction = 'stop'
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()
            score = 0
            pen.clear()
            pen.write('Score: {} High Score: {}'.format(score, high_score), align='center', font=24)

      #We can get the distance between a segment of the tail from the head of the snake. We can use the same unit as the other distance check. Turtle has a built in one for this case: 
          #We set all of the defaults as we have done in the past before! We do this with the following lines. Do these lines look familar? 
      # Now lets run it! Congratulations, we have finished the snake game! 
      # Maybe we want to do some customizations......

    if distance(head, food) < 20:
        x = random.randint(-290,290)
        y = random.randint(-290,290)
        
        food.goto(x,y)
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape('square')
        new_segment.color(colors[c])
        c = c + 1
        if c == n_color:
          c = 0
        new_segment.penup()
        segments.append(new_segment)

        score = score + 1
        if score > high_score:
            high_score = score 
        pen.clear()
        pen.write('Score: {} High Score: {}'.format(score, high_score), align='center', font=24)

    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()     
    time.sleep(delay)


wn.mainloop()
