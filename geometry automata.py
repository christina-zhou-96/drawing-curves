import tkinter as tk
import time

root = tk.Tk()
canvas = tk.Canvas(root, width=300, height=200, bg='black')
canvas.pack(fill="both", expand=True)

# direction will be dynamic later
direction='RIGHT'

# motion will be dynamic later
motion='FULLMOON'

# apply bold to line
def bold(event):
    # find arc user meant
    id = event.widget.find_closest(event.x,event.y)[0]
    # bold arc
    canvas.itemconfigure(id,width=3)
    # redraw canvas
    canvas.update()
    # give time to make each drawing piecemeal
    time.sleep(.5)

    if direction == 'RIGHT' and motion == 'FULLMOON':
        # when there are no more arcs to the right
        while (id != event.widget.find_closest(event.x + arc_width, event.y)[0]):
            # move cursor to the right
            event.x += arc_width
            id = event.widget.find_closest(event.x, event.y)[0]
            # bold the new arc
            canvas.itemconfigure(id, width=3)
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
coords = (0, 0, 100, 100)

# use box width to later move around
box_width = coords[2] - coords[0]

# use arc width for width of 1 component
# 4 components in 1 box
arc_width = box_width/2

box1=Box(coords)

# second bounding box to the right
coords_2 = (0+100, 0, 100+100, 100)
box2=Box(coords_2)

coords_3 = (0+100+100,0,100+100+100,100)
box3=Box(coords_3)

coords_4 = (50,50,150,150)
box4=Box(coords_4)

coords_5 = (50+100,50,150+100,150)
box5=Box(coords_5)

coords_6 = (0, 0+100, 100, 100+100)
box6=Box(coords_6)

coords_7 = (0+100, 0+100, 100+100, 100+100)
box7=Box(coords_7)

coords_8 = (0+100+100, 0+100, 100+100+100, 100+100)
box8=Box(coords_8)

root.mainloop()

