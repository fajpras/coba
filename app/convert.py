from pdf2docx import Converter
from docx2pdf import convert
from pdf2image import convert_from_path
from PIL import Image
from tkinter import filedialog, messagebox
import os

def p2d(a,t):
    try:
        cv = Converter(a)
        cv.convert(t)
        cv.close()

        messagebox.showinfo(
                "Berhasil",
                f"File berhasil dikonversi:\n{t}"
            )
        return True
    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )
        return False


def d2p(a,t):
    try:

        convert(a, t)

        messagebox.showinfo(
            "Berhasil",
            f"File berhasil dikonversi:\n{t}"
        )
        return True
    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Gagal mengonversi file:\n{str(e)}"
        )
        return False

def p2img(a, t):
    try:
        pages = convert_from_path(a, dpi=200)
        cek_format = os.path.splitext(t)[1][1:].upper()
        if cek_format == 'JPG':
            cek_format = 'JPEG' 
        
    
        pages[0].save(t, cek_format)
        messagebox.showinfo(
                "Berhasil",
                f"File berhasil dikonversi:\n{t}"
            )
        return True
  

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Gagal mengonversi file:\n{str(e)}"
        )
        return False


def img2p(a,t):
    try:
        a = os.path.abspath(a)
        t = os.path.abspath(t)


        with Image.open(a) as image:
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
                
            image.save(t, "PDF", resolution=100.0)
        
        messagebox.showinfo("Berhasil", f"Foto berhasil diubah ke PDF:\n{t}")
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Gagal merubah foto ke PDF: {str(e)}")
        # return False