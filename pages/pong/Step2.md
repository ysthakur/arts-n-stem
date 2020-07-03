---
layout: page
title: Creating classes to represent objects
---

In this step, we're going to create a few classes to represent the paddles, the ball, the walls, and positions.

## The `Point` class

```python
class Point:
    
``` 

## The `Paddle` class

Let's start with this rudimentary implementation of a class for paddles. Later on, we'll add more to it.

```python
class Paddle:
    def __init__(self, height, width, pos, color):
        self.height = height
        self.width = width

        left_x = pos.x - width / 2
        top_y = pos.y - height / 2
        right_x = left_x + width
        bottom_y = top_y + height

        self.id = canvas.create_rectangle(left_x, top_y, right_x, bottom_y, fill=color)
```

Every paddle knows its height, width, and the position of its center is (`pos`). This makes it easier to manipulate it later on. We could also have stored the height and width of every paddle in global variables, so that every paddle would only have had to know its position, but global variables are generally considered bad practice.

You might be wondering what `pos` is, but let's not worry about that right now. For now, all you need to know is that `pos` represents where the center of the rectangle, and has 2 fields, `x` and `y`, which represent its coordinates.

The coordinates of the paddle are calculated the same way the coordinates for the rectangle around the [ball](https://github.com/ysthakur/arts-n-stem/blob/master/pages/pong/Step1.md#drawing-the-ball) were calculated. Since `pos.x`, the x-coordinate of `pos`, is right between `left_x`, the left side of the paddle, and `right_x`, the right side of the paddle, and the distance between `left_x` and `right_x` is `width`. Therefore, we know that the left and right sides of the paddle are `width / 2` units away from `pos.x`, from which we can calculate `left_x` and `right_x`. You can apply the same logic for `top_y` and `bottom_y`.


