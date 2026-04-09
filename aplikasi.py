import tkinter as tk

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Inventaris Kelas")
        self.geometry("800x600")
        self.resizable(False, False)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (Login, ):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Login)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


class Login(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)


class Register(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)


if __name__ == "__main__":
    root = Root()
    root.mainloop()