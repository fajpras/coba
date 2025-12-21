import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import filedialog, messagebox
import os
import threading
import time
from PIL import Image
import pypandoc
from pdf2docx import Converter

# --- KONFIGURASI TEMA ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

class App(Tk):
    def __init__(self):
        super().__init__()
        
        self.geometry("600x600")
        self.title("Modern File Converter")
        self.resizable(False, False)
        
        self.file_input_path = None # Variabel penyimpan path file

        # --- HEADER ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=(20, 10))
        ctk.CTkLabel(self.header_frame, text="File Converter Pro", font=("Roboto", 24, "bold")).pack()
        ctk.CTkLabel(self.header_frame, text="Drag & Drop file • Auto Detect Format", text_color="gray").pack()

        # --- DROP ZONE ---
        self.drop_frame = ctk.CTkFrame(self, width=500, height=200, fg_color="#1e1e1e", border_color="#3b3b3b", border_width=2, corner_radius=15)
        self.drop_frame.pack(pady=20)
        self.drop_frame.pack_propagate(False)

        self.icon_label = ctk.CTkLabel(self.drop_frame, text="☁️", font=("Arial", 60))
        self.icon_label.place(relx=0.5, rely=0.4, anchor="center")
        self.text_label = ctk.CTkLabel(self.drop_frame, text="Drop File Here", font=("Roboto", 16, "bold"), text_color="#a1a1aa")
        self.text_label.place(relx=0.5, rely=0.6, anchor="center")

        # Logic DND
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.saat_file_didrop)

        # --- OPSI KONVERSI ---
        self.options_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.options_frame.pack(fill="x", padx=50, pady=10)

        ctk.CTkLabel(self.options_frame, text="Konversi ke format:").pack(side="left", padx=10)
        
        self.format_var = ctk.StringVar(value="Pilih File Dulu")
        self.combo_format = ctk.CTkOptionMenu(self.options_frame, values=[], variable=self.format_var, state="disabled")
        self.combo_format.pack(side="left", padx=10)

        # --- TOMBOL AKSI ---
        self.btn_convert = ctk.CTkButton(self, text="MULAI KONVERSI", font=("Roboto", 14, "bold"), 
                                         height=45, fg_color="#2563eb", state="disabled",
                                         command=self.mulai_thread_konversi)
        self.btn_convert.pack(padx=50, pady=10, fill="x")

        # --- PROGRESS BAR ---
        self.progress_bar = ctk.CTkProgressBar(self, width=500, height=10)
        self.progress_bar.pack(pady=20)
        self.progress_bar.set(0) # 0%

        # --- STATUS LABEL ---
        self.status_label = ctk.CTkLabel(self, text="Siap...", text_color="gray")
        self.status_label.pack(pady=5)

    def saat_file_didrop(self, event):
        file_path = event.data
        if file_path.startswith('{') and file_path.endswith('}'): file_path = file_path[1:-1]
        
        self.file_input_path = file_path
        self.update_ui_file_terdeteksi(file_path)

    def update_ui_file_terdeteksi(self, file_path):
        nama_file = os.path.basename(file_path)
        ext = os.path.splitext(file_path)[1].lower()

        # Update Visual Dropzone
        self.drop_frame.configure(border_color="#4ade80", fg_color="#14532d")
        self.icon_label.configure(text="📄", text_color="#4ade80")
        self.text_label.configure(text=nama_file, text_color="white")
        
        # Logika Pintar: Tentukan opsi format berdasarkan input
        opsi_tujuan = []
        if ext in ['.jpg', '.jpeg', '.png', '.webp']:
            opsi_tujuan = ['PNG', 'JPG', 'PDF', 'ICO']
        elif ext == '.pdf':
            opsi_tujuan = ['DOCX']
        elif ext in ['.odt', '.docx']:
            opsi_tujuan = ['PDF', 'DOCX']
        
        # Update Dropdown
        if opsi_tujuan:
            self.combo_format.configure(values=opsi_tujuan, state="normal")
            self.combo_format.set(opsi_tujuan[0])
            self.btn_convert.configure(state="normal", fg_color="#2563eb") # Enable tombol
            self.status_label.configure(text=f"Terdeteksi {ext.upper()}. Silakan pilih format tujuan.", text_color="white")
        else:
            self.combo_format.configure(state="disabled")
            self.btn_convert.configure(state="disabled")
            self.status_label.configure(text="Format file belum didukung.", text_color="#ef4444")

    # --- LOGIKA THREADING (AGAR GUI TIDAK MACET) ---
    def mulai_thread_konversi(self):
        # Jalankan fungsi 'proses_konversi' di jalur (thread) terpisah
        threading.Thread(target=self.proses_konversi).start()

    def proses_konversi(self):
        # 1. Kunci UI agar user tidak spam klik
        self.btn_convert.configure(state="disabled", text="Memproses...")
        self.progress_bar.start() # Animasi loading jalan
        
        try:
            input_path = self.file_input_path
            target_ext = self.format_var.get().lower()
            file_name_no_ext = os.path.splitext(input_path)[0]
            output_path = f"{file_name_no_ext}_converted.{target_ext}"

            ext_asal = os.path.splitext(input_path)[1].lower()

            # --- LOGIKA INTI KONVERSI ---
            
            # KASUS 1: GAMBAR KE GAMBAR/PDF
            if ext_asal in ['.jpg', '.jpeg', '.png', '.webp', '.bmp']:
                img = Image.open(input_path)
                if target_ext == 'jpg':
                    img = img.convert("RGB") # Hapus transparansi
                    img.save(output_path, "JPEG")
                else:
                    img.save(output_path, target_ext.upper())

            # KASUS 2: PDF KE WORD
            elif ext_asal == '.pdf' and target_ext == 'docx':
                cv = Converter(input_path)
                cv.convert(output_path)
                cv.close()

            # KASUS 3: ODT/DOCX KE PDF/DOCX
            elif ext_asal in ['.odt', '.docx']:
                if target_ext == 'pdf':
                    # Gunakan LibreOffice (soffice) di Linux
                    import subprocess
                    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', input_path, '--outdir', os.path.dirname(input_path)], check=True)
                else:
                    # Gunakan Pandoc
                    pypandoc.convert_file(input_path, target_ext, outputfile=output_path)
            
            # Simulasi delay agar progress bar terlihat (opsional)
            time.sleep(1) 
            
            # Jika sukses
            self.after(0, lambda: self.selesai_konversi(True, output_path))

        except Exception as e:
            # Jika gagal
            self.after(0, lambda: self.selesai_konversi(False, str(e)))

    def selesai_konversi(self, sukses, pesan):
        self.progress_bar.stop()
        self.progress_bar.set(1) # Full 100%
        self.btn_convert.configure(state="normal", text="MULAI KONVERSI")
        
        if sukses:
            self.status_label.configure(text=f"Sukses! Disimpan: {os.path.basename(pesan)}", text_color="#4ade80")
            messagebox.showinfo("Berhasil", f"File berhasil dikonversi!\nLokasi: {pesan}")
        else:
            self.status_label.configure(text="Gagal!", text_color="red")
            messagebox.showerror("Error", f"Terjadi kesalahan:\n{pesan}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
    