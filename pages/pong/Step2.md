---
layout: default
title: Classes to represent objects
---

In this rather short step, we're going to create a couple classes to represent the paddles and the ball.

## The `Paddle` class

Let's start with this rudimentary implementation of a class for paddles. Later on, we'll add more to it.

```python
class Paddle:
    def __init__(self, height, width, pos_x, pos_y, color):
        self.height = height
        self.width = width
        self.pos_y = pos_y

        left_x = pos_x - width / 2
        top_y = pos_y - height / 2
        right_x = pos_x + width / 2 # OR left_x + width
        bottom_y = pos_x + width / 2 # OR top_y + height

        self.id = canvas.create_rectangle(left_x, top_y, right_x, bottom_y, fill=color)
```

Every paddle knows its height, width, and the y-coordinate of its center (`pos_y`). This makes it easier to manipulate it later on. We could also have stored the height and width of every paddle in global variables, so that every paddle would only have had to know its position, but global variables are generally considered bad practice.

The coordinates of the paddle are calculated the same way the coordinates for the rectangle around the [ball](https://github.com/ysthakur/arts-n-stem/blob/gh-pages/pages/pong/Step1.md#drawing-the-ball) were calculated. Since `pos_x`, the x-coordinate of the center, it's right between `left_x`, the left side of the paddle, and `right_x`, the right side of the paddle, and the distance between `left_x` and `right_x` is `width`. Therefore, we know that the left and right sides of the paddle are `width / 2` units away from `pos_x`, from which we can calculate `left_x` and `right_x`. You can apply the same logic for `top_y` and `bottom_y`.

This is how we can create both our paddles.

```python
paddle_height = 200
paddle_width = 30

left_paddle = Paddle(
    height=paddle_height,
    width=paddle_width,
    pos_x=paddle_width / 2,
    pos_y=y_center,
    color="blue",
)
right_paddle = Paddle(
    height=paddle_height,
    width=paddle_width,
    pos_x=canvas_width - paddle_width / 2,
    pos_y=y_center,
    color="red",
)
```

## The `Ball` class

We also need to create a class to represent the ball. Each ball should know the position of its center, its speed (in both the x and y directions), and its radius. It will also need to keep track of the yellow circle that represents the ball on the canvas (hence `self.id`).

```python
class Ball:
    def __init__(self, pos_x, pos_y, radius, color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius

        self.id = canvas.create_oval(
            pos_x - radius,
            pos_y - radius,
            pos_x + radius,
            pos_y + radius,
            fill=color,
        )
```

This constructor is pretty straightforward. It sets instance variables for the position, speed, and radius of the ball, and then creates a circle on the screen. That last part is almost the same as the code we had previously, but `x_center`, `y_center`, and `ball_radius` are substituted with `pos_x`, `pos_y`, and `radius`, respectively, and `color` is used instead of directly using `"yellow"` (so that we can easily change the ball's color later).

```python
ball_id = canvas.create_oval(
    x_center - ball_radius,
    y_center - ball_radius,
    x_center + ball_radius,
    y_center + ball_radius,
    fill="yellow",
)
```

## Instantiating `Ball` and `Paddle`

You can now replace the code you previously had for creating the two rectangles representing paddles with calls to the `Paddle` constructor. It's a lot clearer than what we had before.

```python
left_paddle = Paddle(
    height=paddle_height,
    width=paddle_width,
    pos_x=paddle_width / 2,
    pos_y=y_center,
    color="blue",
)
right_paddle = Paddle(
    height=paddle_height,
    width=paddle_width,
    pos_x=canvas_width - paddle_width / 2,
    pos_y=y_center,
    color="red",
)
```

The ball can be created like this:

```python
ball = Ball(
    pos_x=x_center,
    pos_y=y_center,
    radius=ball_radius,
    color="yellow"
)
```

Before you run this part, though, I would suggest commenting out the code to create the label, since it only blocks our view of the ball and we're not going to need it for a while.

---

<a href="https://ysthakur.github.io/arts-n-stem/pages/pong/Step3" class="button">Next step: Moving the ball and paddles</a>

---

The source code for this part is [here](https://github.com/ysthakur/arts-n-stem/blob/gh-pages/Pong/Step2_Classes.py).
