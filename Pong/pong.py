import statistics
import tkinter as tk
import random
import time
import math
import random

class Ball:
    def __init__(self, pos_x, pos_y, xspeed, yspeed, radius, tk_id, collide_lines):
        self.collide_lines = collide_lines
        self.id = tk_id
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius

        #self.top_y = pos_y - radius
        #self.bottom_y = pos_y + radius
        #self.left_x = pos_x - radius
        #self.right_x = pos_x + radius

        self.is_bouncing = False

        self.draw()

    def update(self):
        if self.is_beyond(left_wall):
            return "Right player"
        elif self.is_beyond(right_wall):
            return "Left player"

        self.pos_x += self.xspeed
        self.pos_y += self.yspeed
        #self.top_y += self.yspeed
        #self.bottom_y += self.yspeed
        #self.left_x += self.xspeed
        #self.right_x += self.xspeed

        # Check if there's going to be a collision
        tried_bouncing = False
        for line in self.collide_lines:
            if self.is_beyond(line):
                tried_bouncing = True
                # Only bounce if it's not already started bouncing
                if not self.is_bouncing:
                    self.bounce(line)
                    break
        if not tried_bouncing:
            self.is_bouncing = False

        self.draw()

    def bounce(self, line):
        if line.is_horiz:
            self.yspeed *= -1
        else:
            self.xspeed *= -1
        self.is_bouncing = True

    def draw(self):
        canvas.move(self.id, self.xspeed, self.yspeed)

    def is_beyond(self, line):
        """
        Whether it's touching or gone beyond a wall or paddle
        """
        return line.distance_to_ball(self) < self.radius and line.within_bounds(self)
    
    def left(self):
        return self.pos_x - self.radius

    def right(self):
        return self.pos_x + self.radius
        
    def top(self):
        return self.pos_y - self.radius

    def bottom(self):
        return self.pos_y + self.radius


class StraightLine:
    """
    A horizontal or vertical line that isn't seen
    """

    def __init__(
        self, start_x, start_y, end_x, end_y, position, name="", is_wall=False
    ):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.name = name
        self.position = position
        self.is_wall = is_wall
        self.is_horiz = self.position == "top" or self.position == "bottom"

    def update(self):
        self.start += self.speed
        self.end += self.speed

    def within_bounds(self, ball):
        if self.is_wall:
            return True

        if self.is_horiz:
            return (
                self.start_x <= ball.left() <= self.end_x
                or self.start_x <= ball.right() <= self.end_x
            )
        else:
            return (
                self.start_y <= ball.top() <= self.end_y
                or self.start_y <= ball.bottom() <= self.end_y
            )

    def distance_to_ball(self, ball):
        """
        Returns the distance to the given ball
        """
        if self.is_horiz:
            return abs(self.start_y - ball.pos_y)
        else:
            return abs(self.start_x - ball.pos_x)


class Paddle:
    def __init__(
        self, height, width, color, pos_x, pos_y, is_on_left, change, name="A paddle"
    ):
        self.height = height
        self.width = width
        self.pos_y = pos_y
        self.name = name
        self.change = change
        self.is_on_left = is_on_left

        if is_on_left:
            left_x = 0
            top_y = pos_y - height / 2
            right_x = width
            bottom_y = top_y + height
        else:
            left_x = canvas_width - width#pos_x - width / 2
            top_y = pos_y - height / 2
            right_x = canvas_width#left_x + width
            bottom_y = top_y + height

        if is_on_left:
            main_edge = StraightLine(right_x, top_y, right_x, bottom_y, "right", name=f"r{name}")
        else:
            main_edge = StraightLine(left_x, top_y, left_x, bottom_y, "left", name=f"l{name}")

        self.edges = [
            main_edge,
            StraightLine(left_x, top_y, right_x, top_y, "bottom"),
            StraightLine(left_x, bottom_y, right_x, bottom_y, "top"),
        ]

        self.id = canvas.create_rectangle(left_x, top_y, right_x, bottom_y, fill=color)

    def move(self, movement):
        # Redraw the paddle
        canvas.move(self.id, 0, movement)

        # Update the position
        self.pos_y += movement

        # Update the positions of the lines
        for edge in self.edges:
            edge.start_y += movement
            edge.end_y += movement

    def move_up(self, evt):
        if self.pos_y - self.height / 2 >= 0:
            self.move(-self.change)

    def move_down(self, evt):
        if self.pos_y + self.height / 2 <= canvas_height:
            self.move(self.change)


canvas_width = 700
canvas_height = 650

x_center = canvas_width / 2
y_center = canvas_height / 2

# root will be the window to put everything in
root = tk.Tk()
# Set the title
root.title("Pong")
# The canvas is where everything will be drawn
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bd=0, bg="black",)
# Adds the canvas to the window
canvas.pack()

# The text for the countdown
label_text = tk.StringVar()
label = tk.Label(
    root,
    anchor=tk.CENTER,
    textvariable=label_text,
    bg="black",
    fg="white",
    font=("Courier", 30),
)
# Adds the label to the window
label.pack()
label.place(x=x_center, y=y_center, anchor="center")

# Countdown loop. Goes from 3 to 1
for t in range(3, 1, -1):
    label_text.set(str(t))
    root.update()
    time.sleep(1)

label_text.set("GO!")
root.update()
time.sleep(1)
#label_text.set("")
label.pack_forget()
root.update()

top_wall = StraightLine(
    0, 0, canvas_width, 0, position="top", name="Top wall", is_wall=True,
)
bottom_wall = StraightLine(
    0,
    canvas_height,
    canvas_width,
    canvas_height,
    position="bottom",
    name="Bottom wall",
    is_wall=True,
)
left_wall = StraightLine(
    0, 0, 0, canvas_height, position="left", name="Left wall", is_wall=True,
)
right_wall = StraightLine(
    canvas_width,
    0,
    canvas_width,
    canvas_height,
    position="right",
    name="Right wall",
    is_wall=True,
)

paddle_height = 200
paddle_width = 50
# How much the paddles move when the keys are pressed
paddle_movement = 15

left_paddle = Paddle(
    height=paddle_height,
    width=paddle_width,
    color="blue",
    is_on_left=True,
    pos_x=paddle_width / 2,
    pos_y=y_center,
    change=paddle_movement,
    name="Left paddle",
)
right_paddle = Paddle(
    height=paddle_height,
    width=paddle_width,
    color="red",
    is_on_left=False,
    pos_x=canvas_width - paddle_width / 2,
    pos_y=y_center,
    change=paddle_movement,
    name="Right paddle",
)

# The keys 'w' and 's' make the left paddle move up and down
w_bind_id = root.bind("w", left_paddle.move_up)
s_bind_id = root.bind("s", left_paddle.move_down)

# The up and down arrow keys make the left paddle move up and down
up_bind_id = root.bind("<KeyPress-Up>", right_paddle.move_up)
down_bind_id = root.bind("<KeyPress-Down>", right_paddle.move_down)

# To randomly choose a speed for the ball
speed_min = 0.02
speed_max = 0.09

ball_radius = 50

ball_id = canvas.create_oval(
    x_center - ball_radius,
    y_center - ball_radius,
    x_center + ball_radius,
    y_center + ball_radius,
    fill="yellow",
)

ball = Ball(
    tk_id=ball_id,
    radius=ball_radius,
    pos_x=x_center,
    pos_y=y_center,
    collide_lines=[top_wall, bottom_wall, left_wall, right_wall]
    + left_paddle.edges
    + right_paddle.edges,
    xspeed=random.uniform(speed_min, speed_max),
    yspeed=random.uniform(speed_min, speed_max),
)

test = canvas.create_rectangle(
    0, 0, 50, 200, fill="yellow"
)
canvas.move(test, 0, 0)

won = False

# Loop to actually run the game
while not won:
    won = ball.update()
    root.update_idletasks()
    root.update()

label.pack()
label.place(x=x_center, y=y_center, anchor="center")
label_text.set(f"{won} has won!")

# stop them from moving afterwards
root.unbind("w", w_bind_id)
root.unbind("s", s_bind_id)
root.unbind("<KeyPress-Up>", up_bind_id)
root.unbind("<KeyPress-Down>", down_bind_id)

root.update()

tk.mainloop()
