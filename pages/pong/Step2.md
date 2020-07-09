---
layout: page
title: Creating classes to represent objects
---

In this step, we're going to create a few classes to represent the paddles, the ball, the walls, and positions.

## The `Paddle` class

Let's start with this rudimentary implementation of a class for paddles. Later on, we'll add more to it.

```python
class Paddle:
    def __init__(self, height, width, pos_x, pos_y, color):
        self.height = height
        self.width = width
        self.pos_x = pos_x
        self.pos_y = pos_y

        left_x = pos_x - width / 2
        top_y = pos_y - height / 2
        right_x = left_x + width
        bottom_y = top_y + height

        self.id = canvas.create_rectangle(left_x, top_y, right_x, bottom_y, fill=color)
```

Every paddle knows its height, width, and the coordinates of its center (`pos_x` and `pos_y`). This makes it easier to manipulate it later on. We could also have stored the height and width of every paddle in global variables, so that every paddle would only have had to know its position, but global variables are generally considered bad practice.

The coordinates of the paddle are calculated the same way the coordinates for the rectangle around the [ball](https://github.com/ysthakur/arts-n-stem/blob/master/pages/pong/Step1.md#drawing-the-ball) were calculated. Since `pos_x`, the x-coordinate of the center, is right between `left_x`, the left side of the paddle, and `right_x`, the right side of the paddle, and the distance between `left_x` and `right_x` is `width`. Therefore, we know that the left and right sides of the paddle are `width / 2` units away from `pos_x`, from which we can calculate `left_x` and `right_x`. You can apply the same logic for `top_y` and `bottom_y`.

This is how we can create both our paddles. 

```python
paddle_height = 200
paddle_width = 50

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
