import os
import tkinter as tk
from tkinter import filedialog

def get_roblox_directory():
    return os.path.join(os.path.expanduser("~"), "AppData\\Local\\Temp\\Roblox\\http")

def get_discord_directory():
    return os.path.join(os.path.expanduser("~"), "AppData\\Roaming\\discord\\Cache\\Cache_Data")

def process_files(source_dir, destination_dir):
    status_label.config(text="Processing files...")
    root.update()
    for filename in os.listdir(source_dir):
        if any(filename.endswith(ext) for ext in [".ogg", ".png", ".gif", ".mp4", ".wav", ".webp", ".jpeg", ".webm", ".rbml", ".ktx"]):
            continue
        file_path = os.path.join(source_dir, filename)
        with open(file_path, 'rb') as file:
            content = file.read()
            oggs_index = content.find(b'OggS')
            png_index = content.find(b'\x89PNG')
            gif_index = content.find(b'GIF89a')
            mp4_index = content.find(b'ftyp')
            wav_index = content.find(b'RIFF')
            webp_index = content.find(b'WEBP')
            jpeg_index = content.find(b'\xFF\xD8\xFF')
            webm_marker = b'\x1A\x45\xDF\xA3\x01\x20\x1F\x42\xB4\x81\x01\x42\xF7\x81\x01\x42\xF2\x81\x04\x42\xF3\x81\x08\x42\x82\x84webmB'
            webm_index = content.find(webm_marker)
            rbml_index = content.find(b"<roblox!\xE2\x80\x8A\xCB\x99")
            ktx_index = content.find(b"\xABKTX 11\xBB")

            if oggs_index != -1:
                content = content[oggs_index:]
                new_filename = os.path.splitext(filename)[0] + ".ogg"
            elif png_index != -1:
                content = content[png_index:]
                new_filename = os.path.splitext(filename)[0] + ".png"
            elif gif_index != -1:
                content = content[gif_index:]
                new_filename = os.path.splitext(filename)[0] + ".gif"
            elif mp4_index != -1:
                content = content[mp4_index:]
                new_filename = os.path.splitext(filename)[0] + ".mp4"
            elif wav_index != -1:
                content = content[wav_index:]
                new_filename = os.path.splitext(filename)[0] + ".wav"
            elif webp_index != -1:
                content = content[webp_index:]
                new_filename = os.path.splitext(filename)[0] + ".webp"
            elif jpeg_index != -1:
                content = content[jpeg_index:]
                new_filename = os.path.splitext(filename)[0] + ".jpeg"
            elif webm_index != -1:
                content = content[webm_index:]
                new_filename = os.path.splitext(filename)[0] + ".webm"
            elif rbml_index != -1:
                content = content[rbml_index:]
                new_filename = os.path.splitext(filename)[0] + ".rbml"
            elif ktx_index != -1:
                content = content[ktx_index:]
                new_filename = os.path.splitext(filename)[0] + ".ktx"
            else:
                continue
        with open(os.path.join(destination_dir, new_filename), 'wb') as new_file:
            new_file.write(content)
    status_label.config(text="Files processed successfully.")
    root.update()

def clear_source_dir(source_dir):
    status_label.config(text="Clearing source directory...")
    root.update()
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        os.remove(file_path)
    status_label.config(text="Source directory cleared.")
    root.update()

def execute_script():
    source_dir = source_dir_entry.get()
    destination_dir = destination_dir_entry.get()
    process_files(source_dir, destination_dir)

def browse_destination_dir():
    destination_dir = filedialog.askdirectory()
    destination_dir_entry.delete(0, tk.END)
    destination_dir_entry.insert(0, destination_dir)

def set_source_to_roblox():
    source_dir_entry.delete(0, tk.END)
    source_dir_entry.insert(0, get_roblox_directory())

def set_source_to_discord():
    source_dir_entry.delete(0, tk.END)
    source_dir_entry.insert(0, get_discord_directory())

root = tk.Tk()
root.title("Cache Extractor")

root.tk_setPalette(background='#2B2B2B', foreground='white')

source_dir_label = tk.Label(root, text="Source Directory:")
source_dir_label.grid(row=0, column=0, padx=5, pady=5)
source_dir_entry = tk.Entry(root, width=50)
source_dir_entry.grid(row=0, column=1, padx=5, pady=5)

roblox_button = tk.Button(root, text="Roblox", command=set_source_to_roblox)
roblox_button.grid(row=0, column=2, padx=5, pady=5)
discord_button = tk.Button(root, text="Discord", command=set_source_to_discord)
discord_button.grid(row=0, column=3, padx=5, pady=5)

destination_dir_label = tk.Label(root, text="Destination Directory:")
destination_dir_label.grid(row=1, column=0, padx=5, pady=5)
destination_dir_entry = tk.Entry(root, width=50)
destination_dir_entry.grid(row=1, column=1, padx=5, pady=5)
destination_dir_button = tk.Button(root, text="Browse", command=browse_destination_dir)
destination_dir_button.grid(row=1, column=2, padx=5, pady=5)

execute_button = tk.Button(root, text="Execute", command=execute_script)
execute_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

clear_button = tk.Button(root, text="Clear Source Directory", command=lambda: clear_source_dir(source_dir_entry.get()))
clear_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

status_label = tk.Label(root, text="", background='#2B2B2B', foreground='white')
status_label.grid(row=4, column=0, columnspan=4, padx=5, pady=5)

root.mainloop()
