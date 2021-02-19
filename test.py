from tkinter import Tk, Frame, Canvas, BOTH, YES

import typing as ty


# a subclass of Canvas for dealing with resizing of windows
class ResizingCanvas(Canvas):

    def __init__(self, parent: Frame, **kwargs: ty.Any) -> None:
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        self.draw_staff()

    def on_resize(self, event: ty.Any):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        # self.scale("all", 0, 0, wscale, hscale)
        self.delete('all')
        self.draw_staff()

    def draw_staff(self) -> None:
        margins = 50
        left, rigth = margins, self.width - margins
        top, bottom = margins, self.height - margins
        step = (bottom - top) / 6
        lines = [
            (left, top + step * 1, rigth, top + step * 1),
            (left, top + step * 2, rigth, top + step * 2),
            (left, top + step * 3, rigth, top + step * 3),
            (left, top + step * 4, rigth, top + step * 4),
            (left, top + step * 5, rigth, top + step * 5),
        ]
        for line in lines:
            width = self.height / 100
            if width < 5:
                width = 5
            self.create_line(line, width=width)


def main() -> None:
    root = Tk()
    myframe = Frame(root)
    myframe.pack(fill=BOTH, expand=YES)
    mycanvas = ResizingCanvas(
        myframe, width=850, height=400, bg="white", highlightthickness=0
    )
    mycanvas.pack(fill=BOTH, expand=YES)

    # add some widgets to the canvas
    # mycanvas.draw_staff()

    # tag all of the drawn widgets
    mycanvas.addtag_all("all")
    root.mainloop()


if __name__ == "__main__":
    main()