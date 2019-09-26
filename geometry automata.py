import tkinter as tk
import time
import numpy

root = tk.Tk()
canvas = tk.Canvas(root, width=500, height=200, bg='black')
# keystrokes
def key(event):
    print("pressed", repr(event.char))

# apply key binding
canvas.bind("<Key>",key)
canvas.pack(fill="both", expand=True)


WIDTH = 5
# direction will be dynamic later
direction='LEFT'

# motion will be dynamic later
motion='FULLMOON'



# apply bold to line
def bold(event):
    # find arc user meant
    id = event.widget.find_closest(event.x,event.y)[0]
    # bold arc
    canvas.itemconfigure(id,width=WIDTH)
    # redraw canvas
    canvas.update()
    # give time to make each drawing piecemeal
    time.sleep(.5)

    if motion == 'FULLMOON':

        if direction == 'RIGHT':
            # when there are no more arcs to the right
            while (id != event.widget.find_closest(event.x + arc_width, event.y)[0]):
                # move cursor to the right
                event.x += arc_width
                id = event.widget.find_closest(event.x, event.y)[0]
                # bold the new arc
                canvas.itemconfigure(id, width=WIDTH)
                canvas.update()
                time.sleep(.5)

        elif direction == 'LEFT':
            # when there are no more arcs to the left
            while (id != event.widget.find_closest(event.x - arc_width, event.y)[0]):
                # move cursor to the left
                event.x -= arc_width
                id = event.widget.find_closest(event.x, event.y)[0]
                # bold the new arc
                canvas.itemconfigure(id, width=WIDTH)
                canvas.update()
                time.sleep(.5)

        elif direction == 'UP':
            # when there are no more arcs upwards
            while (id != event.widget.find_closest(event.x, event.y + arc_width)[0]):
                # move cursor upwards
                event.y += arc_width
                id = event.widget.find_closest(event.x, event.y)[0]
                # bold the new arc
                canvas.itemconfigure(id, width=WIDTH)
                canvas.update()
                time.sleep(.5)

        elif direction == 'DOWN':
            # when there are no more arcs downwards
            while (id != event.widget.find_closest(event.x, event.y - arc_width)[0]):
                # move cursor downwards
                event.y -= arc_width
                id = event.widget.find_closest(event.x, event.y)[0]
                # bold the new arc
                canvas.itemconfigure(id, width=WIDTH)
                canvas.update()
                time.sleep(.5)


# each bounding box is 100 x 100
class Box():
    def __init__(self, coords):
        # give the class a tag for tkinter to find later
        self.tag = 'box{}'.format(id(self))

        # make each arc
        self.arcs = [
            # arc 1
            canvas.create_arc(coords, start=0, extent=90, outline="white", style="arc", tag=(self.tag, 1)),
            # arc 2
            canvas.create_arc(coords, start=90, extent=90, outline="white", style="arc", tag=(self.tag, 2)),
            # arc 3
            canvas.create_arc(coords, start=180, extent=90, outline="white", style="arc", tag=(self.tag, 3)),
            # arc 4
            canvas.create_arc(coords, start=270, extent=90, outline="white", style="arc", tag=(self.tag, 4))
        ]

        # allow each arc to be bolded
        self.bind()

    def bind(self):
        # apply binding to every arc in box
        for arc in self.arcs:
            canvas.tag_bind(arc, "<Button-1>", bold)

# coordinates are (x,y) of upper left corner, and then (x,y) of lower left corner
# use numpy array for vector addition
coords = numpy.array([0, 0, 100, 100])


# use box width to calculate grid indice
box_width = coords[2] - coords[0]
# grid indice to move around
grid_indice = box_width/2

# use arc width for width of 1 component
# 4 components in 1 box
arc_width = box_width/2

# make desired size of grid (width, height)
size=[12,8]

for i in range(size[1]):
    # keep adding 1 grid indice to the y as you move down
    coords = coords + numpy.array([0, 0 + grid_indice, 0, 0 + grid_indice])

    for j in range(size[0]):
        # keep adding 1 grid indice to the x as you move to the right
        box_coords = coords + numpy.array([0 + grid_indice*j, 0, 0 + grid_indice*j, 0])

        # create variables to check parity
        even_row = i%2 == 0
        odd_row = not even_row
        even_column = j%2 == 0
        odd_column = not even_column

        # only draw a box on the same parity of i and j
        # that is: on an odd row (i), only draw on odd column (j) values
        if even_row & even_column:
            Box(tuple(box_coords))
        elif odd_row & odd_column:
            Box(tuple(box_coords))


root.mainloop()

