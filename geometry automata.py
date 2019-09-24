import tkinter as tk
import time

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

# use box width to later move around
box_width = coords[2] - coords[0]

# use arc width for width of 1 component
# 4 components in 1 box
arc_width = box_width/2

arc_one = canvas.create_arc(coords, start=0, extent=90, outline="white", style="arc",tag=1)

arc_two = canvas.create_arc(coords, start=90, extent=90, outline="white", style="arc",tag=2)

arc_three = canvas.create_arc(coords, start=180, extent=90, outline="white", style="arc",tag=3)

arc_four = canvas.create_arc(coords, start=270, extent=90, outline="white", style="arc",tag=4)

'''
I want to just bundle arcs one to four into a single method, and call it with new coordinates to create many new 
circles. 

However, I won't be able to call each arc later if I do so.
'''

# second bounding box to the right
coords_2 = (100 + 100, 50, 200 + 100, 150)

arc_five = canvas.create_arc(coords_2, start=0, extent=90, outline="white", style="arc",tag=1)

arc_six = canvas.create_arc(coords_2, start=90, extent=90, outline="white", style="arc",tag=2)

arc_seven = canvas.create_arc(coords_2, start=180, extent=90, outline="white", style="arc",tag=3)

arc_eight = canvas.create_arc(coords_2, start=270, extent=90, outline="white", style="arc",tag=4)


def bold(event):
    id = event.widget.find_closest(event.x,event.y)[0]
    canvas.itemconfigure(id,width=2.5)
    canvas.update()
    time.sleep(.4)

    if direction == 'RIGHT' and motion == 'FULLMOON':
#         while there are no more new widgets
        while (id != event.widget.find_closest(event.x + arc_width, event.y)[0]):
    #         move cursor to the right
            event.x += arc_width
            id = event.widget.find_closest(event.x, event.y)[0]
            canvas.itemconfigure(id, width=2.5)
            canvas.update()
            time.sleep(.4)


canvas.tag_bind(arc_one,"<Button-1>", bold)
canvas.tag_bind(arc_two,"<Button-1>", bold)
canvas.tag_bind(arc_three,"<Button-1>", bold)
canvas.tag_bind(arc_four,"<Button-1>", bold)

canvas.tag_bind(arc_five,"<Button-1>", bold)
canvas.tag_bind(arc_six,"<Button-1>", bold)
canvas.tag_bind(arc_seven,"<Button-1>", bold)
canvas.tag_bind(arc_eight,"<Button-1>", bold)


root.mainloop()

