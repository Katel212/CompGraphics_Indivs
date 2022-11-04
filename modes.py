class DummyMode:
    def __init__(self):
        pass

    def handle_motion(self, event):
        pass

    def handle_press(self, event):
        pass

    def handle_release(self, event):
        pass


class AddMode:
    def __init__(self, canvas):
        self.canvas = canvas
        pass

    def handle_motion(self, event):
        pass

    def handle_press(self, event):
        if event.widget == self.canvas:
            self.canvas.points.append((event.x, event.y))
            self.canvas.redraw_points()

    def handle_release(self, event):
        pass
