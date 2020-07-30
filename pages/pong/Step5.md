---
layout: default
description: Polishing the game and adding finishing touches
---

Most of the logic for the game has already been implemented, but in this step, we're going to make it more user-friendly and give it a little more functionality.

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

This way, while there is no winner, i.e., the value of `winner` is `None`, the game will keep going. When `winner` contains some value, it'll stop, and we can announce whoever won. For now, let's just use a simple `print(winner)` after the loop.

---

The source code for this part is [here](https://github.com/ysthakur/arts-n-stem/blob/master/Pong/Step5_FinishingTouches.py).