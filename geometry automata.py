import tkinter as tk
from scipy.spatial.distance import cdist


root = tk.Tk()
canvas = tk.Canvas(root, width=300, height=200, bg='black')
canvas.pack(fill="both", expand=True)

# when you click on the half circle, it becomes bold
half_circle = canvas.create_arc(100, 0, 200, 100, start=0, extent=-180, outline="white", style="arc")

def bold(event):
    canvas.itemconfigure(half_circle,width=2.5)

canvas.tag_bind(half_circle,"<Button-1>", bold)

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

