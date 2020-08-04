---
layout: step
title: Making the ball bounce off the paddles
---

## Making the ball bounce off the paddles

The ball now bounces off the walls, but it should also bounce off the paddles. For that, there needs to be a `StraightLine` object for each paddle that the ball can bounce off. We can make each paddle create one in the constructor, but the bouncing edge will be on the left side for the right paddle and on the right side for the left paddle, which means that each paddle needs to know which side it's on to create the `StraightLine` representing the edge the ball bounces off.

Add a parameter called `is_on_left` to the `Paddle` constructor. We won't be creating an instance variable called `is_on_left`, but we will need it to create the bouncing edge.

```python
def __init__(self, height, width, pos_x, pos_y, color, change, is_on_left):
    ...
    left_x = pos_x - width / 2
    top_y = pos_y - height / 2
    right_x = left_x + width
    bottom_y = top_y + height

    # main_edge is what the ball will bounce off
    if is_on_left:
        # Ball will bounce off its right side
        self.main_edge = StraightLine(right_x, top_y, right_x, bottom_y, position="left", is_wall=False)
    else:
        # Ball will bounce off its left side
        self.main_edge = StraightLine(left_x, top_y, left_x, bottom_y, position="right", is_wall=False)
    ...
```

Don't forget to add `is_on_left` to the paddle constructors too.

```python
left_paddle = Paddle(
    height=paddle_height,
    width=paddle_width,
    pos_x=paddle_width / 2,
    pos_y=y_center,
    color="blue",
    change=paddle_movement,
    is_on_left=True,
)
right_paddle = Paddle(
    height=paddle_height,
    width=paddle_width,
    pos_x=canvas_width - paddle_width / 2,
    pos_y=y_center,
    color="red",
    change=paddle_movement,
    is_on_left=False,
)
```

Of course, this isn't going to help the ball bounce off the paddles. We also need to modify the ball object to contain the paddles' `main_edge` attributes. I also removed the left and right walls from `bounce_lines` because the ball isn't supposed to bounce off them anyways - the game should end if it reaches the sides.

```python
ball = Ball(
    ...,# Irrelevant arguments
    bounce_lines=[top_wall, bottom_wall, left_paddle.main_edge, right_paddle.main_edge],
)
```

Try running it again. All seems to be going well - except that the ball bounces even when the paddle isn't there!

<p align="center"><video>
<source src=""></source>
</video></p>

## Fixing the `should_bounce` function

Why does this happen? It's because of the way the `distance_to_ball` function works. Here it is again, just to help you remember.

```python
def distance_to_ball(self, ball):
    if self.is_horiz:
        return abs(self.start_y - ball.pos_y)
    else:
        return abs(self.start_x - ball.pos_x)
```

Notice that it only considers the x-coordinate for the paddles, which are not horizontal. For the top and bottom walls, which are horizontal, it only considers the y-coordinates, but that doesn't matter right now. That means if the ball and paddle were like this, it would still consider the distance between them to be 0.

<p align="center"><img src=""></img></p>

I'm too lazy to do all the math to find the distance properly, so instead, let's create another function called `within_bounds` which tells us whether or not a ball is actually somewhere between the paddle's endpoints and not below or above it somewhere. We'll add that function to the `StraightLine` class later, but for now, let's modify the `should_bounce` function to check whether the ball is even within the line's bounds before checking the distance.

```python
def should_bounce(self, line):
    return line.within_bounds(self) and line.distance_to_ball(self) <= self.radius
```

Now for the `within_bounds` method. You remember the `is_wall` attribute all our `StraightLine` objects had? That's going to come in handy now. Since we know the ball is always within bounds of a wall (since the walls are practically infinite, and the ball is never going to go off the screen), we can just return `True` if `is_wall` is `True`:

```python
def within_bounds(self, ball):
    if self.is_wall:
        return True

    # we'll implement this part later
```

Now for the paddles. They're both vertical, so we don't need to check which direction they're in. We just need to make sure the top of the ball is above the bottom of the paddle, and that the bottom of the ball is below the top of the paddle.

```python
def within_bounds(self, ball):
    if self.is_wall:
        return True

    # The y-coordinate of the top of the ball
    ball_top = ball.pos_y - ball.radius
    ball_bottom = ball.pos_y + ball.radius

    return self.end_y <= ball_top <= self.start_y and self.end_y <= ball_bottom <= self.start_y
```

Do you see a mistake here? `self.end_y` is not guaranteed to represent the top of the paddle. What if someone used the bottom as the start and the top as the end of the line? We have to deal with that case too, so let's change the return statement to this:

```python
return (
    self.end_y <= ball_top <= self.start_y and self.end_y <= ball_bottom <= self.start_y
    or self.start_y <= ball_top <= self.end_y and self.start_y <= ball_bottom <= self.end_y
)
```

If you run it again, you'll find it still doesn't work. Time to debug the program! Inside your `within_bounds` function, add a print statement telling you the values of `ball_top`, `ball_bottom`, `self.start_y`, and `self.end_y`. Run it again, but be careful - if you let your program run too long, it might freeze because of the sheer amount of text being printed.

Here's the output I got:
```
ball_top=497.0, ball_bottom=597.0, line_start=225.0, line_end=425.0
ball_top=499.0, ball_bottom=599.0, line_start=225.0, line_end=425.0
ball_top=499.0, ball_bottom=599.0, line_start=225.0, line_end=425.0
```
I'll spare you the rest of it, but if you did it yourself, you would have noticed that both the paddles' `start_y` and `end_y` didn't change a bit, even though they were moving. This is because in the `move_up` and `move_down` functions, we never changed the paddles' edges' coordinates! Let's do that now.

```python
def move_up(self, event):
    canvas.move(self.id, 0, -self.change)

    self.pos_y -= self.change
    self.main_edge.start_y -= self.change
    self.main_edge.end_y -= self.change

def move_down(self, event):
    canvas.move(self.id, 0, self.change)

    self.pos_y += self.change
    self.main_edge.start_y += self.change
    self.main_edge.end_y += self.change
```

Let's try running it again (be sure to remove the `print` statement(s) you used to debug the `within_bounds` function).

It's not so bad this time, except the ball goes off the screen when it hits the left or right walls. We want the game to stop and the winner to be announced when it does, but that can be easily fixed.

---

<a href="https://ysthakur.github.io/arts-n-stem/pages/pong/Step5" class="button">Next step: Putting some finishing touches</a>

---

The source code for this part is [here](https://github.com/ysthakur/arts-n-stem/blob/gh-pages/Pong/Step4_BounceOffPaddle.py).
