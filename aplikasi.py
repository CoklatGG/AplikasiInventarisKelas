import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-Page App")
        self.geometry("400x300")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (Page1, Page2):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        print(self.frames)

        self.show_frame(Page1)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


class Page1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        label = tk.Label(self, text="Page 1")
        label.pack(pady=10)

        btn = tk.Button(self, text="Go to Page 2",
                        command=lambda: controller.show_frame(Page2))
        btn.pack()


class Page2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        label = tk.Label(self, text="Page 2")
        label.pack(pady=10)

        btn = tk.Button(self, text="Back to Page 1",command=self.bebek)
        btn.pack()
    
    def bebek(self):
        self.controller.show_frame(Page1)
        



if __name__ == "__main__":
    app = App()
    app.mainloop()