import tkinter as tk

# root will be the window to put everything in
root = tk.Tk()
# Set the title
root.title("Pong")


canvas_width = 700
canvas_height = 650

# The canvas is where everything will be drawn
canvas = tk.Canvas(
    root,
    width=canvas_width,
    height=canvas_height,
    bg="black",
)
# Adds the canvas to the window
canvas.pack()

x_center = canvas_width / 2
y_center = canvas_height / 2

# The text for the countdown
label_text = tk.StringVar()
label_text.set("Hello world")
label = tk.Label(
    root,
    textvariable=label_text,
    bg="black",
    fg="white",
    font=("Courier", 30),
)
label.pack()
label.place_configure(x=x_center, y=200, anchor="center")

paddle_height = 200
paddle_width = 50

left_paddle_id = canvas.create_rectangle(
    0,
    y_center - paddle_height / 2,
    0 + paddle_width,
    y_center + paddle_height / 2,
    fill='blue',
)

right_paddle_id = canvas.create_rectangle(
    canvas_width - paddle_width,
    y_center - paddle_height / 2,
    canvas_width,
    y_center + paddle_height / 2,
    fill='red',
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