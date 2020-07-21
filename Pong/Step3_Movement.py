import tkinter as tk

import time


class Paddle:
    def __init__(self, height, width, pos_x, pos_y, color, change):
        self.height = height
        self.width = width
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.change = change

        left_x = pos_x - width / 2
        top_y = pos_y - height / 2
        right_x = left_x + width
        bottom_y = top_y + height

        self.id = canvas.create_rectangle(left_x, top_y, right_x, bottom_y, fill=color)

    def move_up(self, event):
        canvas.move(self.id, 0, -self.change)

    def move_down(self, event):
        canvas.move(self.id, 0, self.change)


class Ball:
    def __init__(self, pos_x, pos_y, radius, xspeed, yspeed, bounce_lines):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.bounce_lines = bounce_lines

        self.id = canvas.create_oval(
            pos_x - radius,
            pos_y - radius,
            pos_x + radius,
            pos_y + radius,
            fill="yellow",
        )

    def update(self):
        self.pos_x += self.xspeed
        self.pos_y += self.yspeed

        canvas.move(self.id, self.xspeed, self.yspeed)

        for line in self.bounce_lines:
            if self.should_bounce(line):
                self.bounce(line)
                break
    
    def should_bounce(self, line):
        """
        Whether or not it should bounce off the given line
        """
        return line.distance_to_ball(self) <= self.radius

    def bounce(self, line):
        """
        Bounce off the given line
        """
        if line.is_horiz:
            self.yspeed *= -1
        else:
            self.xspeed *= -1


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

        self.is_horiz = self.position == "top" or self.position == "bottom"

    def distance_to_ball(self, ball):
        """
        Returns the distance to the given ball
        """
        if self.is_horiz:
            return abs(self.start_y - ball.pos_y)
        else:
            return abs(self.start_x - ball.pos_x)


# root will be the window to put everything in
root = tk.Tk()
# Set the title
root.title("Pong")

canvas_width = 700
canvas_height = 650

x_center = canvas_width / 2
y_center = canvas_height / 2

# The canvas is where everything will be drawn
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="black",)
# Adds the canvas to the window
canvas.pack()

# The code for the label is not necessary yet

top_wall = StraightLine(0, 0, canvas_width, 0, position="top", is_wall=True,)
bottom_wall = StraightLine(
    0, canvas_height, canvas_width, canvas_height, position="bottom", is_wall=True,
)
left_wall = StraightLine(0, 0, 0, canvas_height, position="left", is_wall=True,)
right_wall = StraightLine(
    canvas_width, 0, canvas_width, canvas_height, position="right", is_wall=True,
)

paddle_height = 200
paddle_width = 50
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

ball_radius = 50

ball = Ball(
    pos_x=x_center,
    pos_y=y_center,
    radius=ball_radius,
    xspeed=1,
    yspeed=2,
    bounce_lines=[left_wall, top_wall, right_wall, bottom_wall],
)

# The keys 'w' and 's' make the left paddle move up and down
w_bind_id = root.bind("w", left_paddle.move_up)
s_bind_id = root.bind("s", left_paddle.move_down)

# The up and down arrow keys make the left paddle move up and down
up_bind_id = root.bind("<KeyPress-Up>", right_paddle.move_up)
down_bind_id = root.bind("<KeyPress-Down>", right_paddle.move_down)

root.update()

while True:
    ball.update()
    root.update()
    time.sleep(0.01)

root.update()

tk.mainloop()
