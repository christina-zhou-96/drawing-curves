import tkinter as tk
import time
import numpy

root = tk.Tk()
canvas = tk.Canvas(root, width=500, height=200, bg='black')
canvas.pack(fill="both", expand=True)

# direction will be dynamic later
direction='RIGHT'

# motion will be dynamic later
motion='FULLMOON'

# apply bold to line
def bold(event):
    # initial boldness
    # find arc user meant
    id = event.widget.find_closest(event.x,event.y)[0]
    # retrieve arc tag
    tag = canvas.gettags(id)[1]
    print(tag)
    print(type(tag))
    # bold arc
    canvas.itemconfigure(id,width=5)
    # redraw canvas
    canvas.update()
    # give time to make each drawing piecemeal
    time.sleep(.5)

    # directional logic
    if direction == 'RIGHT':
        if motion == 'FULLMOON':

            # find within the next enclosed box in the right, the arc with a tag that fits the motion type so long as
            # there are no more arcs to the right

            set_a = ['1','2']   # tags are in type string, so we match the type
            set_b = ['3','4']
            current_set = []

            # check to see what kind of curve this is
            if tag in set_a:
                current_set = set_a
            else:
                current_set = set_b


            if tag == '2':
                # set up variables to find next coordinates
                current_box_coords = numpy.array(canvas.coords(id))
                arc_2_normalizer = numpy.array([0,0,-arc_width,-arc_width]) # box is too big, we just want the arc box
                current_arc_coords = current_box_coords + arc_2_normalizer
                next_coords_additive = numpy.array([arc_width,0,0,arc_width])
                # tkinter's find_enclosed method will exclude any objects it finds right at the perimeter, so make the perimeter slightly larger
                boundaries_additive = numpy.array([-1,-1,1,1])
                # obtain the next coordinates
                next_coords = current_arc_coords + next_coords_additive + boundaries_additive

            # obtain list of the next IDs
            next_ids = event.widget.find_enclosed(*next_coords)

            # obtain list of the next tags
            next_tags = [canvas.gettags(next_id)[1] for next_id in next_ids]

            for next_id,next_tag in zip(next_ids,next_tags):
                while ((id != next_id) & (next_tag in current_set)):
                    # move cursor to the right
                    event.x += arc_width
                    # bold the new arc
                    canvas.itemconfigure(next_id, width=5)
                    canvas.update()
                    time.sleep(.5)
                    # update current arc
                    id = event.widget.find_closest(event.x, event.y)[0]
                    # update next arc
                    next_id = event.widget.find_closest(event.x + arc_width, event.y)[0]
                    # update next arc tag
                    next_tag = canvas.gettags(next_id)[1]

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
size=[6,4]

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

