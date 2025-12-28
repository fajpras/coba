import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
from app.file import pilih_file,file_out
from tkinter import filedialog, messagebox

          
class app(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

class box(app):
    def __init__(self):
        super().__init__()

        # window
        self.geometry("500x600")
        self.title("file converter") 
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # rangka dnd
        self.drop_bg = ctk.CTkFrame(self, width=400, height=200,corner_radius=10,border_width=2,border_color="#3B8ED0")
        self.drop_bg.pack(pady=30,padx=10)

        # rangka label
        self.drop_label = ctk.CTkLabel(self.drop_bg,text="Taruh file di sini", font=("Monospace",20))
        self.drop_label.place(relx=0.5,rely=0.5,anchor="center")

        # jadi ini untuk atur grid input dan btn
        frame_input = ctk.CTkFrame(self,fg_color="transparent")
        frame_input.pack(pady=10)

        # input form
        self.input = ctk.CTkEntry(frame_input, width=300,height=40,border_width=1,border_color="#85BCEA",
        placeholder_text="file", font=("Monospace",16),corner_radius=5)
        self.input.grid(row=0, column=0)

        # button file
        self.btn_file = ctk.CTkButton(frame_input,width=70, height= 40,corner_radius=5,text="file", command=self.file_pil)
        self.btn_file.grid(row=0, column=1,padx=(20,0))


        # label pilih 
        self.label_convert =ctk.CTkLabel(self,width=200,height=30,text="Konversi ke", font=("monospace",16,"bold"))
        self.label_convert.pack(pady=10,padx=10,anchor="center")

        # file format option
        options = ["PDF", "DOCX", "JPG", "PNG"]
        self.dropdown = ctk.CTkOptionMenu(self,height=40,width=200, font=("monospace",20), values=options)
        self.dropdown.pack(pady=5,anchor="center")

        # frame output
        frame_output = ctk.CTkFrame(self, fg_color="transparent")
        frame_output.pack(pady=20)

        # entry
        self.entry_output = ctk.CTkEntry(frame_output, width=300, height=40, placeholder_text="Lokasi Simpan", font=("Monospace", 16))
        self.entry_output.grid(row=0, column=0)

        # btn lokasi F file_out
        self.btn_dest = ctk.CTkButton(frame_output, width=70, height=40, text="Simpan", command=self.aksi_out)
        self.btn_dest.grid(row=0, column=1, padx=(10, 0))

        # btn konvert convert F konversi
        self.btn_konversi = ctk.CTkButton(self,text="MULAI KONVERSI", width=300, height=50,  fg_color="#10b981", hover_color="#059669", font=("Monospace", 18, "bold"),command=self.konversi)
        self.btn_konversi.pack(padx=10,pady=10,anchor="center")

        # dnd file logic
        self.drop_bg.drop_target_register(DND_FILES)
        self.drop_bg.dnd_bind('<<Drop>>', self.file_hasil)


   
    # guna fungsi ini untuk menentukan lokasi file output dimana 
    def aksi_out(self):
        ext = self.dropdown.get().lower()
        path_file = file_out(ext)
        self.entry_output.delete(0,"end")
        self.entry_output.insert(0,path_file)
        print(f"file akan di simpan di {path_file}")
        
    # fungsi yang berguna untuk membuka window baru untuk mencari filel
    # yang akan di konvert
    def file_pil(self):
        path_file = pilih_file()
        self.input.delete(0,"end")

        self.input.insert(0,path_file)
        self.cek_ext(path_file) 

    # fungsi untuk mengecek path file dan
    # menentukan tujuan konverter
    def cek_ext(self,path_file):
        ext = os.path.splitext(path_file)[1].lower()

        if ext == ".pdf":
            pilihan_baru = ["DOCX", "JPG", "PNG"]
            self.dropdown.configure(values=pilihan_baru)
            self.dropdown.set("DOCX")
        elif ext == ".docx":
            pilihan_baru = ["PDF"]
            self.dropdown.configure(values=pilihan_baru)
            self.dropdown.set("PDF")
        elif ext in [".jpg", ".jpeg", ".png"]:
            pilihan_baru = ["PDF"]
            self.dropdown.configure(values=pilihan_baru)
            self.dropdown.set("PDF")
        elif ext == ".txt":
            pilihan_baru = ["PDF"]
            self.dropdown.configure(values=pilihan_baru)
            self.dropdown.set("PDF")


    # fungsi untuk merubah penampilan bg
    def file_hasil(self,event):  
        path_file = event.data.strip('{}') 
        nama_file = os.path.basename(path_file) 
        self.drop_label.configure(
            text=f"file \n{nama_file}", 
                text_color="#10b981"
            )
        self.drop_bg.configure(border_color="#4ade80", fg_color="#14532d")

        self.input.delete(0,"end")
        self.input.insert(0,path_file)
        self.cek_ext(path_file)
        print(path_file)

    # btn konversi dan tempat pemanggilan fungsi converter
    # dari app.convert
    def konversi(self):
        file_asal = self.input.get()
        file_tujuan = self.entry_output.get()
        format = self.dropdown.get()

        ext = os.path.splitext(file_asal)[1].lower()

        # validasi jika form masih kosong
        if not file_asal or not file_tujuan:
            print("Pilih file terlebih dahulu!")
            return


        # PDF to DOCX
        if format == "DOCX":
            from app.convert import p2d
            ok = p2d(file_asal,file_tujuan)
        # PDF to IMG
        elif format in ["JPG", "PNG"]:
            from app.convert import p2img
            ok = p2img(file_asal,file_tujuan)

        elif format == "PDF":
            # IMG to PDF
            if ext in [".jpg", ".jpeg", ".png"]:
                from app.convert import img2p
                ok =img2p(file_asal, file_tujuan)

            # DOCX to PDF
            else:
                from app.convert import d2p
                ok = d2p(file_asal,file_tujuan)
        
        # untuk konfirmas jika file suksess
        if ok:
            print("Berhasil di konversi")
            self.reset_form()
        else:
            messagebox.showerror("Error", f"Gagal melakukan konvert: ")
            self.reset_form()

       
    # fungsi reset form jika sudah selesai
    def reset_form(self):
            self.input.delete(0,"end")
            self.input.insert(0,"Pilih file")
            self.entry_output.delete(0, "end")
            self.entry_output.insert(0, "Pilih lokasi penyimpanan")
            
            self.drop_label.configure(text="Taruh file di sini", text_color="white")
            self.drop_bg.configure(border_color="#3B8ED0", fg_color="transparent")
            
            pilihan_awal = ["PDF", "DOCX", "JPG", "PNG", "TXT"]
            self.dropdown.configure(values=pilihan_awal)
            self.dropdown.set("PDF")
 
# run
if __name__ == "__main__":
    app = box()
    app.mainloop()
