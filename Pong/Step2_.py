import tkinter as tk
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])

class Paddle:
    def __init__(self, height, width, pos, color):
        self.height = height
        self.width = width

        left_x = pos.x - width / 2
        top_y = pos.y - height / 2
        right_x = left_x + width
        bottom_y = top_y + height

        self.id = canvas.create_rectangle(left_x, top_y, right_x, bottom_y, fill=color)


# root will be the window to put everything in
root = tk.Tk()
# Set the title
root.title("Pong")


canvas_width = 700
canvas_height = 650

x_center = canvas_width / 2
y_center = canvas_height / 2

# The canvas is where everything will be drawn
canvas = tk.Canvas(
    root,
    width=canvas_width,
    height=canvas_height,
    bg="black",
)
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
    pos=Point(paddle_width / 2, y_center),
    change=paddle_movement,
    name="Left paddle",
)
right_paddle = Paddle(
    height=paddle_height,
    width=paddle_width,
    color="red",
    is_on_left=False,
    pos=Point(canvas_width - paddle_width / 2, y_center),
    change=paddle_movement,
    name="Right paddle",
)

ball_radius = 50

ball_id = canvas.create_oval(
    x_center - ball_radius,
    y_center - ball_radius,
    x_center + ball_radius,
    y_center + ball_radius,
    fill="yellow",
)

root.update()

tk.mainloop()
