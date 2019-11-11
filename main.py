##### Version 1.1.0
#
# python 3.7
# numpy 1.7.4
##### ..............

# TODO: reset focus to computer generated animations, antialias lines for
#  better look, add border for better look

import tkinter as tk
import time
import numpy

# set hex colors
cream = '#fafaeb'
umber = '#21201f'

# set background and arc colors
# can switch between cream/umber theme and white/black theme
# I thought that cream/umber would be good because it matches the book,
# but I think white/black shows on computer displays better.
bg = "black"
arc_color = "white"

# set how wide the arc becomes when it's bolded, or activated
# I thought 6 would be good because it's obvious, but I think 4.5 is the most
# aesthetic width
WIDTH = 4.5

##### initialize canvas
root = tk.Tk()
canvas = tk.Canvas(root, width=650, height=450, bg=bg)
canvas.pack(fill="both", expand=True)

# initialize motion
motion='HALFMOON'
# initialize direction
direction='DOWN'

# change direction or motion
def apply_directives(event):
    '''
    WASD or arrow keys to trigger drawing to one direction.
    Spacebar to trigger one by one drawing.
    :param event: tkinter event with attributes including the event character or
    key symbol
    :return: None
    '''
    global direction
    global motion
    if event.char == 'w' or event.keysym == "Up":
        direction = 'UP'
        motion = 'HALFMOON'
    if event.char == 's' or event.keysym == "Down":
        direction = 'DOWN'
        motion = 'HALFMOON'
    if event.char == 'd' or event.keysym == "Right":
        direction = 'RIGHT'
        motion = 'HALFMOON'
    if event.char == 'a' or event.keysym == "Left":
        direction = 'LEFT'
        motion = 'HALFMOON'

    if event.keysym == "space":
        motion = 'CLICK'

root.bind("<Key>", apply_directives)

# apply bold to arc
def bold(event):
    ##### initial boldness
    # find arc user meant
    id = event.widget.find_closest(event.x,event.y)[0]
    # retrieve arc tag
    tag = canvas.gettags(id)[1]
    # bold arc
    canvas.itemconfigure(id,width=WIDTH)
    # redraw canvas
    canvas.update()
    # give time to make each drawing piecemeal
    time.sleep(.5)

    ##### propagate motion
    if motion == 'HALFMOON':

        # find within the next enclosed box in the right, the arc with a tag that fits the motion type so long as
        # there are no more arcs to the right
        set_a = 0
        set_b = 0

        # sets inverse depending on vertical or horizontal direction
        if direction == 'RIGHT' or direction == 'LEFT':
            set_a = ['1','2']   # tags are in type string, so we match the type
            set_b = ['3','4']
        if direction == 'UP' or direction == 'DOWN':
            set_a = ['1','4']   # tags are in type string, so we match the type
            set_b = ['2','3']

        current_set = []

        # check to see what kind of curve this is
        if tag in set_a:
            current_set = set_a
        else:
            current_set = set_b

        # TODO: Sometimes takes an arc that shouldn't be within the bounding box, but can't consistently
        #  replicate this. find out way and fix

        # direction logic
        directional_additive = 0
        if direction == 'RIGHT':
            directional_additive = numpy.array([arc_width,0])
        if direction == 'LEFT':
            directional_additive = numpy.array([-arc_width,0])
        if direction == 'UP':
            directional_additive = numpy.array([0,-arc_width])
        if direction == 'DOWN':
            directional_additive = numpy.array([0,arc_width])
        prev_id = 0

        # when there are no more arcs to the desired direction
        while (id != prev_id):
            # set up variables to find next coordinates
            current_box_coords = numpy.array(canvas.coords(id))
            # box is too big, we just want the arc box
            normalizer = 0
            if tag == '1': # take upper right of box
                normalizer = numpy.array([arc_width,0,0,-arc_width])
            if tag == '2': # take upper left of box
                normalizer = numpy.array([0,0,-arc_width,-arc_width])
            if tag == '3': # take lower left of box
                normalizer = numpy.array([0,arc_width,-arc_width,0])
            if tag == '4': # take lower right of box
                normalizer = numpy.array([arc_width,arc_width,0,0])
            current_arc_coords = current_box_coords + normalizer
            next_coords_additive = 0
            # directional logic
            if direction == 'RIGHT':
                next_coords_additive = numpy.array([arc_width,0,arc_width,0])
            if direction == 'LEFT':
                next_coords_additive = numpy.array([-arc_width,0,-arc_width,0])
            if direction == 'UP':
                next_coords_additive = numpy.array([0,-arc_width,0,-arc_width])
            if direction == 'DOWN':
                next_coords_additive = numpy.array([0,arc_width,0,arc_width])
            # tkinter's find_enclosed method will exclude any objects it finds right at the perimeter, so make the perimeter slightly larger
            boundaries_additive = numpy.array([-1,-1,1,1])
            # obtain the next coordinates
            next_coords = current_arc_coords + next_coords_additive + boundaries_additive

            # obtain list of the next IDs
            next_ids = event.widget.find_enclosed(*next_coords)

            # obtain list of the next tags
            next_tags = [canvas.gettags(next_id)[1] for next_id in next_ids]

            last_event_x = event.x
            prev_id = id

            for next_id,next_tag in zip(next_ids,next_tags):
                if ((id != next_id) & (next_tag in current_set)):
                    # move cursor to the desired direction
                    if direction == 'RIGHT':
                        event.x += arc_width
                    if direction == 'LEFT':
                        event.x -= arc_width
                    if direction == 'UP':
                        event.y -= arc_width
                    if direction == 'DOWN':
                        event.y += arc_width

                    # bold the new arc
                    canvas.itemconfigure(next_id, width=WIDTH)
                    canvas.update()
                    time.sleep(.5)
                    # update current arc
                    id = event.widget.find_closest(event.x, event.y)[0]
                    # update current tag
                    tag = canvas.gettags(id)[1]


class Box():
    def __init__(self, coords):
        # give the class a tag for tkinter to find later
        self.tag = 'box{}'.format(id(self))

        # make each arc
        self.arcs = [
            # arc 1
            canvas.create_arc(coords, start=0, extent=90, outline=arc_color,
                              style="arc", tag=(self.tag, 1)),
            # arc 2
            canvas.create_arc(coords, start=90, extent=90, outline=arc_color,
                              style="arc", tag=(self.tag, 2)),
            # arc 3
            canvas.create_arc(coords, start=180, extent=90, outline=arc_color,
                              style="arc", tag=(self.tag, 3)),
            # arc 4
            canvas.create_arc(coords, start=270, extent=90, outline=arc_color,
                              style="arc", tag=(self.tag, 4))
        ]

        # allow each arc to be bolded
        self.bind()

    def bind(self):
        # apply binding to every arc in box
        for arc in self.arcs:
            canvas.tag_bind(arc, "<Button-1>", bold)

# coordinates are (x,y) of upper left corner, and then (x,y) of lower left corner
# use numpy array for vector addition
# each bounding box is 100 x 100
coords = numpy.array([0, 0, 100, 100])

# use box width to calculate grid indice
box_width = coords[2] - coords[0]
# grid indice to move around
grid_indice = box_width/2

# use arc width for width of 1 component
# 4 components in 1 box
arc_width = box_width/2

# make desired size of grid (width, height)
multiplier = 4
size=[6*multiplier,4*multiplier]

def init_grid(size, coords, grid_indice):
    """
    Create the initial grid by passing in the width and height
    :param size: list of [width, height]
    :return: None
    """
    for i in range(size[1]):
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

        # keep adding 1 grid indice to the y as you move down
        coords = coords + numpy.array([0, 0 + grid_indice, 0, 0 + grid_indice])

init_grid(size, coords, grid_indice)

root.mainloop()

