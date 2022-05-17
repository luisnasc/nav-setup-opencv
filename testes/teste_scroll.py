import tkinter
import ScrollableImage

root = tkinter.Tk()

# PhotoImage from tkinter only supports:- PGM, PPM, GIF, PNG format.
# To use more formats use PIL ImageTk.PhotoImage
img = tkinter.PhotoImage(file="map.png")

image_window = ScrollableImage(root, image=img, scrollbarwidth=6, 
                               width=200, height=200)
image_window.pack()

root.mainloop()