import tkinter as tk

class Paddle:
    def __init__(self, height, width, pos_x, pos_y, color):
        self.height = height
        self.width = width
        self.pos_y = pos_y

        left_x = pos_x - width / 2
        top_y = pos_y - height / 2
        right_x = left_x + width
        bottom_y = top_y + height

        self.id = canvas.create_rectangle(left_x, top_y, right_x, bottom_y, fill=color)

class Ball:
    def __init__(self, pos_x, pos_y, radius):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius

        self.id = canvas.create_oval(
            pos_x - radius,
            pos_y - radius,
            pos_x + radius,
            pos_y + radius,
            fill="yellow",
        )


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

# I've commented out the label for now
# # The text for the countdown
# label_text = tk.StringVar()
# label_text.set("Hello world")
# label = tk.Label(
#     root,
#     anchor=tk.CENTER,
#     textvariable=label_text,
#     bg="black",
#     fg="white",
#     font=("Courier", 30),
# )
# # Adds the label to the window
# label.place_configure(x=x_center, y=y_center, anchor="center")

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

ball_radius = 50

ball = Ball(
    pos_x=x_center,
    pos_y=y_center,
    radius=ball_radius,
)

root.update()

tk.mainloop()
