import tkinter as tk
import tkinter.font as tkfont

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Inventaris Kelas")
        self.geometry("800x600")
        self.resizable(False, False)
        self.option_add("*Button.cursor", "hand2")
        self.option_add("*Checkbutton.cursor", "hand2")
        
        default_font = tkfont.nametofont(name="TkDefaultFont")
        default_font.config(size=14)
        default_font = tkfont.nametofont(name="TkTextFont")
        default_font.config(size=14)

        container: tk.Frame = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Login, Register):
            frame: tk.Frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Login)

    def show_frame(self, page):
        frame: tk.Frame = self.frames[page]
        frame.tkraise()


class Login(tk.Frame):
    def __init__(self, parent, root: tk.Tk):
        super().__init__(parent, )

        root.geometry("800x600")

        login_frame = tk.Frame(self, width=400, height=550, bg="cyan", borderwidth=5, relief="ridge")
        login_frame.pack_propagate(False)
        login_frame.pack(expand=True)

        self.img = tk.PhotoImage(file="res/placeholder.png")
        
        tk.Label(login_frame, image=self.img).place(anchor="center", relx=0.5, rely=0.2)  

        entry_frame = tk.Frame(login_frame, bg="purple")
        entry_frame.place(anchor="center", rely=0.51, relx=0.5)

        username_frame = tk.Frame(entry_frame, bg="red")
        username_frame.pack(expand=True, pady=10)

        username_label = tk.Label(username_frame, text="Username")
        username_label.grid(row=0, column=0, sticky="w")

        self.username_ent = tk.Entry(username_frame, width=30)
        self.username_ent.grid(row=1, column=0)

        password_frame = tk.Frame(entry_frame, bg="blue")
        password_frame.pack(expand=True, pady=10)

        password_label = tk.Label(password_frame, text="Password")
        password_label.grid(row=0, column=0, sticky="w")

        self.password_ent = tk.Entry(password_frame, width=30, show="•")
        self.password_ent.grid(row=1, column=0)

        self.password_hidden = tk.IntVar()
        self.password_hidden.set(1)
        tk.Checkbutton(entry_frame, variable=self.password_hidden, onvalue=0, offvalue=1, command=self.password_show_hide, text="Show Password").pack(anchor="w")

        tk.Button(login_frame, text="Login", command=self.login).place(anchor="center", relx=0.5, rely=0.77)
        tk.Label(login_frame, text="Or").place(anchor="center", relx=0.5, rely=0.85)
        tk.Button(login_frame, text="Register", command=self.register).place(anchor="center", relx=0.5, rely=0.93)


    def password_show_hide(self):
        if bool(self.password_hidden.get()):
            self.password_ent.config(show="•")
        else:
            self.password_ent.config(show="")

        

    
    def login(self):
        pass


    def register(self):
        root.show_frame(Register)




class Register(tk.Frame):
    def __init__(self, parent, root: tk.Tk):
        super().__init__(parent, )

        root.geometry("800x600")

        login_frame = tk.Frame(self, width=400, height=550, bg="cyan", borderwidth=5, relief="ridge")
        login_frame.pack_propagate(False)
        login_frame.pack(expand=True)

        entry_frame = tk.Frame(login_frame, bg="purple")
        entry_frame.place(anchor="center", rely=0.375, relx=0.5)

        username_frame = tk.Frame(entry_frame, bg="red")
        username_frame.pack(expand=True, pady=10)

        username_label = tk.Label(username_frame, text="Username")
        username_label.grid(row=0, column=0, sticky="w")

        self.username_ent = tk.Entry(username_frame, width=30)
        self.username_ent.grid(row=1, column=0)

        password_frame = tk.Frame(entry_frame, bg="blue")
        password_frame.pack(expand=True, pady=10)

        password_label = tk.Label(password_frame, text="Password")
        password_label.grid(row=0, column=0, sticky="w")

        self.password_ent = tk.Entry(password_frame, width=30)
        self.password_ent.grid(row=1, column=0)

        confirm_password_frame = tk.Frame(entry_frame, bg="blue")
        confirm_password_frame.pack(expand=True, pady=10)

        confirm_password_label = tk.Label(confirm_password_frame, text="Confirm Password")
        confirm_password_label.grid(row=0, column=0, sticky="w")

        self.confirm_password_ent = tk.Entry(confirm_password_frame, width=30)
        self.confirm_password_ent.grid(row=1, column=0)

        tk.Button(login_frame, text="Register", command=self.register).place(anchor="center", relx=0.5, rely=0.77)
        tk.Label(login_frame, text="Or").place(anchor="center", relx=0.5, rely=0.85)
        tk.Button(login_frame, text="Login", command=self.login).place(anchor="center", relx=0.5, rely=0.93)
    
    
    def login(self):
        root.show_frame(Login)


    def register(self):
        pass
        


if __name__ == "__main__":
    root = Root()
    root.mainloop()