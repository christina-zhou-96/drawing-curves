import tkinter as tk
from scipy.spatial.distance import cdist


root = tk.Tk()
canvas = tk.Canvas(root, width=300, height=200, bg='black')
canvas.pack(fill="both", expand=True)

# direction will be dynamic later
direction='RIGHT'

# motion will be dynamic later
motion='FULLMOON'

# each bounding box is 100 x 100
# coordinates are (x,y) of upper left corner, and then (x,y) of lower left corner

coords = (100, 50, 200, 150)

arc_one = canvas.create_arc(coords, start=0, extent=90, outline="white", style="arc")

arc_two = canvas.create_arc(coords, start=90, extent=90, outline="white", style="arc")

arc_three = canvas.create_arc(coords, start=180, extent=90, outline="white", style="arc")

arc_four = canvas.create_arc(coords, start=270, extent=90, outline="white", style="arc")

# second bounding box to the right
coords_2 = (100 + 100, 50, 200 + 100, 150)

arc_five = canvas.create_arc(coords_2, start=0, extent=90, outline="white", style="arc")

arc_six = canvas.create_arc(coords_2, start=90, extent=90, outline="white", style="arc")

arc_seven = canvas.create_arc(coords_2, start=180, extent=90, outline="white", style="arc")

arc_eight = canvas.create_arc(coords_2, start=270, extent=90, outline="white", style="arc")


def bold(event):
    id = event.widget.find_closest(event.x,event.y)[0]
    canvas.itemconfigure(id,width=2.5)

canvas.tag_bind(arc_one,"<Button-1>", bold)
canvas.tag_bind(arc_two,"<Button-1>", bold)
canvas.tag_bind(arc_three,"<Button-1>", bold)
canvas.tag_bind(arc_four,"<Button-1>", bold)

canvas.tag_bind(arc_five,"<Button-1>", bold)
canvas.tag_bind(arc_six,"<Button-1>", bold)
canvas.tag_bind(arc_seven,"<Button-1>", bold)
canvas.tag_bind(arc_eight,"<Button-1>", bold)


root.mainloop()

def arc_one(coords):
    return canvas.create_arc(coords, start=0, extent=90, outline="white", style="arc")

def arc_two(coords):
    return canvas.create_arc(coords, start=90, extent=90, outline="white", style="arc")

def arc_three(coords):
    return canvas.create_arc(coords, start=180, extent=90, outline="white", style="arc")

def arc_four(coords):
    return canvas.create_arc(coords, start=270, extent=90, outline="white", style="arc")

class Box():
    def __init__(self, x,y,x1,y1):
        self.x = x
        self.y = y
        self.x1 = x1
        self.y1 = y1
        self.coords = x,y,x1,y1
        self.one = arc_one(coords)
        self.two = arc_two(coords)
        self.three = arc_three(coords)
        self.four = arc_four(coords)

coords = (100, 50, 200, 150)
unit_1 = Box(coords)

def closest_node(node, nodes):
    return nodes[cdist([node], nodes).argmin()]

def draw(x,y):
    point = closest_node([x,y],[(150,100),(200,100),(150,150),(100,00)])


def start(event):
    global lastx, lasty
    lastx, lasty = event.x, event.y
    draw(lastx, lasty)



root.mainloop()
# canvas.itemconfig(one,fill='red')

