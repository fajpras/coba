import customtkinter as ctk
from tkinter import filedialog as flpp



def pilih_file():
    filetypes = [
        ("Dokumen PDF", "*.pdf"),
        ("Dokumen Word", "*.docx *.doc"),
        ("Dokumen ODT (Linux)", "*.odt"),
        ("Gambar (JPG/PNG)", "*.jpg *.jpeg *.png"),
        ("Semua File", "*.*")
    ]
    filename= flpp.askopenfilename(
        title='Pilih File',
        initialdir='/',
        filetypes=filetypes
    )
    return filename.strip('{}') 


def file_out(ext):
        
    path_tujuan = flpp.asksaveasfilename(
    defaultextension=f".{ext}",
    filetypes=[("All files", "*.*")]
        )
    return path_tujuan
 


