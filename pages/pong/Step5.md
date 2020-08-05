---
layout: step
title: Polishing the game and adding finishing touches
---

Most of the logic for the game has already been implemented, but in this step, we're going to make it more user-friendly and fix a glitch or two.

## Ending the game

Currently, if the ball touches the left or right walls, it just keeps going and the game doesn't end. To fix that, we need to constantly check if the ball has touched those walls in the `while` loop inside which the entire game runs. Let's create a `find_winner` function so that if the game has ended, it returns the winner.

```python
def find_winner(self):
    if ball.should_bounce(left_wall):
        return "Right" # If it's touching the left wall, the right player has won
    elif ball.should_bounce(right_wall):
        return "Left" # If it's touching the right  wall, the left player has won
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

<video width="100%" autoplay controls>
  <source src="https://github.com/ysthakur/arts-n-stem/blob/gh-pages/images/pong/GlitchyBounce.mp4?raw=true" type="video/mp4">
</video>

This is happening because the ball starts bouncing off the paddle, but hasn't completely cleared it when it's once again updated, causing it to reverse its direction yet again. How about we also check in our `should_bounce` if we're touching a line but also moving away from it already?

```python
# The ball is touching the paddle
if line.within_bounds(self) and line.distance_to_ball(self) <= self.radius:
    # The paddle is on the right and the ball is moving right
    if line.position == "right" and self.xspeed > 0:
        return True
    # The paddle is on the left and the ball is moving left
    elif line.position == "left" and self.xspeed < 0:
        return True
    # The paddle is on the top and the ball is moving up
    elif line.position == "top" and self.yspeed < 0:
        return True
    # The paddle is on the bottom and the ball is moving down
    elif line.position == "bottom" and self.yspeed > 0:
        return True

# Otherwise, return false
return False
```

That could be shortened into a one-liner.

```python
def should_bounce(self, line):
    """
    Whether or not it should bounce off the given line
    """
    return (
        line.within_bounds(self) and line.distance_to_ball(self) <= self.radius
        and (
            # The paddle is on the right and the ball is moving right
            line.position == "right" and self.xspeed > 0 or
            # The paddle is on the left and the ball is moving left
            line.position == "left" and self.xspeed < 0 or
            # The paddle is on the top and the ball is moving up
            line.position == "top" and self.yspeed < 0 or
            # The paddle is on the bottom and the ball is moving down
            line.position == "bottom" and self.yspeed > 0
        )
    )
```

The glitch should be gone now, and you'll be able to move your paddles while the ball is touching them. Moving on...

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

## Creating a countdown

Don't you hate it when a game starts before you're ready? It'd be nice to have a countdown of, say, 3 seconds, so that when the ball does start moving, both players are prepared. Remember the "Hello World" label we created in [Step 1](Step1)? We're going to use that again, but this time, instead of displaying "Hello world", we'll make it count down from 3 to 1, and then display "GO!" before the game starts. Put the following code somewhere before the the ball and the paddles are drawn.

```python
label_text = tk.StringVar()
label = tk.Label(
    root,
    textvariable=label_text,
    bg="black",
    fg="white",
    font=("Courier", 30),
)
label.place_configure(x=350, y=325, anchor="center")
```

This will create a label with no text inside. To change what's displayed, we use the `label_text.set` function. Next, use a loop with a counter that goes from 3 to 1. `range(3, 0, -1)` creates a range from 3 to 0 (not including 0), decreasing by -1 each time.

```python
for s in range(3, 0, -1):
    label_text.set(s)
    # Don't forget to update the canvas!
    root.update()
    # Wait a second before the next number
    time.sleep(1)

label_text.set("GO!")
root.update()
```

Now you'll have a countdown before the ball starts moving, but the label remains right there even after the game has begun, which is annoying. We could make the text that the label contains empty by using `label_text.set("")`, but that just results in this:

![Empty label](https://github.com/ysthakur/arts-n-stem/blob/gh-pages/images/pong/EmptyLabel.png?raw=true)

Luckily, Tkinter has a `place_forget` function that will make the canvas forget about our label until we add it back using `label.place` again. Just add this right after the part where the text is set to "GO!" and the label will disappear when the window is updated.

```python
time.sleep(1)
label.place_forget()
```

## Announcing the winner

It doesn't seem right to simply print "Left" or "Right" in the console when the program ends. You can't see it in the window where the game itself is running, which is a bit confusing. To fix that, simply set the text of the label to whoever the winner is, and then (this is very important) add the label back using `label.place_configure` again. If you don't use the `place_configure` function again, the label will remain "forgotten".

```python
label_text.set(winner + " player wins!")
label.place_configure(x=x_center,y=y_center,anchor="center")
```

Congratulations, you've just finished making a two-player pong game!

## Further improvements

As awesome as the game we've made is, it's still pretty basic. There are a lot of things you can do on your own to make it nicer, including

* Moving functions from one class to another, changing the flow of the program, etc.
* Adding sound effects
* Changing the layout, colors, etc. and making the game look better
* Letting users play multiple rounds and displaying the score at the top
* Making a single-player version where the computer plays against a human player

---

The source code for this part is [here](https://github.com/ysthakur/arts-n-stem/blob/gh-pages/Pong/Step5_FinishingTouches.py).
