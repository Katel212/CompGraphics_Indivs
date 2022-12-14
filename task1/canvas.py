from tkinter import Canvas, PhotoImage

class MyCanvas(Canvas):
    def __init__(self, tk, width, height, bg="white"):
        super().__init__(tk, width=width, height=height, bg=bg)
        self.width = width
        self.height = height
        self.points = []
        self.hull = []
        self.create_image()

    # def redraw_content(self):
    #     self.clear()

    def delete_content(self):
        self.points = []
        self.hull = []
        self.clear()

    def clear(self):
        self.delete('all')
        self.create_image()

    def create_image(self, state="normal"):
        self.image = PhotoImage(width=self.width, height=self.height)
        super().create_image((self.width / 2, self.height / 2), image=self.image, state=state)

    def draw_circle(self, x, y, r=10, color="magenta"):
        self.create_oval(x - r, y - r, x + r, y + r, fill=color, outline=color)

    # перерисовываем точки и кривую
    def redraw_points(self):
        self.clear()
        for p in self.points:
            self.draw_circle(p[0], p[1], 3)
        #draw_hull
