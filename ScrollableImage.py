import tkinter

class ScrollableImage(tkinter.Frame):
    def __init__(self, master=None, **kw):
        self.image = kw.pop('image', None)
        sw = kw.pop('scrollbarwidth', 10)
        super(ScrollableImage, self).__init__(master=master, **kw)
        self.cnvs = tkinter.Canvas(self, highlightthickness=0, **kw)
        self.cnvs.create_image(0, 0, anchor='nw', image=self.image)
        #self.cnvs.place(relx=0.0, rely=1.0, anchor=SW)

        # Vertical and Horizontal scrollbars
        self.v_scroll = tkinter.Scrollbar(self, orient='vertical', width=sw)
        self.h_scroll = tkinter.Scrollbar(self, orient='horizontal', width=sw)
        # Grid and configure weight.
        self.cnvs.grid(row=0, column=0,  sticky='nsew')
        self.h_scroll.grid(row=1, column=0, sticky='ew')
        self.v_scroll.grid(row=0, column=1, sticky='ns')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # Set the scrollbars to the canvas
        self.cnvs.config(xscrollcommand=self.h_scroll.set, 
                           yscrollcommand=self.v_scroll.set)
        # Set canvas view to the scrollbars
        self.v_scroll.config(command=self.cnvs.yview)
        self.h_scroll.config(command=self.cnvs.xview)
        # Assign the region to be scrolled 
        self.cnvs.config(scrollregion=self.cnvs.bbox('all'))
        self.cnvs.bind_class(self.cnvs, "<MouseWheel>", self.mouse_scroll)
        self.cnvs.bind_class(self.cnvs, "<Button-4>", self.mouse_scroll)
        self.cnvs.bind_class(self.cnvs, "<Button-5>", self.mouse_scroll)
        self.cnvs.bind_class(self.cnvs, "<Button-2>", self.mouse_scroll)

    def mouse_scroll(self, evt):
        passo = 3
        if evt.num==5: #evt.state == 0 :
            if evt.state == 16:
                self.cnvs.yview_scroll(passo, 'units')
            elif evt.state == 17:
                self.cnvs.xview_scroll(passo, 'units')
            #elif evt.state == 20:
            #    print('zoom out')
        if evt.num == 2:
            print('meioooo')
        if evt.num==4: #evt.state == 1:
            if evt.state == 16:
                self.cnvs.yview_scroll(-passo, 'units')
            elif evt.state == 17:
                self.cnvs.xview_scroll(-passo, 'units') # For MacOS
            #elif evt.state == 20:
            #    print('zoom in')

    def reset_canvas(self, ids):
        for i in ids:
            self.cnvs.delete(i)

'''
root = tkinter.Tk()
img = tkinter.PhotoImage(file="map.png")

image_window = ScrollableImage(root, image=img, scrollbarwidth=6, 
                               width=200, height=200)
image_window.pack()

root.mainloop()
'''