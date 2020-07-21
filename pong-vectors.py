import statistics
import tkinter as tk
import random
import time
import math
from collections import namedtuple
import random
import threading


def in_between(x, n1, n2):
    """
    Whether or not the number 'x' is between the numbers
    'n1' and 'n2' on the number line 
    """
    return n1 < x < n2 or n1 > x > n2


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return type(self)(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        else:
            return type(self)(self.x * other, self.y * other)

    def __neg__(self): return type(self)(-self.x, -self.y)

    __rmul__ = __mul__

    def __str__(self):
        return f"Vector({self.x}, {self.y})"


class Point(Vector):
    def __init__(self, x, y):
        super(Point, self).__init__(x, y)

    def __str__(self):
        return f"Point({self.x}, {self.y})"


#times = []

# Define ball properties and functions


class Ball:
    did_bounce = False

    def __init__(self, pos, speed, radius, tk_id, collide_lines):
        self.collide_lines = collide_lines
        self.id = tk_id
        self.speed = speed
        self.pos = pos
        self.radius = radius
        self.last_pos = pos
        self.hit_bottom = False
        self.top_y = pos.y - radius
        self.bottom_y = pos.y + radius
        self.left_x = pos.x - radius
        self.right_x = pos.x + radius
        self.is_bouncing = False
        self.draw()

    def get_edge(self):
        angle = -1
        while angle < 360:
            yield (math.cos(angle) * self.radius, math.sin(angle) * self.radius)
            angle += 1

    def update(self):
        #starttime = time.time()

        if self.is_beyond(left_wall):
            # It passed the left wall, so the right player won
            return 'Right player'
        elif self.is_beyond(right_wall):
            # It passed the left wall, so the left player won
            return 'Left player'

        self.pos += self.speed
        self.top_y += self.speed.y
        self.bottom_y += self.speed.y
        self.left_x += self.speed.x
        self.right_x += self.speed.x

        # Check if there's going to be a collision
        tried_bouncing = False
        for line in self.collide_lines:
            # Check if the edge of this ball is beyond that line
            if self.is_beyond(line):
                # print("Beyond", line.name)
                tried_bouncing = True
                if not self.is_bouncing:
                    self.bounce(line)
                    break
        if not tried_bouncing:
            self.is_bouncing = False

        self.draw()

        #times.append(time.time() - starttime)

    def bounce(self, line):
        #print("Bouncing off", line.name)
        normal = line.normal_vec
        proj = (-self.speed * normal) / (normal * normal) * normal
        self.speed = 2 * proj + self.speed
        self.is_bouncing = True

    def draw(self):
        canvas.move(self.id, self.speed.x, self.speed.y)

    def is_beyond(self, line):
        """
        Whether it's touching or gone beyond a wall or paddle
        """
        # return line.within_bounds(self) and line.distance_to_ball(self) < self.radius
        distance = line.distance_to_ball(self)
        if distance < self.radius:
            pass
            #print(distance, "to", line.name)
        return line.distance_to_ball(self) < self.radius and line.within_bounds(self)


class StraightLine:
    """
    A horizontal or vertical line that isn't seen
    """

    def __init__(self, start, end, position, name, is_wall=False):
        self.start = start
        self.end = end
        self.name = name
        self.position = position
        self.is_wall = is_wall
        self.is_horiz = self.position == 'top' or self.position == 'bottom'

        if self.position == 'left':
            self.normal_vec = Vector(1, 0)
        elif self.position == 'bottom':
            self.normal_vec = Vector(0, -1)
        elif self.position == 'right':
            self.normal_vec = Vector(-1, 0)
        elif self.position == 'top':
            self.normal_vec = Vector(0, 1)
        else:
            raise EnvironmentError

    def update(self):
        self.start += self.speed
        self.end += self.speed

    def within_bounds(self, ball):
        if self.is_wall:
            return True
        if self.is_horiz:
            if self.start.x <= ball.left_x <= self.end.x or self.start.x <= ball.right_x <= self.end.x:
                # if 'Paddle2' in self.name:
                #print("Ball is within bounds of", self.name)
                return True
            else:
                # if 'Paddle2' in self.name:
                #print("Ball is not within bounds  of", self.name)
                return False
        else:
            if self.start.y <= ball.top_y <= self.end.y or self.start.y <= ball.bottom_y <= self.end.y:
                # if 'Paddle2' in self.name:
                #print("Ball is within bounds vert of", self.name)
                return True
            else:
                # if 'Paddle2' in self.name:
                #print(ball.top_y, ball.bottom_y, self.start, self.end)
                #print("Ball is not within bounds vert of", self.name)
                return False

    def distance_to_ball(self, ball):
        """
        Returns the distance to the given ball
        """
        return abs(self.start.y - ball.pos.y) if self.is_horiz else abs(self.start.x - ball.pos.x)

# Define paddle properties and functions


class Paddle:
    def __init__(self, height, width, color, pos, is_on_left, change, name='A paddle'):
        self.height = height
        self.width = width
        self.pos_y = pos.y
        left_x = pos.x - width / 2
        top_y = pos.y - height / 2
        right_x = left_x + width
        bottom_y = top_y + height
        self.is_on_left = is_on_left
        self.edges = [
            StraightLine(Point(left_x, top_y), Point(
                right_x, top_y), 'bottom', f'Top({name})'),  # Top
            StraightLine(Point(left_x, bottom_y), Point(
                right_x, bottom_y), 'top', f'Bottom({name})'),  # Bottom
            # StraightLine(Point(left_x, top_y), Point(left_x, bottom_y), 'left', f'Left({name})'), # Left side
            # StraightLine(Point(right_x, top_y), Point(right_x, bottom_y), 'right', f'Right({name})') # Right side
        ]
        if is_on_left:
            # The right side edge
            self.edges.insert(0, StraightLine(Point(right_x, top_y), Point(
                right_x, bottom_y), 'right', f'Right({name})'))
        else:
            # The left side edge
            self.edges.insert(0, StraightLine(Point(left_x, top_y), Point(
                left_x, bottom_y), 'left', f'Left({name})'))

        self.id = canvas.create_rectangle(
            left_x, top_y, right_x, bottom_y, fill=color)
        self.name = name
        self.change = change

    def move(self, movement):
        # Redraw the paddle
        canvas.move(self.id, 0, movement)

        # Update the position
        self.pos_y += movement

        # Update the positions of the lines
        for edge in self.edges:
            edge.start += Vector(0, movement)
            edge.end += Vector(0, movement)

    def move_up(self, evt):
        if self.pos_y - self.height / 2 >= y_top_limit:
            self.move(-self.change)

    def move_down(self, evt):
        if self.pos_y + self.height / 2 <= y_bottom_limit:
            self.move(self.change)


x_right_limit = 700
x_left_limit = 0
y_bottom_limit = 700
y_top_limit = 0

x_center = (x_left_limit + x_right_limit) / 2
y_center = (y_top_limit + y_bottom_limit) / 2

# Create window and canvas to draw on
root = tk.Tk()
root.title("Ball Game")
canvas = tk.Canvas(
    root,
    width=x_right_limit - x_left_limit,
    height=y_bottom_limit - y_top_limit,
    bd=0,
    bg='white')
canvas.pack()

label_text = tk.StringVar()
label = tk.Label(root, anchor=tk.CENTER,
                 textvariable=label_text, bg='black', fg='white', font=('Courier', 30))
label.pack()
label.place(x=x_center, y=y_center, anchor='center')

# Countdown
for t in range(3, 1, -1):
    label_text.set(str(t))
    root.update()
    time.sleep(1)

label_text.set("GO!")
root.update()
time.sleep(1)
label_text.set("")
root.update()

top_wall = StraightLine(
    start=Point(x_left_limit, y_top_limit),
    end=Point(x_right_limit, y_top_limit),
    position='top',
    name="Top wall",
    is_wall=True
)
bottom_wall = StraightLine(
    start=Point(x_left_limit, y_bottom_limit),
    end=Point(x_right_limit, y_bottom_limit),
    position='bottom',
    name="Bottom wall",
    is_wall=True
)
left_wall = StraightLine(
    start=Point(x_left_limit, y_top_limit),
    end=Point(x_left_limit, y_bottom_limit),
    position='left',
    name="Left wall",
    is_wall=True
)
right_wall = StraightLine(
    start=Point(x_right_limit, y_top_limit),
    end=Point(x_right_limit, y_bottom_limit),
    position='right',
    name="Right wall",
    is_wall=True
)

paddle_width = 50
# How much the paddles move when the keys are pressed
paddle_movement = 15

left_paddle = Paddle(
    height=200,
    width=paddle_width,
    color='blue',
    is_on_left=True,
    pos=Point(x_left_limit + paddle_width/2, y_center),
    change=paddle_movement,
    name='Left paddle'
)
right_paddle = Paddle(
    height=200,
    width=paddle_width,
    color='red',
    is_on_left=False,
    pos=Point(x_right_limit - paddle_width/2, y_center),
    change=paddle_movement,
    name='Right paddle'
)

# The keys 'w' and 's' make the left paddle move up and down
w_bind_id = root.bind('w', left_paddle.move_up)
s_bind_id = root.bind('s', left_paddle.move_down)

# The up and down arrow keys make the left paddle move up and down
up_bind_id = root.bind('<KeyPress-Up>', right_paddle.move_up)
down_bind_id = root.bind('<KeyPress-Down>', right_paddle.move_down)


# Randomly choose a speed for the ball
speed_min = 0.02
speed_max = 0.09
x_speed = random.uniform(speed_min, speed_max)
y_speed = random.uniform(speed_min, speed_max)

ball_radius = 50

ball_id = canvas.create_oval(
    x_center - ball_radius,
    y_center - ball_radius,
    x_center + ball_radius,
    y_center + ball_radius,
    fill='yellow')

ball = Ball(
    tk_id=ball_id,
    radius=ball_radius,
    pos=Point(x_center, y_center),
    collide_lines=[top_wall, bottom_wall, left_wall,
                   right_wall] + left_paddle.edges + right_paddle.edges,
    speed=Vector(x_speed, y_speed)
)

won = False

# Loop to actually run the game
while not won:
    start_time = time.time()
    #thread = threading.Thread(target=waitAWhile)
    # thread.start()
    root.update_idletasks()
    root.update()
    won = ball.update()
    # thread.join()
    #times.append(time.time() - start_time)

#print(max(times))

print(won, 'has won!')
label_text.set(f"{won} has won!")
# print(max(times))

# stop them from moving afterwards
root.unbind('w', w_bind_id)
root.unbind('s', s_bind_id)
root.unbind('<KeyPress-Up>', up_bind_id)
root.unbind('<KeyPress-Down>', down_bind_id)

root.update()

tk.mainloop()
