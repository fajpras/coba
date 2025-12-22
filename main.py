import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
import os

<<<<<<< HEAD
from app.file import pilih_file,file_out

          
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
        options = ["PDF", "DOCX", "JPG", "PNG", "ODT"]
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


        self.drop_bg.drop_target_register(DND_FILES)
        self.drop_bg.dnd_bind('<<Drop>>', self.file_hasil)

    def aksi_out(self):
        
        ext = self.dropdown.get().lower()
        path_file = file_out(ext)
        nama_file = os.path.basename(path_file) 
        self.entry_output.delete(0,"end")
        self.entry_output.insert(0,nama_file)
        print(path_file)
      
    def file_pil(self):
        path_file = pilih_file()
        self.input.delete(0,"end")
        self.input.insert(0,path_file)
        print(path_file)

    def file_hasil(self, event):  
        path_file = event.data.strip('{}') 
        nama_file = os.path.basename(path_file) 
        self.drop_label.configure(
            text=f"file {nama_file}", 
                text_color="#10b981"
            )
        self.input.delete(0,"end")
        self.input.insert(0,nama_file 
            )
        # return path_file
        print(path_file)

    def konversi(self):
        file_asal = self.input.get()
        file_tujuan = self.entry_output.get()
            
        print(f"Mengonversi {file_asal} ke {file_tujuan}...")
# run
if __name__ == "__main__":
    app = box()
    app.mainloop()
