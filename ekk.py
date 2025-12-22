import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog as flpp 
import os
from app.file import pilih_file

class app(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)
     

class box(app):
    def __init__(self):
        super().__init__()

        self.geometry("500x600") 
        self.title("File Converter") 
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")


        self.labelformat = ctk.CTkLabel(self, text="Pilih File Yang Akan Dikonverter", font=("Monospace", 18,"bold"))
        self.labelformat.pack(pady=(50, 10))
        
        self.drop_bg = ctk.CTkFrame(self, width=400, height=150, corner_radius=10, border_width=2, border_color="#3B8ED0")
        self.drop_bg.pack(pady=(20), padx=10)
        self.drop_label = ctk.CTkLabel(self.drop_bg, text="Taruh file di sini", font=("Monospace", 20))
        self.drop_label.place(relx=0.5, rely=0.5, anchor="center")

        frame_input = ctk.CTkFrame(self, fg_color="transparent")
        frame_input.pack(pady=10)
        
        self.input = ctk.CTkEntry(frame_input, width=300, height=40, placeholder_text="File Input", font=("Monospace", 16))
        self.input.grid(row=0, column=0)
        
        self.btn_file = ctk.CTkButton(frame_input, width=70, height=40, text="Cari", command=self.file_pil)
        self.btn_file.grid(row=0, column=1, padx=(10, 0))

 
        self.label_format = ctk.CTkLabel(self, text="Pilih Format Tujuan:", font=("Monospace", 12))
        self.label_format.pack(pady=(10, 0))
        
        self.format_options = ["PDF", "DOCX", "JPG", "PNG", "ODT"]
        self.dropdown_format = ctk.CTkOptionMenu(self, values=self.format_options)
        self.dropdown_format.pack(pady=5)

        frame_output = ctk.CTkFrame(self, fg_color="transparent")
        frame_output.pack(pady=20)

        self.entry_output = ctk.CTkEntry(frame_output, width=300, height=40, placeholder_text="Lokasi Simpan", font=("Monospace", 16))
        self.entry_output.grid(row=0, column=0)

        self.btn_dest = ctk.CTkButton(frame_output, width=70, height=40, text="Simpan", command=self.tentukan_tujuan)
        self.btn_dest.grid(row=0, column=1, padx=(10, 0))

        self.btn_convert = ctk.CTkButton(self, text="MULAI KONVERSI", width=380, height=50, 
                                         fg_color="#10b981", hover_color="#059669", font=("Monospace", 18, "bold"),
                                         command=self.mulai_konversi)
        self.btn_convert.pack(pady=20)

        self.drop_bg.drop_target_register(DND_FILES)
        self.drop_bg.dnd_bind('<<Drop>>', self.file_hasil)

    def file_pil(self):
        path_file = pilih_file()
        if path_file:
            self.isi_input_output(path_file)

    def file_hasil(self, event):
        path_file = event.data.strip('{}') 
        self.isi_input_output(path_file)

    def isi_input_output(self, path):
        self.input.delete(0, "end")
        self.input.insert(0, path)

        nama_file = os.path.basename(path)
        self.drop_label.configure(text=f"File: {nama_file}", text_color="#10b981")
        
        nama_dasar = os.path.splitext(path)[0]
        ext_baru = self.dropdown_format.get().lower()
        self.entry_output.delete(0, "end")
        self.entry_output.insert(0, f"{nama_dasar}.{ext_baru}")

    def tentukan_tujuan(self):
        
        ext = self.dropdown_format.get().lower()
        path_tujuan = flpp.asksaveasfilename(
            defaultextension=f".{ext}",
            filetypes=[(f"{ext.upper()} file", f"*.{ext}"), ("All files", "*.*")]
        )
        if path_tujuan:
            self.entry_output.delete(0, "end")
            self.entry_output.insert(0, path_tujuan)

    def mulai_konversi(self):
        file_asal = self.input.get()
        file_tujuan = self.entry_output.get()
            
        print(f"Mengonversi {file_asal} ke {file_tujuan}...")

if __name__ == "__main__":
    app = box()
    app.mainloop()