---
layout: default
description: Polishing the game and adding finishing touches
---

Most of the logic for the game has already been implemented, but in this step, we're going to make it more user-friendly and fix a glitch or two.

## Ending the game

Currently, if the ball touches the left or right walls, it just keeps going and the game doesn't end. To fix that, we need to constantly check if the ball has touched those walls in the `while` loop inside which the entire game runs. Let's create a `find_winner` function so that if the game has ended, it returns the winner.

```python
def find_winner(self):
    if ball.should_bounce(left_wall):
        return "right" # If it's touching the left wall, the right player has won
    elif ball.should_bounce(right_wall):
        return "left" # If it's touching the right  wall, the left player has won
```

The nice thing about Python functions is that even if you don't explicitly return anything at the end of a function, `None` is returned (so if the game hasn't ended, the `winner` function will return a `None`). `None` is a special sort of object that's Python's way of representing "nothing" (this is somewhat similar to `null` in other languages). Another nice thing is that `None` is falsey, whereas non-empty strings, such as `"right"` and `"left"` are truthy. This means that we can use the output of `ball.update()` in our while loop to check if the game has ended. Let's refactor our `while` loop to look like this:

```python
winner = None
while not winner:
    winner = find_winner()
    ball.update()
    root.update()
    time.sleep(0.01)
```

This way, as long as no one has won, i.e., the value of `winner` is `None`, the game will keep going. When `winner` contains some value, it'll stop, and we can announce whoever won. For now, let's just use a simple `print(winner)` after the loop.

## Glitchy bouncing

As long as the players don't move their paddles while the ball is bouncing off of them, everything seems fine, but try moving the paddle up or down while the ball is touching it, and you'll see something crazy happen.

<video src="https://github.com/ysthakur/arts-n-stem/blob/master/images/pong/GlitchyBounce.mp4"\>

This is happening because the ball starts bouncing off the paddle, but hasn't completely cleared it when it's once again updated, causing it to reverse its direction yet again. How about we also check in our `should_bounce` if we're touching a line but also moving away from it already?

```python

```

## Stopping the paddles from moving off the screen

Currently, it's possible to keep moving the paddles up and down until they disappear off the screen completely, and it's a little annoying to have to move them back each time. Let's make it so that they don't move at all if they're already at the edge of the screen. In the `move_up` function, we can make sure that the y-position of the paddle in question is not less than 0 (the y-coordinate of the top of the canvas). Likewise, the `move_down` function can be edited to ensure that the paddle's y-position is not more than `canvas_height`, since `canvas_height` is also the y-position of the bottom of the canvas.

```python
def move_up(self, event):
    if self.pos_y > 0:
        canvas.move(self.id, 0, -self.change)

        self.main_edge.start_y -= self.change
        self.main_edge.end_y -= self.change

def move_down(self, event):
    if self.pos_y < canvas_height:
        canvas.move(self.id, 0, self.change)

        self.main_edge.start_y += self.change
        self.main_edge.end_y += self.change
```

The paddle can still go a little beyond the walls (`self.change` units, to be precise), but it stops after that. Try it out yourself to see.

## Announcing the winner



---

The source code for this part is [here](https://github.com/ysthakur/arts-n-stem/blob/master/Pong/Step5_FinishingTouches.py).
