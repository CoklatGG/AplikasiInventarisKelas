import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk 
from tkinter import filedialog
import sqlite3
import csv
from time import sleep
from re import sub

conn = sqlite3.connect("inventaris.db")
cursor = conn.cursor()

weight_nama = 90
weight_jumlah = 35
weight_kondisi = 50
weight_lokasi = 50
weight_sum = (weight_nama + weight_jumlah + weight_kondisi + weight_lokasi)

# COLOR PALLETE BIAR GAMPANG

color_text = "#466980"
color_text_secondary_btn_activated = "#698AA0"
color_text_disabled = "#64727A"
color_white_text_disabled = "#b4b4b4" 
color_bg_0 = "#fbfdff"
color_bg_1 = "#eff6fc"
color_bg_2 = "#d2eefc"
color_bg_3 = "#aad7fa"
color_primary_btn_normal = "#5fbee9"
color_primary_btn_activated = "#8dc7e2"
color_secondary_btn_normal = "#eef8fd"
color_secondary_btn_activated = "#f4fbff"
color_outline = "#599BDE"
color_record_bg = "#a3e2ff"

style_primary_btn = {
    "relief" : "flat",
    "foreground" : "white",
    "background" : color_primary_btn_normal,
    "activebackground" : color_primary_btn_activated,
    "activeforeground" : "white",
    "borderwidth" : 0
}

style_secondary_btn = {
    "relief" : "flat",
    "fg" : color_text, 
    "bg" : color_secondary_btn_normal, 
    "activebackground" : color_secondary_btn_activated, 
    "activeforeground" : color_text_secondary_btn_activated,
    "borderwidth" : 0
}

style_plus_btn = {
    "relief" : "flat",
    "fg" : "#e5ffe5", 
    "bg" : "#00ff00", 
    "activebackground" : "#70ff70", 
    "activeforeground" : "#ffffff",
    "borderwidth" : 0
}

style_trash_btn = {
    "relief" : "flat", 
    "bg" : "#ff0000", 
    "activebackground" : "#ff4646",
    "borderwidth" : 0
}

style_entry = {
    "highlightbackground" : color_text, 
    "highlightcolor" : color_text, 
    "highlightthickness" : 2, 
    "relief" : "flat", 
    "fg" : color_text, 
    "bg" : color_bg_1
}


class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Inventaris Kelas")
        self.geometry("800x600")
        self.resizable(False, False)

        self.iconbitmap("res/crep.ico")

        self.option_add("*Button.cursor", "hand2")
        self.option_add("*Checkbutton.cursor", "hand2")
        self.option_add("*TCheckbutton.cursor", "hand2")
        self.option_add("*Frame.background", color_bg_3)
        self.option_add("*Label.font", ("Times New Roman", 16))
        self.option_add("*Button.font", ("Times New Roman", 16))
        self.option_add("*Entry.font", ("Times New Roman", 16))
        self.option_add("*TCombobox.font", ("Times New Roman", 16))
        self.option_add("*TCombobox*Listbox.font", ("Times New Roman", 16))
        self.option_add("*TCombobox*Listbox.background", color_bg_1)
        self.option_add("*TCombobox*Listbox.foreground", color_text)
        self.option_add("*TCombobox*Listbox.selectBackground", color_bg_0)
        self.option_add("*TCombobox*Listbox.selectForeground", color_text)
        self.option_add("*TCombobox*Listbox.cursor", "hand2")

        default_font = tkfont.nametofont(name="TkDefaultFont")
        default_font.config(size=14)
        default_font = tkfont.nametofont(name="TkTextFont")
        default_font.config(size=14)

        container: tk.Frame = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Login, Register, Admin, User):
            frame: tk.Frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Login)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.arise(self)


class Login(tk.Frame):
    def __init__(self, parent, root: Root):
        super().__init__(parent)

        login_frame = tk.Frame(self, width=400, height=550, bg=color_bg_2, borderwidth=5, relief="ridge")
        login_frame.pack_propagate(False)
        login_frame.pack(expand=True)

        self.img = tk.PhotoImage(file="res/user.png")
        
        tk.Label(login_frame, image=self.img, bg=color_bg_2).place(anchor="center", relx=0.5, y=100)  

        entry_frame = tk.Frame(login_frame, bg=color_bg_2)
        entry_frame.place(anchor="center", rely=0.51, relx=0.5)

        username_frame = tk.Frame(entry_frame, bg=color_bg_2)
        username_frame.pack(expand=True, pady=10)

        self.username_label = tk.Label(username_frame, text="Username", bg=color_bg_2, fg=color_text)
        self.username_label.grid(row=0, column=0, sticky="w")

        self.username_ent = tk.Entry(username_frame, width=30, **style_entry)
        self.username_ent.grid(row=1, column=0)

        password_frame = tk.Frame(entry_frame, bg=color_bg_2)
        password_frame.pack(expand=True, pady=10)

        self.password_label = tk.Label(password_frame, text="Password", bg=color_bg_2, fg=color_text)
        self.password_label.grid(row=0, column=0, sticky="w")

        self.password_ent = tk.Entry(password_frame, width=30, show="•", **style_entry)
        self.password_ent.grid(row=1, column=0)

        self.password_hidden = tk.IntVar()
        self.password_hidden.set(1)
        
        self.style = ttk.Style()
        self.style.configure("Login.TCheckbutton", font=("Times New Roman", 10), background=color_bg_2, foreground=color_text)

        show_password_cb = ttk.Checkbutton(password_frame, variable=self.password_hidden, onvalue=0, offvalue=1, command=self.password_show_hide, text="Show Password", style="Login.TCheckbutton")
        show_password_cb.grid(row=2, column=0, sticky="nw")

        self.error_label = tk.Label(password_frame, text="Username atau Password salah!", fg=color_bg_2, bg=color_bg_2, font=("Times New Roman", 10))
        self.error_label.grid(row=3, column=0)

        tk.Button(login_frame, text="Login", command=self.login, **style_primary_btn, width=8).place(anchor="center", relx=0.5, rely=0.77)
        tk.Label(login_frame, text="Or", fg=color_text, bg=color_bg_2).place(anchor="center", relx=0.5, rely=0.85)
        tk.Button(login_frame, text="Register", command=self.acc_register, **style_secondary_btn, width=8).place(anchor="center", relx=0.5, rely=0.93)

    def arise(self, root: Root):
        self.tkraise()
        root.geometry("800x600")


    def unerror(self):
        self.username_label.config(fg=color_text)
        self.password_label.config(fg=color_text)
        self.username_ent.config(highlightbackground=color_text, highlightcolor=color_text, bg=color_bg_1, state="disabled", fg=color_text)
        self.password_ent.config(highlightbackground=color_text, highlightcolor=color_text, bg=color_bg_1, state="disabled", fg=color_text)
        self.error_label.config(fg=color_bg_2)
        self.style.configure("Login.TCheckbutton", foreground=color_text)
        root.update()
        sleep(0.5)

    
    def error(self):
        self.username_label.config(fg="red")
        self.password_label.config(fg="red")
        self.username_ent.config(highlightbackground="red", highlightcolor="red", bg="#ffe0e0", state="normal", fg="red")
        self.password_ent.config(highlightbackground="red", highlightcolor="red", bg="#ffe0e0", state="normal", fg="red")
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
        
        if not password_input == result[2]:
            return
        
        if result[3] == 0:
            root.show_frame(User)
            return

        root.show_frame(Admin)

        self.error()


    def acc_register(self):
        root.show_frame(Register)


class Register(tk.Frame):
    def __init__(self, parent, root: Root):
        super().__init__(parent)

        login_frame = tk.Frame(self, width=400, height=550, bg=color_bg_2, borderwidth=5, relief="ridge")
        login_frame.pack_propagate(False)
        login_frame.pack(expand=True)

        entry_frame = tk.Frame(login_frame, bg=color_bg_2)
        entry_frame.place(anchor="center", rely=0.375, relx=0.5)

        username_frame = tk.Frame(entry_frame, bg=color_bg_2)
        username_frame.pack(expand=True, pady=10)

        self.username_label = tk.Label(username_frame, text="Username", bg=color_bg_2, fg=color_text)
        self.username_label.grid(row=0, column=0, sticky="w")

        self.username_ent = tk.Entry(username_frame, width=30, **style_entry)
        self.username_ent.grid(row=1, column=0)

        password_frame = tk.Frame(entry_frame, bg=color_bg_2)
        password_frame.pack(expand=True, pady=10)

        self.password_label = tk.Label(password_frame, text="Password", bg=color_bg_2, fg=color_text)
        self.password_label.grid(row=0, column=0, sticky="w")

        self.password_ent = tk.Entry(password_frame, width=30, show="•", **style_entry)
        self.password_ent.grid(row=1, column=0)

        confirm_password_frame = tk.Frame(entry_frame, bg=color_bg_2)
        confirm_password_frame.pack(expand=True, pady=10)

        self.confirm_password_label = tk.Label(confirm_password_frame, text="Confirm Password", bg=color_bg_2, fg=color_text)
        self.confirm_password_label.grid(row=0, column=0, sticky="w")

        self.confirm_password_ent = tk.Entry(confirm_password_frame, width=30, show="•", **style_entry)
        self.confirm_password_ent.grid(row=1, column=0)
        
        self.password_hidden = tk.IntVar()
        self.password_hidden.set(1)

        self.style = ttk.Style()
        self.style.configure("Register.TCheckbutton", font=("Times New Roman", 10), background=color_bg_2, foreground=color_text)

        show_password_cb = ttk.Checkbutton(confirm_password_frame, variable=self.password_hidden, onvalue=0, offvalue=1, command=self.password_show_hide, text="Show Password", style="Register.TCheckbutton")
        show_password_cb.grid(row=2, column=0, sticky="nw")

        self.error_label = tk.Label(confirm_password_frame, text="Username sudah ada!", fg=color_bg_2, bg=color_bg_2, font=("Times New Roman", 10))
        self.error_label.grid(row=3, column=0)


        tk.Button(login_frame, text="Register", command=self.acc_register, **style_primary_btn, width=8).place(anchor="center", relx=0.5, rely=0.77)
        tk.Label(login_frame, text="Or", bg=color_bg_2, fg=color_text).place(anchor="center", relx=0.5, rely=0.85)
        tk.Button(login_frame, text="Login", command=self.login, **style_secondary_btn, width=8).place(anchor="center", relx=0.5, rely=0.93)
    

    def password_show_hide(self):
        if bool(self.password_hidden.get()):
            self.password_ent.config(show="•")
            self.confirm_password_ent.config(show="•")
        else:
            self.password_ent.config(show="")
            self.confirm_password_ent.config(show="")
    
    
    def unerror(self):
        self.username_label.config(fg=color_text)
        self.password_label.config(fg=color_text)
        self.confirm_password_label.config(fg=color_text)
        self.username_ent.config(highlightbackground=color_text, highlightcolor=color_text, bg=color_bg_2, state="disabled")
        self.password_ent.config(highlightbackground=color_text, highlightcolor=color_text, bg=color_bg_2, state="disabled")
        self.confirm_password_ent.config(highlightbackground=color_text, highlightcolor=color_text, bg=color_bg_2, state="disabled")
        self.error_label.config(fg=color_bg_2)
        self.style.configure("Register.TCheckbutton", foreground=color_text)
        root.update()
        sleep(0.5)

    
    def error(self, text: str, emptify = True):
        self.username_label.config(fg="red")
        self.password_label.config(fg="red")
        self.confirm_password_label.config(fg="red")
        self.password_ent.config(highlightbackground="red", highlightcolor="red", bg="#ffe0e0", fg="red", state="normal")
        self.username_ent.config(highlightbackground="red", highlightcolor="red", bg="#ffe0e0", fg="red", state="normal")
        self.confirm_password_ent.config(highlightbackground="red", highlightcolor="red", bg="#ffe0e0", fg="red", state="normal")
        self.error_label.config(fg="red", text=text)
        self.style.configure("Register.TCheckbutton", foreground="red")

        if emptify:
            self.username_ent.delete(0, tk.END)
            self.password_ent.delete(0, tk.END)
            self.confirm_password_ent.delete(0, tk.END)


    def arise(self, root: Root):
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
    def __init__(self, parent, root: Root):
        super().__init__(parent)
        
        table_height = 600

        self.root = root

        self.record_frame = tk.Frame()

        self.edit_mode = False

        data_border_frame = tk.LabelFrame(self, bg=color_bg_2, fg=color_text, height=750, width=1200, text="Inventaris (Admin)", font=("Times New Roman", 24), relief="flat")
        data_border_frame.pack_propagate(False)
        data_border_frame.place(anchor="center", relx=0.5, y=420)
        
        self.edit_btn = tk.Button(self, text="Edit", width=9, command=self.edit, **style_primary_btn)
        self.edit_btn.place(anchor="se", x=1240, y=860, height=35)

        self.apply_btn = tk.Button(self, text="Accept", width=9, bg="green", command=self.apply_changes, **style_primary_btn)

        self.export_btn = tk.Button(data_border_frame, text="Export", command=self.export, **style_primary_btn)
        self.export_btn.place(anchor="se", x=1173, y=692, width=75, height=30)

        self.sortby = tk.StringVar(value="Waktu dibuat")

        self.sortby.trace_add("write", self.load_record)

        sortby_frame = tk.Frame(data_border_frame, bg=color_bg_2)
        sortby_frame.place(anchor="ne", x=1173, y=10, width=370, height=30)

        self.sortby_label = tk.Label(sortby_frame, text="Urut berdasarkan : ", bg=color_bg_2, fg=color_text)
        self.sortby_label.place(anchor="nw", width=170, height=30, x=0)

        self.sort_dic = {
            "Nama": "nama_barang", 
            "Waktu dibuat": "id", 
            "Jumlah": "jumlah", 
            "Kondisi": "kondisi", 
            "Lokasi": "lokasi"
        }

        self.sortby_cb = ttk.Combobox(sortby_frame, textvariable=self.sortby, values=["Nama", "Waktu dibuat", "Jumlah", "Kondisi", "Lokasi"], state="readonly", cursor="hand2", background=color_bg_1)
        self.sortby_cb.place(anchor="nw", width=170, height=30, x=170)

        self.sortby_cb.unbind_class("TCombobox", "<MouseWheel>")

        self.ascending = True

        self.ascdesc_btn = tk.Button(sortby_frame, text="↑", command=self.change_order, **style_primary_btn)
        self.ascdesc_btn.place(anchor="nw", width=30, height=30, x=340)
        
        content_container = tk.Frame(data_border_frame, background=color_bg_1, height=table_height, width=1150)
        content_container.pack_propagate(False)
        content_container.place(anchor="center", relx=0.5, rely=0.49)

        data_canvas_container = tk.Frame(content_container, bg=color_bg_1)
        data_canvas_container.pack(side="left", fill="both", expand=True)

        self.data_canvas = tk.Canvas(data_canvas_container, bg=color_bg_1, highlightthickness=0)
        self.data_canvas.pack(side="bottom", fill="both", expand=True)

        data_scrollbar = tk.Scrollbar(content_container, orient="vertical", command=self.data_canvas.yview)
        data_scrollbar.pack(side="right", fill="y")

        self.data_canvas.config(yscrollcommand=data_scrollbar.set)
        self.data_canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        self.data_frame = tk.Frame(self.data_canvas, bg=color_bg_1)
        self.data_frame.pack(fill="both", expand=True)
        self.data_frame.bind(
            "<Configure>",
            lambda e: self.data_canvas.config(scrollregion=self.data_canvas.bbox("all"))
        )
        
        self.data_canvas.create_window((0, 0), window=self.data_frame, anchor="nw")

        self.loaded_record: list[EditableRecord] = []
        self.added_record: list[EditableRecord] = []
        self.delete_request_record_id: list[int] = []

        Record(data_canvas_container, [0, "Nama Barang", "Jumlah", "Kondisi", "Lokasi"], color_primary_btn_normal, "white", True).pack(side="top", anchor="nw")
    

    def change_order(self):
        if self.ascending:
            self.ascending = False
            self.ascdesc_btn.config(text="↓")
        else:
            self.ascending = True
            self.ascdesc_btn.config(text="↑")
        
        self.load_record()
    
    def clear_record(self):
        self.record_frame.destroy()
        self.loaded_record.clear()
        self.added_record.clear()
    

    def load_record(self, *args):
        self.clear_record()

        if self.ascending:
            cursor.execute(f"SELECT * FROM barang ORDER BY {self.sort_dic[self.sortby.get()]} ASC")
        else:
            cursor.execute(f"SELECT * FROM barang ORDER BY {self.sort_dic[self.sortby.get()]} DESC")
        
        result = cursor.fetchall()

        data_length = len(result)

        self.record_frame = tk.Frame(self.data_frame)
        self.record_frame.pack()

        for i in range(data_length):
            new_record_separator = MyHSeparator(self.record_frame, color_outline, 1)

            if self.edit_mode:
                new_record = EditableRecord(self.record_frame, result[i], color_record_bg, self, new_record_separator)
                new_record.pack()
                
                self.loaded_record.append(new_record)
            else:
                new_record = Record(self.record_frame, result[i], color_record_bg, color_text)
                new_record.pack()
            
            
            if i + 1 >= data_length:
                continue
            
            new_record_separator.pack(fill="x", expand=True)
        
        if not self.edit_mode:
            return

        self.plus_button_frame = tk.Frame(self.record_frame, width=1135, height=42)
        self.plus_button_frame.pack()

        plus_button = tk.Button(self.plus_button_frame, text="+", font=("Arial", 24), command=self.add_record, **style_plus_btn)
        plus_button.place(anchor="nw", width=1135, height=42)

    
    def edit(self):
        self.edit_mode = True

        self.edit_btn.config(text="Cancel", command=self.unedit, **style_secondary_btn)
        
        self.apply_btn.place(anchor="se", x=1240 - 20 - self.edit_btn.winfo_reqwidth(), y=860, height=35)
        
        self.ascdesc_btn.config(state="disabled")
        self.sortby_cb.config(state="disabled")
        self.sortby_label.config(state="disabled")
        self.export_btn.config(state="disabled")

        self.load_record()
    

    def unedit(self):
        self.edit_mode = False

        self.edit_btn.config(text="Edit", command=self.edit, **style_primary_btn)

        self.apply_btn.place_forget()

        self.sortby_label.config(state="normal")
        self.ascdesc_btn.config(state="normal")
        self.sortby_cb.config(state="readonly")
        self.export_btn.config(state="normal")

        self.load_record()


    def add_record(self):
        new_record_separator = MyHSeparator(self.record_frame, color_outline, 1)
        
        new_record = EditableRecord(self.record_frame, [-1, "Barang baru", 1, "Baik", "Di kelas"], "#ff7979", self, new_record_separator)

        self.plus_button_frame.pack_forget()

        last_separator = None
        
        if len(self.added_record) <= 0:
            if len(self.loaded_record) > 0:
                last_separator = self.loaded_record[len(self.loaded_record) - 1].separator
        else:
            last_separator = self.added_record[len(self.added_record) - 1].separator

        self.added_record.append(new_record)

        if not last_separator == None:
            last_separator.pack(fill="x", expand=True)

        new_record.pack()
        self.plus_button_frame.pack()
        

    def apply_changes(self):
        for d in self.loaded_record:
            if d.delete_requested:
                continue

            if d.not_changed():
                continue

            cursor.execute(
"""
UPDATE barang
SET nama_barang = ?, jumlah = ?, kondisi = ?, lokasi = ?
WHERE id = ?
""",
(
    d.nama_str.get(), 
    int(d.jumlah_str.get()), 
    d.kondisi_str.get(), 
    d.lokasi_str.get(), 
    d.data_id
)
            )

        for id in self.delete_request_record_id:
            cursor.execute("DELETE FROM barang WHERE id = ?", (id, ))
        
        for d in self.added_record:
            if d.delete_requested:
                continue

            cursor.execute(
"""
INSERT INTO barang (nama_barang, jumlah, kondisi, lokasi)
VALUES (?, ?, ?, ?)
""",
(
    d.nama_str.get(), 
    int(d.jumlah_str.get()), 
    d.kondisi_str.get(), 
    d.lokasi_str.get()
)
            )
        
        conn.commit()

        self.unedit()

    
    def arise(self, root: Root):
        self.tkraise()
        root.geometry("1280x900")
        root.geometry(f"+{max(0, root.winfo_x() - 240)}+{max(0, root.winfo_y() - 150)}")

        self.data_canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        self.load_record()
        
    
    def on_mouse_wheel(self, e: tk.Event):
        canvas_height = self.data_canvas.winfo_height()
        content_height = self.data_canvas.bbox("all")[3]

        if canvas_height < content_height:
            self.data_canvas.yview_scroll(int(-1*(e.delta/120)), "units")
    

    def reload_cb_opts(self):
        kondisi_opts = ["Baik", "Rusak"]
        cursor.execute("SELECT * FROM kondisi")

        for r in cursor.fetchall():
            kondisi_opts.append(r[1])
        
        lokasi_opts = ["Di kelas", "Dipinjam"]
        cursor.execute("SELECT * FROM lokasi")

        for r in cursor.fetchall():
            lokasi_opts.append(r[1])

        for r in self.loaded_record:
            if r.delete_requested:
                continue

            r.kondisi_dd.config(values=kondisi_opts)
            r.lokasi_dd.config(values=lokasi_opts)

        for r in self.added_record:
            if r.delete_requested:
                continue

            r.kondisi_dd.config(values=kondisi_opts)
            r.lokasi_dd.config(values=lokasi_opts)
    

    def export(self):
        file_path = filedialog.asksaveasfilename(
            initialdir=".",
            initialfile="data.csv",
            title="Export File As",
            defaultextension=".csv",
            filetypes=(("CSV files", "*.csv"), ),
            confirmoverwrite=True
        )

        if not file_path:
            return
        
        if self.ascending:
            cursor.execute(f"SELECT nama_barang, jumlah, kondisi, lokasi FROM barang ORDER BY {self.sort_dic[self.sortby.get()]} ASC")
        else:
            cursor.execute(f"SELECT nama_barang, jumlah, kondisi, lokasi FROM barang ORDER BY {self.sort_dic[self.sortby.get()]} DESC")

        data = cursor.fetchall()
        
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file, delimiter=";")

            header = ["Nama Barang", "Jumlah", "Kondisi", "Lokasi"]

            writer.writerow(header)
            writer.writerows(data)


class MyHSeparator(tk.Frame):
    def __init__(self, master: tk.Misc, color: str, thickness: int):
        super().__init__(master, background=color, height=thickness)


class MyVSeparator(tk.Frame):
    def __init__(self, master: tk.Misc, color: str, thickness: int):
        super().__init__(master, background=color, width=thickness)


class Record(tk.Frame):
    def __init__(self, master: tk.Misc, data: list, bg: str, fg: str, justify_center = False):
        super().__init__(master, bg=color_outline, width=1135, height=42)
        self.grid_propagate(False)

        self.data = data

        self.data_id = data[0]
        
        nama_frame = tk.Frame(self, bg=bg, width=int((weight_nama/weight_sum) * 1135) - 1, height=60)
        nama_frame.pack(side="left")
        nama_frame.pack_propagate(False)

        separator_1 = MyVSeparator(self, color_outline, 1)
        separator_1.pack(side="left")
        separator_1.pack_propagate(False)

        jumlah_frame = tk.Frame(self, bg=bg, width=int((weight_jumlah/weight_sum) * 1135) - 1, height=60)
        jumlah_frame.pack(side="left")
        jumlah_frame.pack_propagate(False)

        separator_2 = MyVSeparator(self, color_outline, 1)
        separator_2.pack(side="left")
        separator_2.pack_propagate(False)

        kondisi_frame = tk.Frame(self, bg=bg, width=int((weight_kondisi/weight_sum) * 1135) - 1, height=60)
        kondisi_frame.pack(side="left")
        kondisi_frame.pack_propagate(False)

        separator_2 = MyVSeparator(self, color_outline, 1)
        separator_2.pack(side="left")
        separator_2.pack_propagate(False)

        lokasi_frame = tk.Frame(self, bg=bg, width=int((weight_lokasi/weight_sum) * 1135), height=60)
        lokasi_frame.pack(side="left")
        lokasi_frame.pack_propagate(False)

        anchor = "w"

        if justify_center:
            anchor = "center"

        nama_label = tk.Label(nama_frame, text=data[1], bg=bg, font=("Times New Roman", 20), fg=fg)
        nama_label.pack(anchor=anchor, padx=5, expand=True)

        jumlah_label = tk.Label(jumlah_frame, text=data[2], bg=bg, font=("Times New Roman", 20), fg=fg)
        jumlah_label.pack(anchor=anchor, padx=5, expand=True)

        kondisi_label = tk.Label(kondisi_frame, text=data[3], bg=bg, font=("Times New Roman", 20), fg=fg)
        kondisi_label.pack(anchor=anchor, padx=5, expand=True)

        lokasi_label = tk.Label(lokasi_frame, text=data[4], bg=bg, font=("Times New Roman", 20), fg=fg)
        lokasi_label.pack(anchor=anchor, padx=5, expand=True)


class EditableRecord(tk.Frame):
    def __init__(self, master: tk.Misc, data: list, color: str, admin_control: Admin, separator: MyHSeparator):
        super().__init__(master, bg=color_outline, width=1135, height=42)
        self.grid_propagate(False)

        self.data_id = data[0]

        self.separator = separator

        self.admin_control = admin_control

        self.delete_requested = False

        nama_frame = tk.Frame(self, bg=color, width=int((weight_nama/weight_sum) * 1135) - 1, height=60)
        nama_frame.pack(side="left")
        nama_frame.pack_propagate(False)

        separator_1 = MyVSeparator(self, color_outline, 1)
        separator_1.pack(side="left")
        separator_1.pack_propagate(False)

        jumlah_frame = tk.Frame(self, bg=color, width=int((weight_jumlah/weight_sum) * 1135) - 1, height=60)
        jumlah_frame.pack(side="left")
        jumlah_frame.pack_propagate(False)

        separator_2 = MyVSeparator(self, color_outline, 1)
        separator_2.pack(side="left")
        separator_2.pack_propagate(False)

        kondisi_frame = tk.Frame(self, bg=color, width=int((weight_kondisi/weight_sum) * 1135) - 1, height=60)
        kondisi_frame.pack(side="left")
        kondisi_frame.pack_propagate(False)

        separator_3 = MyVSeparator(self, color_outline, 1)
        separator_3.pack(side="left")
        separator_3.pack_propagate(False)

        lokasi_frame = tk.Frame(self, bg=color, width=int((weight_lokasi/weight_sum) * 1135) - 1, height=60)
        lokasi_frame.pack(side="left")
        lokasi_frame.pack_propagate(False)

        self.previous_nama_str =  tk.StringVar(value=data[1])
        self.previous_jumlah_str = tk.StringVar(value=data[2])
        self.previous_kondisi_str = tk.StringVar(value=data[3])
        self.previous_lokasi_str = tk.StringVar(value=data[4])
        
        self.nama_str =  tk.StringVar(value=data[1])
        self.jumlah_str = tk.StringVar(value=data[2])
        self.kondisi_str = tk.StringVar(value=data[3])
        self.lokasi_str = tk.StringVar(value=data[4])

        kondisi_opts = ["Baik", "Rusak"]
        cursor.execute("SELECT * FROM kondisi")

        for r in cursor.fetchall():
            kondisi_opts.append(r[1])
        
        lokasi_opts = ["Di kelas", "Dipinjam"]
        cursor.execute("SELECT * FROM lokasi")

        for r in cursor.fetchall():
            lokasi_opts.append(r[1])

        self.sampah_img = tk.PhotoImage(file="res/garbage.png")

        delete_btn = tk.Button(nama_frame, font=("Times New Roman", 20), image=self.sampah_img, command=self.delete, **style_trash_btn)
        delete_btn.place(anchor="w", rely=0.5, x=5, width=35, height=35)

        nama_ent = tk.Entry(nama_frame, font=("Times New Roman", 20), textvariable=self.nama_str, **style_entry)
        nama_ent.place(anchor="w", rely=0.5, x=50, height=35, width=397)

        jumlah_spinb = tk.Spinbox(
            jumlah_frame,
            font=("Times New Roman", 20), 
            textvariable=self.jumlah_str, 
            from_=1, 
            to=999, 
            buttoncursor="hand2", 
            width=12,
            bg=color_bg_1,
            fg=color_text,
            buttonuprelief="flat",
            buttondownrelief="flat",
            buttonbackground=color_bg_2
        )
        jumlah_spinb.pack(anchor="w", padx=5, expand=True)

        jumlah_spinb.bind("<FocusOut>", self.spin_box_digitify)
        jumlah_spinb.bind("<Return>", self.oof)

        kondisi_cbtn_frame = tk.Frame(kondisi_frame, bg=color, height=30, width=245)
        kondisi_cbtn_frame.pack(anchor="w", padx=5, expand=True)

        self.kondisi_dd = ttk.Combobox(kondisi_cbtn_frame, values=kondisi_opts, textvariable=self.kondisi_str, cursor="hand2", state="readonly", font=("Times New Roman", 16))
        self.kondisi_dd.place(anchor="nw", x=0, y=0, height=30, width=211)

        kondisi_btn = tk.Button(kondisi_cbtn_frame, text="+", font=("Arial", 14, "bold"), command=self.summon_konwin, **style_plus_btn)
        kondisi_btn.place(anchor="ne", relx=1, rely=0, height=30, width=30)

        lokasi_cbtn_frame = tk.Frame(lokasi_frame, bg=color, height=30, width=245)
        lokasi_cbtn_frame.pack(anchor="w", padx=5, expand=True)
        
        self.lokasi_dd = ttk.Combobox(lokasi_cbtn_frame, values=lokasi_opts, textvariable=self.lokasi_str, cursor="hand2", state="readonly", font=("Times New Roman", 16))
        self.lokasi_dd.place(anchor="nw", x=0, y=0, height=30, width=211)
    
        lokasi_btn = tk.Button(lokasi_cbtn_frame, text="+", font=("Arial", 14, "bold"), command=self.summon_lokwin, **style_plus_btn)
        lokasi_btn.place(anchor="ne", relx=1, rely=0, height=30, width=30)


    def oof(self, e: tk.Event):
        self.master.focus_set()
    

    def spin_box_digitify(self, e):
        self.jumlah_str.set(sub(r'\D', '', self.jumlah_str.get()))

        if not str.isdigit(self.jumlah_str.get()):
            self.jumlah_str.set("1")
        
        self.jumlah_str.set(str(min(max(1, int(self.jumlah_str.get())), 999)))

    
    def delete(self):
        self.delete_requested = True

        self.separator.destroy()
        self.destroy()

        if self.data_id < 0:
            return

        self.admin_control.delete_request_record_id.append(self.data_id)

    def not_changed(self) -> bool:
        if not self.previous_nama_str.get() == self.nama_str:
            return False

        if not self.previous_jumlah_str.get() == self.jumlah_str:
            return False

        if not self.previous_kondisi_str.get() == self.kondisi_str:
            return False

        if not self.previous_lokasi_str.get() == self.lokasi_str:
            return False
        
        return True


    def summon_konwin(self):
        TinyWin(self.admin_control, self.admin_control, "Kondisi Custom", "kondisi")


    def summon_lokwin(self):
        TinyWin(self.admin_control, self.admin_control, "Lokasi Custom", "lokasi")


    
class TinyWin(tk.Toplevel):
    def __init__(self, master, admin_control: Admin, title: str, table: str):
        super().__init__(master, bg=color_bg_2)

        width = 350
        height = 400

        self.admin_control = admin_control

        self.table = table

        self.resizable(False, False)
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.geometry(f"+{max(0, root.winfo_x() + int((1280 - width) / 2))}+{max(0, root.winfo_y() + int((900 - height) / 2))}")
        self.transient(root)
        self.grab_set()        
        self.protocol("WM_DELETE_WINDOW", self.close)

        main_frame = tk.Frame(self, bg=color_bg_2)
        main_frame.pack(fill="both", expand=True)

        trecord_canvas_container = tk.Frame(main_frame, height=height, width=width-50, bg=color_bg_2)
        trecord_canvas_container.pack_propagate(False)
        trecord_canvas_container.place(anchor="nw")

        self.trecord_canvas = tk.Canvas(main_frame, bg=color_bg_2, highlightthickness=0)
        self.trecord_canvas.pack(fill="both", expand=True)

        data_scrollbar = tk.Scrollbar(main_frame, orient="vertical", bg=color_bg_2, command=self.trecord_canvas.yview)
        data_scrollbar.place(anchor="ne", relx=1, height=height)

        self.trecord_canvas.config(yscrollcommand=data_scrollbar.set)
        self.trecord_canvas.bind_all("<MouseWheel>", self.scroll)

        self.trecord_frame = tk.Frame(self.trecord_canvas, bg=color_bg_2)
        self.trecord_frame.pack(fill="both", expand=True)
        self.trecord_frame.bind(
            "<Configure>",
            lambda e: self.trecord_canvas.config(scrollregion=self.trecord_canvas.bbox("all"))
        )
        
        self.trecord_canvas.create_window((0, 0), window=self.trecord_frame, anchor="nw")

        self.loaded_record: list[TinyRecord] = []
        self.added_record: list[TinyRecord] = []
        self.delete_request_record_id: list[int] = []

        data_scrollbar.tkraise()

        btn_frame = tk.Frame(self, width=100, height=60, bg=color_bg_2, highlightbackground=color_text, highlightcolor=color_text, highlightthickness=2)
        btn_frame.place(anchor="center", rely=0.925, relx=0.5, height=60)
        btn_frame.place(anchor="center", rely=0.93, relx=0.5, height=60)

        tk.Button(btn_frame, text="Apply", command=self.apply_changes, **style_primary_btn).pack(padx=20, side="left")
        tk.Button(btn_frame, text="Cancel", command=self.close, **style_secondary_btn).pack(padx=20, side="right")

        self.load_record()

        root.wait_window(self)


    def load_record(self):
        tk.Frame(self.trecord_frame, height=5, bg=color_bg_2).pack()

        cursor.execute(f"SELECT * FROM {self.table}")

        result = cursor.fetchall()

        for d in result:
            new_record = TinyRecord(self.trecord_frame, d, self)
            new_record.pack()
                
            self.loaded_record.append(new_record)

        self.plus_button_frame = tk.Frame(self.trecord_frame, width=333, height=50, bg=color_bg_2)
        self.plus_button_frame.pack()

        plus_button = tk.Button(self.plus_button_frame, text="+", font=("Arial", 16), command=self.add_record, **style_plus_btn)
        plus_button.place(anchor="nw", x=10, y=5, width=25, height=25)


    def apply_changes(self):
        for d in self.loaded_record:
            if d.delete_requested:
                continue

            if d.not_changed():
                continue

            cursor.execute(
f"""
UPDATE {self.table}
SET teks = ?
WHERE id = ?
""",
(
    d.text.get(),
    d.data_id
)
            )

        for id in self.delete_request_record_id:
            cursor.execute(f"DELETE FROM {self.table} WHERE id = ?", (id, ))
        
        for d in self.added_record:
            if d.delete_requested:
                continue

            cursor.execute(
f"""
INSERT INTO {self.table} (teks)
VALUES (?)
""",
(
    d.text.get(),
)
            )
        
        conn.commit()

        self.admin_control.reload_cb_opts()

        self.close()


    def add_record(self):
        new_record = TinyRecord(self.trecord_frame, [-1, "Kondisi Baru"], self)

        self.plus_button_frame.pack_forget()

        self.added_record.append(new_record)

        new_record.pack()
        self.plus_button_frame.pack()


    def scroll(self, e: tk.Event):
        canvas_height = self.trecord_canvas.winfo_height()
        content_height = self.trecord_canvas.bbox("all")[3]

        if canvas_height < content_height:
            self.trecord_canvas.yview_scroll(int(-1*(e.delta/120)), "units")
    

    def close(self):
        self.destroy()

        self.admin_control.data_canvas.bind_all("<MouseWheel>", self.admin_control.on_mouse_wheel)


class TinyRecord(tk.Frame):
    def __init__(self, master, data: list, tw_control: TinyWin):
        super().__init__(master, width=336, height=50, bg=color_bg_2)

        self.data_id = data[0]

        self.delete_requested = False

        self.tw_control = tw_control

        self.previous_text = tk.StringVar(value=data[1])
        self.text = tk.StringVar(value=data[1])

        text_frame = tk.Frame(self, width=279, height=50, bg=color_bg_2)
        text_frame.pack_propagate(False)
        text_frame.place(anchor="w", x=10, rely=0.5)

        text_ent = tk.Entry(text_frame, textvariable=self.text, font=("Times New Roman", 24), **style_entry)
        text_ent.pack(expand=True)

        self.sampah_img = tk.PhotoImage(file="res/garbage15x20.png")

        trash_btn = tk.Button(self, image=self.sampah_img, command=self.delete, **style_trash_btn)
        trash_btn.place(anchor="e", x=326, rely=0.5, width=30, height=30)

    def delete(self):
        self.delete_requested = True

        self.destroy()

        if self.data_id < 0:
            return

        self.tw_control.delete_request_record_id.append(self.data_id)


    def not_changed(self) -> bool:
        return not self.previous_text.get() == self.text.get()


class User(tk.Frame):
    def __init__(self, parent, root: Root):
        super().__init__(parent)
        
        table_height = 650

        self.root = root

        self.record_frame = tk.Frame()


        self.door = tk.PhotoImage(file="res/logout25x25.png")

        tk.Button(
            self,
            relief="flat",
            command=self.logout,
            bg=color_bg_3,
            activebackground=color_bg_2,
            image=self.door,
            borderwidth=0
        ).place(anchor="ne", relx=0.995, rely=0.005, width=30, height=30)

        data_border_frame = tk.LabelFrame(self, background=color_bg_2, height=800, width=1200, text="Inventaris", font=("Times New Roman", 24), relief="flat")
        data_border_frame.pack_propagate(False)
        data_border_frame.place(anchor="center", relx=0.5, rely=0.5)

        export_btn = tk.Button(data_border_frame, bg="blue", text="Export", command=self.export, **style_primary_btn)
        export_btn.place(anchor="se", x=1173, y=742, width=75, height=30)

        self.sortby = tk.StringVar(value="Waktu dibuat")

        self.sortby.trace_add("write", self.load_record)

        sortby_frame = tk.Frame(data_border_frame, bg=color_bg_2)
        sortby_frame.place(anchor="ne", x=1173, width=370, height=30)

        self.sortby_label = tk.Label(sortby_frame, text="Urut berdasarkan : ", bg=color_bg_2)
        self.sortby_label.place(anchor="nw", width=170, height=30, x=0)

        self.sort_dic = {
            "Nama": "nama_barang", 
            "Waktu dibuat": "id", 
            "Jumlah": "jumlah", 
            "Kondisi": "kondisi", 
            "Lokasi": "lokasi"
        }
        
        self.sortby_cb = ttk.Combobox(sortby_frame, textvariable=self.sortby, values=["Nama", "Waktu dibuat", "Jumlah", "Kondisi", "Lokasi"], state="readonly", cursor="hand2")
        self.sortby_cb.place(anchor="nw", width=170, height=30, x=170)

        self.sortby_cb.unbind_class("TCombobox", "<MouseWheel>")

        self.ascending = True

        self.ascdesc_btn = tk.Button(sortby_frame, text="↑", command=self.change_order, **style_primary_btn)
        self.ascdesc_btn.place(anchor="nw", width=30, height=30, x=340)
        
        content_container = tk.Frame(data_border_frame, background="lime", height=table_height, width=1150, bg=color_bg_1)
        content_container.pack_propagate(False)
        content_container.place(anchor="center", relx=0.5, rely=0.49)

        data_canvas_container = tk.Frame(content_container, bg=color_bg_1)
        data_canvas_container.pack(side="left", fill="both", expand=True)

        self.data_canvas = tk.Canvas(data_canvas_container, bg=color_bg_1, highlightthickness=0)
        self.data_canvas.pack(side="bottom", fill="both", expand=True)

        data_scrollbar = tk.Scrollbar(content_container, orient="vertical", command=self.data_canvas.yview, bg=color_bg_1)
        data_scrollbar.pack(side="right", fill="y")

        self.data_canvas.config(yscrollcommand=data_scrollbar.set)
        self.data_canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        self.data_frame = tk.Frame(self.data_canvas, bg=color_bg_1)
        self.data_frame.pack(fill="both", expand=True)
        self.data_frame.bind(
            "<Configure>",
            lambda e: self.data_canvas.config(scrollregion=self.data_canvas.bbox("all"))
        )
        
        self.data_canvas.create_window((0, 0), window=self.data_frame, anchor="nw")

        self.loaded_record: list[Record] = []
        

        Record(data_canvas_container, [0, "Nama Barang", "Jumlah", "Kondisi", "Lokasi"], color_primary_btn_normal, "white").pack(side="top", anchor="nw")
    

    def logout(self):
        root.show_frame(Login)


    def change_order(self):
        if self.ascending:
            self.ascending = False
            self.ascdesc_btn.config(text="↓")
        else:
            self.ascending = True
            self.ascdesc_btn.config(text="↑")
        
        self.load_record()
    
    
    def clear_record(self):
        self.record_frame.destroy()
        self.loaded_record.clear()
    

    def load_record(self, *args):
        self.clear_record()

        if self.ascending:
            cursor.execute(f"SELECT * FROM barang ORDER BY {self.sort_dic[self.sortby.get()]} ASC")
        else:
            cursor.execute(f"SELECT * FROM barang ORDER BY {self.sort_dic[self.sortby.get()]} DESC")
        
        result = cursor.fetchall()

        data_length = len(result)

        self.record_frame = tk.Frame(self.data_frame, bg=color_bg_2)
        self.record_frame.pack()

        for i in range(data_length):
            new_record_separator = MyHSeparator(self.record_frame, color_outline, 1)

            new_record = Record(self.record_frame, result[i], color_record_bg, color_outline)
            new_record.pack()
            
            if i + 1 >= data_length:
                continue
            new_record_separator.pack(fill="x", expand=True)

    
    def arise(self, root: Root):
        self.tkraise()
        root.geometry("1280x900")
        root.geometry(f"+{max(0, root.winfo_x() - 240)}+{max(0, root.winfo_y() - 150)}")

        self.load_record()
        
    
    def on_mouse_wheel(self, e: tk.Event):
        canvas_height = self.data_canvas.winfo_height()
        content_height = self.data_canvas.bbox("all")[3]

        if canvas_height < content_height:
            self.data_canvas.yview_scroll(int(-1*(e.delta/120)), "units")
    

    def export(self):
        file_path = filedialog.asksaveasfilename(
            initialdir=".",
            initialfile="data.csv",
            title="Export File As",
            defaultextension=".csv",
            filetypes=(("CSV files", "*.csv"), ),
            confirmoverwrite=True
        )

        if not file_path:
            return
        
        if self.ascending:
            cursor.execute(f"SELECT nama_barang, jumlah, kondisi, lokasi FROM barang ORDER BY {self.sort_dic[self.sortby.get()]} ASC")
        else:
            cursor.execute(f"SELECT nama_barang, jumlah, kondisi, lokasi FROM barang ORDER BY {self.sort_dic[self.sortby.get()]} DESC")

        data = cursor.fetchall()
        
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file, delimiter=";")

            header = ["Nama Barang", "Jumlah", "Kondisi", "Lokasi"]

            writer.writerow(header)
            writer.writerows(data)



if __name__ == "__main__":
    root = Root()
    root.mainloop()