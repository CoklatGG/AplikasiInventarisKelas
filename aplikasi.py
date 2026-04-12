import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk 
import sqlite3
from time import sleep

conn = sqlite3.connect("inventaris.db")
cursor = conn.cursor()

weight_nama = 90
weight_jumlah = 30
weight_kondisi = 50
weight_lokasi = 50
weight_sum = (weight_nama + weight_jumlah + weight_kondisi + weight_lokasi)

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Inventaris Kelas")
        self.geometry("800x600")
        self.resizable(False, False)
        self.option_add("*Button.cursor", "hand2")
        self.option_add("*Checkbutton.cursor", "hand2")
        self.option_add("*TCheckbutton.cursor", "hand2")
        
        default_font = tkfont.nametofont(name="TkDefaultFont")
        default_font.config(size=14)
        default_font = tkfont.nametofont(name="TkTextFont")
        default_font.config(size=14)

        container: tk.Frame = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Login, Register, Admin):
            frame: tk.Frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Admin)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.arise(self)


class Login(tk.Frame):
    def __init__(self, parent, root: tk.Tk):
        super().__init__(parent)

        login_frame = tk.Frame(self, width=400, height=550, bg="cyan", borderwidth=5, relief="ridge")
        login_frame.pack_propagate(False)
        login_frame.pack(expand=True)

        self.img = tk.PhotoImage(file="res/placeholder.png")
        
        tk.Label(login_frame, image=self.img).place(anchor="center", relx=0.5, rely=0.2)  

        entry_frame = tk.Frame(login_frame, bg="purple")
        entry_frame.place(anchor="center", rely=0.51, relx=0.5)

        username_frame = tk.Frame(entry_frame, bg="red")
        username_frame.pack(expand=True, pady=10)

        self.username_label = tk.Label(username_frame, text="Username")
        self.username_label.grid(row=0, column=0, sticky="w")

        self.username_ent = tk.Entry(username_frame, width=30, highlightbackground="black", highlightcolor="black", highlightthickness=2, relief="flat")
        self.username_ent.grid(row=1, column=0)

        password_frame = tk.Frame(entry_frame, bg="blue")
        password_frame.pack(expand=True, pady=10)

        self.password_label = tk.Label(password_frame, text="Password")
        self.password_label.grid(row=0, column=0, sticky="w")

        self.password_ent = tk.Entry(password_frame, width=30, show="•", highlightbackground="black", highlightcolor="black", highlightthickness=2, relief="flat")
        self.password_ent.grid(row=1, column=0)

        self.password_hidden = tk.IntVar()
        self.password_hidden.set(1)
        
        self.style = ttk.Style()
        self.style.configure("Login.TCheckbutton", font=("Arial", 10))

        show_password_cb = ttk.Checkbutton(password_frame, variable=self.password_hidden, onvalue=0, offvalue=1, command=self.password_show_hide, text="Show Password", style="Login.TCheckbutton")
        show_password_cb.grid(row=2, column=0, sticky="nw")

        self.error_label = tk.Label(password_frame, text="Username atau Password salah!", fg="blue", bg="blue", font=("Arial", 10))
        self.error_label.grid(row=3, column=0)

        tk.Button(login_frame, text="Login", command=self.login).place(anchor="center", relx=0.5, rely=0.77)
        tk.Label(login_frame, text="Or").place(anchor="center", relx=0.5, rely=0.85)
        tk.Button(login_frame, text="Register", command=self.acc_register).place(anchor="center", relx=0.5, rely=0.93)

    def arise(self, root: tk.Tk):
        self.tkraise()
        root.geometry("800x600")


    def unerror(self):
        self.username_label.config(fg="black")
        self.password_label.config(fg="black")
        self.username_ent.config(highlightbackground="black", highlightcolor="black", bg="white", state="disabled")
        self.password_ent.config(highlightbackground="black", highlightcolor="black", bg="white", state="disabled")
        self.error_label.config(fg="blue")
        self.style.configure("Login.TCheckbutton", foreground="black")
        root.update()
        sleep(0.5)

    
    def error(self):
        self.username_label.config(fg="red")
        self.password_label.config(fg="red")
        self.username_ent.config(highlightbackground="red", highlightcolor="red", bg="#ffa3a3", state="normal")
        self.password_ent.config(highlightbackground="red", highlightcolor="red", bg="#ffa3a3", state="normal")
        self.error_label.config(fg="red")
        self.style.configure("Login.TCheckbutton", foreground="red")

        self.username_ent.delete(0, tk.END)
        self.password_ent.delete(0, tk.END)
        


    def password_show_hide(self):
        if bool(self.password_hidden.get()):
            self.password_ent.config(show="•")
        else:
            self.password_ent.config(show="")

    
    def login(self):
        username_input = self.username_ent.get()
        password_input = self.password_ent.get()

        self.unerror()

        result = cursor.execute("SELECT * FROM user WHERE username=?", (username_input, )).fetchone()

        if not result:
            self.error()
            return
        
        if password_input == result[2]:
            root.show_frame(Admin)
            return
        
        self.error()


    def acc_register(self):
        root.show_frame(Register)




class Register(tk.Frame):
    def __init__(self, parent, root: tk.Tk):
        super().__init__(parent)

        login_frame = tk.Frame(self, width=400, height=550, bg="cyan", borderwidth=5, relief="ridge")
        login_frame.pack_propagate(False)
        login_frame.pack(expand=True)

        entry_frame = tk.Frame(login_frame, bg="purple")
        entry_frame.place(anchor="center", rely=0.375, relx=0.5)

        username_frame = tk.Frame(entry_frame, bg="red")
        username_frame.pack(expand=True, pady=10)

        self.username_label = tk.Label(username_frame, text="Username")
        self.username_label.grid(row=0, column=0, sticky="w")

        self.username_ent = tk.Entry(username_frame, width=30, highlightbackground="black", highlightcolor="black", highlightthickness=2, relief="flat")
        self.username_ent.grid(row=1, column=0)

        password_frame = tk.Frame(entry_frame, bg="blue")
        password_frame.pack(expand=True, pady=10)

        self.password_label = tk.Label(password_frame, text="Password")
        self.password_label.grid(row=0, column=0, sticky="w")

        self.password_ent = tk.Entry(password_frame, width=30, show="•", highlightbackground="black", highlightcolor="black", highlightthickness=2, relief="flat")
        self.password_ent.grid(row=1, column=0)

        confirm_password_frame = tk.Frame(entry_frame, bg="blue")
        confirm_password_frame.pack(expand=True, pady=10)

        self.confirm_password_label = tk.Label(confirm_password_frame, text="Confirm Password")
        self.confirm_password_label.grid(row=0, column=0, sticky="w")

        self.confirm_password_ent = tk.Entry(confirm_password_frame, width=30, show="•", highlightbackground="black", highlightcolor="black", highlightthickness=2, relief="flat")
        self.confirm_password_ent.grid(row=1, column=0)
        
        self.password_hidden = tk.IntVar()
        self.password_hidden.set(1)

        self.style = ttk.Style()
        self.style.configure("Register.TCheckbutton", font=("Arial", 10))

        show_password_cb = ttk.Checkbutton(confirm_password_frame, variable=self.password_hidden, onvalue=0, offvalue=1, command=self.password_show_hide, text="Show Password", style="Register.TCheckbutton")
        show_password_cb.grid(row=2, column=0, sticky="nw")

        self.error_label = tk.Label(confirm_password_frame, text="Username sudah ada!", fg="blue", bg="blue", font=("Arial", 10))
        self.error_label.grid(row=3, column=0)


        tk.Button(login_frame, text="Register", command=self.acc_register).place(anchor="center", relx=0.5, rely=0.77)
        tk.Label(login_frame, text="Or").place(anchor="center", relx=0.5, rely=0.85)
        tk.Button(login_frame, text="Login", command=self.login).place(anchor="center", relx=0.5, rely=0.93)
    

    def password_show_hide(self):
        if bool(self.password_hidden.get()):
            self.password_ent.config(show="•")
            self.confirm_password_ent.config(show="•")
        else:
            self.password_ent.config(show="")
            self.confirm_password_ent.config(show="")
    
    
    def unerror(self):
        self.username_label.config(fg="black")
        self.password_label.config(fg="black")
        self.confirm_password_label.config(fg="black")
        self.username_ent.config(highlightbackground="black", highlightcolor="black", bg="white", state="disabled")
        self.password_ent.config(highlightbackground="black", highlightcolor="black", bg="white", state="disabled")
        self.confirm_password_ent.config(highlightbackground="black", highlightcolor="black", bg="white", state="disabled")
        self.error_label.config(fg="blue")
        self.style.configure("Register.TCheckbutton", foreground="black")
        root.update()
        sleep(0.5)

    
    def error(self, text: str, emptify = True):
        self.username_label.config(fg="red")
        self.password_label.config(fg="red")
        self.confirm_password_label.config(fg="red")
        self.password_ent.config(highlightbackground="red", highlightcolor="red", bg="#ffa3a3", state="normal")
        self.username_ent.config(highlightbackground="red", highlightcolor="red", bg="#ffa3a3", state="normal")
        self.confirm_password_ent.config(highlightbackground="red", highlightcolor="red", bg="#ffa3a3", state="normal")
        self.error_label.config(fg="red", text=text)
        self.style.configure("Register.TCheckbutton", foreground="red")

        if emptify:
            self.username_ent.delete(0, tk.END)
            self.password_ent.delete(0, tk.END)
            self.confirm_password_ent.delete(0, tk.END)


    def arise(self, root: tk.Tk):
        self.tkraise()
        root.geometry("800x600")


    
    def login(self):
        root.show_frame(Login)


    def acc_register(self):
        username = self.username_ent.get()
        password = self.password_ent.get()
        confirm_password = self.confirm_password_ent.get()

        self.unerror()

        if username == "" or password == "" or confirm_password == "":
            self.error("Jangan ada field yang kosong!", False)
            return

        if username.find(" ") >= 0:
            self.error("Username tidak boleh ada spasi!")
            return

        if not confirm_password == password:
            self.error("Ketik ulang password yang benar!")
            return

        if len(password) < 8:
            self.error("Password minimal 8 karakter!")
            return
        
        result = cursor.execute("SELECT * FROM user WHERE username=?", (username, )).fetchall()

        if result:
            self.error("Nama sudah ada!")
            return
        
        cursor.execute(
            "INSERT INTO user (username, password, status) VALUES (?, ?, ?)",
            (username, confirm_password, 0)
        )
        
        conn.commit()

        root.show_frame(Login) 
        

class Admin(tk.Frame):
    def __init__(self, parent, root: tk.Tk):
        super().__init__(parent)
        
        data_border_frame = tk.LabelFrame(self, background="cyan", height=750, width=1200, text="Inventaris", font=("Arial", 24))
        data_border_frame.pack_propagate(False)
        data_border_frame.place(anchor="center", relx=0.5, rely=0.45)

        self.edit_btn = tk.Button(self, text="Edit", width=6)
        self.edit_btn.place(anchor="se", x=1240, y=860, height=35)

        content_container = tk.Frame(data_border_frame, background="lime", height=680, width=1150)
        content_container.pack_propagate(False)
        content_container.pack(expand=True)

        data_canvas_container = tk.Frame(content_container, bg="green")
        data_canvas_container.pack(side="left", fill="both", expand=True)

        self.data_canvas = tk.Canvas(data_canvas_container, bg="blue", highlightthickness=0)
        self.data_canvas.pack(side="bottom", fill="both", expand=True)

        data_scrollbar = tk.Scrollbar(content_container, orient="vertical", command=self.data_canvas.yview, bg="pink")
        data_scrollbar.pack(side="right", fill="y")

        self.data_canvas.config(yscrollcommand=data_scrollbar.set)
        self.data_canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        self.data_frame = tk.Frame(self.data_canvas, bg="lime")
        self.data_frame.pack(fill="both", expand=True)
        self.data_frame.bind(
            "<Configure>",
            lambda e: self.data_canvas.config(scrollregion=self.data_canvas.bbox("all"))
        )
        
        self.data_canvas.create_window((0, 0), window=self.data_frame, anchor="nw")

        self.loaded_record: list[tk.Frame] = []
        self.added_record: list[tk.Frame] = []
        self.delete_request_record_id: list[int] = []

        Record(data_canvas_container, [0, "Nama Barang", "Jumlah", "Kondisi", "Lokasi"], "#834646").pack(side="top", anchor="nw")

    
    def clear_record(self):
        for r in self.loaded_record:
            r.destroy()
        
        self.loaded_record.clear()

        for r in self.added_record:
            r.destroy()

        self.added_record.clear()
    

    def load_record(self):
        self.clear_record()
        
        result = cursor.execute("SELECT * FROM barang").fetchall()

        for d in result:
            EditableRecord(self.data_frame, d, "#ff7979").pack()
            MyHSeparator(self.data_frame, "lime", 1).pack(fill="x", expand=True)

    

    def arise(self, root: tk.Tk):
        self.tkraise()
        root.geometry("1280x900")
        root.geometry(f"+{max(0, root.winfo_x() - 240)}+{max(0, root.winfo_y() - 150)}")

        self.load_record()
    
    
    def on_mouse_wheel(self, e: tk.Event):
        canvas_height = self.data_canvas.winfo_height()
        content_height = self.data_canvas.bbox("all")[3]

        if canvas_height < content_height:
            self.data_canvas.yview_scroll(int(-1*(e.delta/120)), "units")


class MyHSeparator(tk.Frame):
    def __init__(self, master: tk.Misc, color: str, thickness: int):
        super().__init__(master, background=color, height=thickness)


class Record(tk.Frame):
    def __init__(self, master: tk.Misc, data: list, color: str):
        super().__init__(master, bg="purple", width=1135, height=42)
        self.grid_propagate(False)

        self.data_id = data[0]
        
        nama_frame = tk.Frame(self, bg=color, width=int((weight_nama/weight_sum) * 1135), height=60)
        nama_frame.pack(side="left")
        nama_frame.pack_propagate(False)

        jumlah_frame = tk.Frame(self, bg=color, width=int((weight_jumlah/weight_sum) * 1135), height=60)
        jumlah_frame.pack(side="left")
        jumlah_frame.pack_propagate(False)

        kondisi_frame = tk.Frame(self, bg=color, width=int((weight_kondisi/weight_sum) * 1135), height=60)
        kondisi_frame.pack(side="left")
        kondisi_frame.pack_propagate(False)

        lokasi_frame = tk.Frame(self, bg=color, width=int((weight_lokasi/weight_sum) * 1135), height=60)
        lokasi_frame.pack(side="left")
        lokasi_frame.pack_propagate(False)


        nama_label = tk.Label(nama_frame, text=data[1], bg="red", font=("Arial", 20))
        nama_label.pack(anchor="w", padx=5,expand=True)

        jumlah_label = tk.Label(jumlah_frame, text=data[2], bg="red", font=("Arial", 20))
        jumlah_label.pack(anchor="w", padx=5,expand=True)

        kondisi_label = tk.Label(kondisi_frame, text=data[3], bg="red", font=("Arial", 20))
        kondisi_label.pack(anchor="w", padx=5,expand=True)

        lokasi_label = tk.Label(lokasi_frame, text=data[4], bg="red", font=("Arial", 20))
        lokasi_label.pack(anchor="w", padx=5,expand=True)


class EditableRecord(tk.Frame):
    def __init__(self, master: tk.Misc, data: list, color: str):
        super().__init__(master, bg="purple", width=1135, height=42)
        self.grid_propagate(False)

        self.data_id = data[0]
        
        nama_frame = tk.Frame(self, bg=color, width=int((weight_nama/weight_sum) * 1135), height=60)
        nama_frame.pack(side="left")
        nama_frame.pack_propagate(False)

        jumlah_frame = tk.Frame(self, bg=color, width=int((weight_jumlah/weight_sum) * 1135), height=60)
        jumlah_frame.pack(side="left")
        jumlah_frame.pack_propagate(False)

        kondisi_frame = tk.Frame(self, bg=color, width=int((weight_kondisi/weight_sum) * 1135), height=60)
        kondisi_frame.pack(side="left")
        kondisi_frame.pack_propagate(False)

        lokasi_frame = tk.Frame(self, bg=color, width=int((weight_lokasi/weight_sum) * 1135), height=60)
        lokasi_frame.pack(side="left")
        lokasi_frame.pack_propagate(False)

        self.kondisi_str = tk.StringVar()
        self.lokasi_str = tk.StringVar()

        kondisi_opts = ["Baik", "Rusak"]
        kondisi_selected = tk.StringVar(value=data[3])

        lokasi_opts = ["Di kelas", "Dipinjam"]
        lokasi_selected = tk.StringVar(value=data[4])

        nama_ent = tk.Entry(nama_frame, bg="red", font=("Arial", 20))
        nama_ent.pack(anchor="w", padx=5,expand=True)

        nama_ent.insert(0, data[1])

        self.jumlah = tk.IntVar(value=data[2])

        jumlah_spinb = tk.Spinbox(jumlah_frame, bg="red", font=("Arial", 20), textvariable=self.jumlah)
        jumlah_spinb.pack(anchor="w", padx=5,expand=True)

        kondisi_dd = tk.OptionMenu(kondisi_frame, kondisi_selected, *kondisi_opts)
        kondisi_dd.pack(anchor="w", padx=5,expand=True)

        lokasi_dd = tk.OptionMenu(lokasi_frame, lokasi_selected, *lokasi_opts)
        lokasi_dd.pack(anchor="w", padx=5,expand=True)


if __name__ == "__main__":
    root = Root()
    root.mainloop()