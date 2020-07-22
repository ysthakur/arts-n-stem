---
layout: default
title: Classes to represent objects
---

## Moving the paddles

Finally, we're going to get around to moving the paddles. To move them, you can use the `canvas.move` function. Add these two functions inside the `Paddle` class.

```python
def move_up(self):
    canvas.move(self.id, 0, -5)

def move_down(self):
    canvas.move(self.id, 0, 5)
```

The `move` function takes the widget that has to be moved (`self.id`), the amount it has to be moved in the x-direction (`0` because the paddles aren't moving sideways), and the amount it moves in the y-direction. I'm moving the paddles by 5 units each time, but you can always change that. Try adding a few calls to `move_up` and `move_down` in your code and what happens - how far the paddle moves, how fast it moves, etc.

One can use `root.bind` to **bind** a key to a function, i.e., trigger a function when a certain key is pressed. The first argument of `bind` is the triggering event (a key in this case), and the second is the function to be triggered. When the key "w" is pressed, the left paddle should move up; when "s" is pressed, it should move down; when the up arrow is pressed, the right paddle should move up; and when the down arrow is pressed, it should move down.

```python
# The keys 'w' and 's' make the left paddle move up and down
w_bind_id = root.bind("w", left_paddle.move_up)
s_bind_id = root.bind("s", left_paddle.move_down)

# The up and down arrow keys make the left paddle move up and down
up_bind_id = root.bind("<KeyPress-Up>", right_paddle.move_up)
down_bind_id = root.bind("<KeyPress-Down>", right_paddle.move_down)
```

Add the above code to your program, run it, and try moving the paddles by pressing "w", "s", up, and down. You'll see that there's an error saying that `move_up` or `move_down` "takes 1 positional argument but 2 were given." Why is this? It's because Tkinter also wants to give your function an object that contains information about the event that happened (for more information, see [here](https://effbot.org/tkinterbook/tkinter-events-and-bindings.html)). We'll have to modify our `move_up` and `move_down` functions like this (there's no need to use `event`):

```python
def move_up(self, event):
    canvas.move(self.id, 0, -5)

def move_down(self, event):
    canvas.move(self.id, 0, 5)
```

*Now* try moving the paddles up and down. It should work properly now. However, you might find that they move a little too slowly. To find the right value, we'll have to experiment a little by increasing and decreasing the speed of the paddle. But say you want to make the paddle go faster (30 units every keypress instead of 5). You'll have to change the value in `move_up` to -30 and the one in `move_down` to 30, and you'll have to change both numbers every single time you want to tweak the paddle's movement even a little bit. So instead of hardcoding that value, let's have an instance variable called `change` that tells us how much the paddle moves.

Add a `change` parameter in your constructor (what position you put it in is a matter of preference), and use that to set `self.change`:

```python
def __init__(self, height, width, pos_x, pos_y, color, change):
    ...
    self.change = change
    ... # The rest of your code
```

Then use `self.change` in `move_up` and `move_down`:

```python
def move_up(self, event):
    canvas.move(self.id, 0, -self.change)

def move_down(self, event):
    canvas.move(self.id, 0, self.change)
```

You'll also have to give an argument for `change` when you create your paddles. Like we did with `height` and `width` before, we can create a single variable (`paddle_movement`) and use that for both paddles.

```python
paddle_movement = 15

left_paddle = Paddle(
    height=paddle_height,
    width=paddle_width,
    pos_x=paddle_width / 2,
    pos_y=y_center,
    color="blue",
    change=paddle_movement,
)
right_paddle = Paddle(
    height=paddle_height,
    width=paddle_width,
    pos_x=canvas_width - paddle_width / 2,
    pos_y=y_center,
    color="red",
    change=paddle_movement,
)
```

## Making the ball move

For now, let's just make the ball move without making it bounce. First, the ball needs to have `xspeed` and `yspeed` attributes to know how much it should move. Add them as parameters to the constructor.

```python
def __init__(self, pos_x, pos_y, radius, xspeed, yspeed):
    ...
    self.xspeed = xspeed
    self.yspeed = yspeed
    ... # The rest of your code
```

The ball should also have an `update` function that moves the ball and is called continuously. The below code is pretty straightforward: it updates `pos_x` and `pos_y` and then actually redraws the ball on the screen. Remember that the `move` function expects the speed of the object and not the position where you want it to go.

```python
def update(self, line):
    self.pos_x += self.xspeed
    self.pos_y += self.yspeed

    canvas.move(self.id, self.xspeed, self.yspeed)
```

Let's change the creation of the ball now. We'll have to give it arguments for `xspeed` and `yspeed`, but there's no need to create variables for it like we did for the paddles' height and width because the `Ball` constructor is only being called once. Later on, we'll choose the speeds randomly.

```python
# You can set xspeed and yspeed to whatever you like
ball = Ball(pos_x=x_center, pos_y=y_center, radius=ball_radius, xspeed=1, yspeed=2)
```

After this, we make a `while` loop to continuously move the ball. Right now, it's going to be an infinite loop, but later on, it'll end when someone wins the game. Make sure this while loop is *after* you bind the keys, because you won't be able to move the paddles during the while loop otherwise. Also make sure that you call `root.update()` every time you update the ball, because you won't see it move otherwise.

```python
while True:
    ball.update()
    root.update()
```

Try running the code now. You won't see the ball, because it disappeared almost instantly. We need to delay the ball, and luckily, there's a `time` module for that. Add `import time` at the top of your file, and at the bottom of the while loop, insert `time.sleep(0.5)`, which will make it pause for half a second. Try running again and you'll see that the ball moves in little jumps and eventually goes off screen, because we haven't implemented any bouncing logic.

## Making the ball bounce

Before we write code to actually make the ball bounce, let's think about how a ball bounces. It bounces off of the top wall, the bottom wall, the right edge of the left paddle, and the left edge of the right paddle. When it bounces off of the left paddle, its y speed is unchanged, but it goes right at the same speed it was previously going left at. When it bounces off the top paddle, its x speed is unchanged, but it goes down at the same speed that it was previously going up at. When it bounces off the right paddle, it goes left. You get the idea.

Let's first define a `StraightLine` class to represent things that the ball can bounce off of. Each line must know its endpoints, hence the parameters (and attributes) `start_x`, `start_y`, `end_x`, `end_y`. As you've guessed, these will be floating-point numbers representing x- and y-coordinates. `position` will be a string telling us where the line is. For example, if it's `"left"`, we will know that the line is on the left, meaning that the ball will probably bounce off to the right. As you guessed, `is_wall` is a boolean telling us whether or not the line is a wall. It's not completely necessary, but we can use it to avoid some extra calculations later.

```python
class StraightLine:
    """
    A horizontal or vertical line that isn't seen
    """

    def __init__(self, start_x, start_y, end_x, end_y, position, is_wall):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.position = position
        self.is_wall = is_wall
```

Let's use these to define the walls

```python
top_wall = StraightLine(0, 0, canvas_width, 0, position="top", is_wall=True,)
bottom_wall = StraightLine(
    0, canvas_height, canvas_width, canvas_height, position="bottom", is_wall=True,
)
left_wall = StraightLine(0, 0, 0, canvas_height, position="left", is_wall=True,)
right_wall = StraightLine(
    canvas_width, 0, canvas_width, canvas_height, position="right", is_wall=True,
)
```

Let's pass the ball a list of lines that it can bounce off. We can call this list `bounce_lines`.

```python
def __init__(self, pos_x, pos_y, radius, xspeed, yspeed, bounce_lines):
    ...
    self.bounce_lines = bounce_lines
    ... # The rest of your code
```

You'll have to modify the ball again, and pass in the 4 walls as a list (the ball won't actually bounce off the side walls, but we can remove that later):

```python
ball = Ball(
    pos_x=x_center,
    pos_y=y_center,
    radius=ball_radius,
    xspeed=1,
    yspeed=2,
    bounce_lines=[left_wall, top_wall, right_wall, bottom_wall],
)
```

We need to make 2 new methods in the `Ball` class, `should_bounce`, and `bounce`. Just make stubs for them now - we'll deal with the actual implementation later.

```python
def should_bounce(self, line):
    """
    Whether or not it should bounce off the given line
    """
    pass

def bounce(self, line):
    """
    Bounce off the given line
    """
    pass
```

Now, in the `Ball.update` method, it can check if there's a line that it should bounce off of, and if there is, it should bounce off it. The `break` is there because once it's started bouncing, there's no need to go through the rest of the list to find another line to bounce off.

```python
def update(self, line):
    self.pos_x += self.xspeed
    self.pos_y += self.yspeed

    canvas.move(self.id, self.xspeed, self.yspeed)

    for line in self.bounce_lines:
        if self.should_bounce(line):
            self.bounce(line)
            break
```

### Filling in the function stubs

Now to implement the `bounce` function. As I mentioned earlier, the ball basically reverses its x speed if it bounces off the left or right paddles(or walls), and reverses its y speed if it bounces off the top or bottom walls.

Let's pretend that `Line`s have an attribute `is_horiz` which tells us whether or not they're horizontal. If the line the ball is bouncing off is horizontal (which the top and bottom walls are), we can reverse the ball's `yspeed` attribute by multiplying by `-1`. If the line is vertical, we can multiply `xspeed` by `-1`.

```python
def bounce(self, line):
    if line.is_horiz:
        self.yspeed *= -1
    else:
        self.xspeed *= -1
```

Creating the `is_horiz` attribute is pretty trivial. In the constructor of `StraightLine`, just check the position and set it accordingly.

```python
if self.position == "top" or self.position == "bottom"
    self.is_horiz = True
else:
    self.is_horiz = False

# Or you could use this shorter version:
self.is_horiz = self.position == "top" or self.position == "bottom"
```

The `should_bounce` function is a little more complicated. For now, let's just implement it by checking the distance from the line to the ball. But first, let's decide how the distance is going to be defined. Instead of checking the distance from a certain point on the ball's edge to the walls/paddles, we can use the distance from the center of the ball and check if it's more than the radius. Having done that, we need to define what point on the *wall* we need to use to calculate the distance. Should we use the distance to the ends of the wall (red and lavender), the distance to the center of the wall (green), or the distance to the point on the wall that's right below the ball (blue)?

![Ball distance horizontal](https://github.com/ysthakur/arts-n-stem/blob/master/images/pong/ShouldBounceBasicHoriz.png?raw=true)

The lengths of the red, green, and lavender lines will change if the length of the wall changes, so we can't use them, since the distance between the ball and wall should have nothing to do with the length of the wall. That leaves us the blue line. No matter what the length of the wall, it will always stay the same.

That's all well and good, but how do you actually find the length of this line? Well, it's perpendicular to the wall and it goes straight through the ball's center. That means the x-coordinate of both its endpoints is the same. We don't have to worry about the Pythagorean theorem and whatnot - we can just treat it as a 1D number line and find the difference between the y-coordinates of the line's endpoints, i.e., find the difference between the ball's center's y-coordinate and the wall's y-coordinate (since the wall is horizontal, every point on that line has the same y-coordinate).

We can also use this same formula when the ball is bouncing off the top wall. The only difference is that because this time the wall is higher than the ball, the wall's y-coordinate minus the ball's y-coordinate will be a negative number (remember that the coordinate system is backwards). We can work around this by using the absolute value so as to make them both positive.

Finding the distance to a vertical wall/paddle is very similar - just use the x-coordinates instead of the y-coordinates. Let's make a function in the `StraightLine` class to calculate the distance when the wall/paddle in question is on the top or bottom of the screen, i.e., it is horizontal:

```python
def distance_to_ball(self, ball):
    if self.is_horiz:
        # Note that you could also use self.end_y since they're the same
        return abs(self.start_y - ball.pos_y)
    else:
        # Vertical, so use the x-coordinates instead
        return abs(self.start_x - ball.pos_x)
```

You can now use `distance_to_ball` in the `should_bounce` function above. Since `distance_to_ball` returns the distance to the center of the ball, the radius of the ball is important. If the distance is the same as the radius, it means that the point on the wall is on the edge of the ball (because a circle is basically the set of all points whose distance from the center is the radius). If the distance is more than the radius, it means that the point on the wall is outside the circle of the ball. If the distance is less than the radius, it means that the point is inside the circle. So basically, if the distance is less than or equal to the radius, the ball is touching the wall, meaning it should bounce. Keeping that in mind, one can define `should_bounce` this way:

```python
def should_bounce(self, line):
    if line.distance_to_ball(self) <= self.radius:
        return True
    else:
        return False

# A shorter version

def should_bounce(self, line):
    return line.distance_to_ball(self) <= self.radius
```

When you run it, you should see the ball bouncing off the walls. If it's going too slowly, make the delay in the while loop smaller (I'm using `time.sleep(0.01)`).

<a href="https://github.com/ysthakur/arts-n-stem/blob/master/pages/pong/Step4" class="button">Next step</a>

---

The source code for this part is [here](https://github.com/ysthakur/arts-n-stem/blob/master/Pong/Step3_Movement.py).
