---
layout: page
title: Creating classes to represent objects
---

In this step, we're going to create a few classes to represent the paddles, the ball, the walls, and positions.

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


