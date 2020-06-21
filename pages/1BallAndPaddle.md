# Step 1: Drawing paddles and a ball

We're going to be using **Tkinter**, Python's default GUI framework, to draw everything. While it may not be considered the best framework out there, it doesn't require any downloads and is relatively easy to use.

The first thing to do is add the necessary imports. The name of the module is `tkinter`, but it's an idiom to import it as `tk`, which is easier to type.

Open up your favorite editor (preferably with at least syntax highlighting support). Create a new file called something like `pong.py` and add the following line to it.

```python
import tkinter as tk
```

To create the window that everything will be drawn on, we will create an instance of the `Tk` class in the `tkinter` module.

```python
root = tk.Tk()
```

Here, `root` is the main part of the application, and all the other shapes, labels, buttons, etc. (called "widgets") will be added to `root` (directly or indirectly).

To set the title, we can use the `title` method:

```python
root.title("Pong")
```

Now we'll need a canvas to draw the paddles and the ball on. For that, you'll have to create a `Canvas` object

```python
# I'm storing the width and height in these variables so
# they can be used later
canvas_width = 700
canvas_height = 700

canvas = tk.Canvas(
    root,
    width=canvas_width,
    height=canvas_height,
)
```

This will create a canvas whose master is `root` with the specified width and height. You can configure more things about the canvas, such as the border width (with the `bd` option) and the background color (with `background` or `bg`). [Here][1] is a list of the options you can pass in (it's for a different function, but it should work for the `Canvas` constructor too).

The result will look something like this

![Step 1](media/Step1BallAndPaddle.png)

[1]: https://effbot.org/tkinterbook/canvas.htm#Tkinter.Canvas.config-method
