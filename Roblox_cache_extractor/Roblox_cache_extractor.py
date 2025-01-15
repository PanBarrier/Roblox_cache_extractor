import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import imageio

def get_roblox_directory():
    return os.path.join(os.path.expanduser("~"), "AppData\\Local\\Temp\\Roblox\\http")

def process_files(source_dir, destination_dir):
    status_label.config(text="Processing files...")
    root.update()
    for filename in os.listdir(source_dir):
        if any(filename.endswith(ext) for ext in [".ogg", ".png", ".mp4", ".wav", ".ktx"]):
            continue
        file_path = os.path.join(source_dir, filename)
        with open(file_path, 'rb') as file:
            content = file.read()
            oggs_index = content.find(b'OggS')
            png_index = content.find(b'\x89PNG')
            mp4_index = content.find(b'ftyp')
            wav_index = content.find(b'RIFF')
            ktx_index = content.find(b"\xABKTX 11\xBB")

            if oggs_index != -1:
                content = content[oggs_index:]
                new_filename = os.path.splitext(filename)[0] + ".ogg"
            elif png_index != -1:
                content = content[png_index:]
                new_filename = os.path.splitext(filename)[0] + ".png"
            elif mp4_index != -1:
                content = content[mp4_index:]
                new_filename = os.path.splitext(filename)[0] + ".mp4"
            elif wav_index != -1:
                content = content[wav_index:]
                new_filename = os.path.splitext(filename)[0] + ".wav"
            elif ktx_index != -1:
                content = content[ktx_index:]
                temp_ktx_file = os.path.join(destination_dir, os.path.splitext(filename)[0] + ".ktx")
                new_filename = os.path.splitext(filename)[0] + ".png"
                
                # Save KTX file temporarily
                with open(temp_ktx_file, 'wb') as temp_file:
                    temp_file.write(content)
                
                # Convert KTX to PNG
                try:
                    image = imageio.imread(temp_ktx_file, format="ktx")
                    png_file_path = os.path.join(destination_dir, new_filename)
                    Image.fromarray(image).save(png_file_path)
                    os.remove(temp_ktx_file)  # Remove the temporary KTX file
                except Exception as e:
                    status_label.config(text=f"Error converting KTX to PNG: {e}")
                    continue
                continue
            else:
                continue
        with open(os.path.join(destination_dir, new_filename), 'wb') as new_file:
            new_file.write(content)
    status_label.config(text="Files processed successfully.")
    root.update()

def clear_directory(directory):
    if not directory:
        status_label.config(text="Directory path is empty!")
        root.update()
        return
    status_label.config(text=f"Clearing {directory}...")
    root.update()
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            os.remove(file_path)
        status_label.config(text=f"Directory '{directory}' cleared.")
    except Exception as e:
        status_label.config(text=f"Error clearing directory: {e}")
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

root = tk.Tk()
root.title("Cache Extractor")

root.tk_setPalette(background='#2B2B2B', foreground='white')

source_dir_label = tk.Label(root, text="Source Directory:")
source_dir_label.grid(row=0, column=0, padx=5, pady=5)
source_dir_entry = tk.Entry(root, width=50)
source_dir_entry.grid(row=0, column=1, padx=5, pady=5)

roblox_button = tk.Button(root, text="Roblox", command=set_source_to_roblox)
roblox_button.grid(row=0, column=2, padx=5, pady=5)

destination_dir_label = tk.Label(root, text="Destination Directory:")
destination_dir_label.grid(row=1, column=0, padx=5, pady=5)
destination_dir_entry = tk.Entry(root, width=50)
destination_dir_entry.grid(row=1, column=1, padx=5, pady=5)
destination_dir_button = tk.Button(root, text="Browse", command=browse_destination_dir)
destination_dir_button.grid(row=1, column=2, padx=5, pady=5)

execute_button = tk.Button(root, text="Execute", command=execute_script)
execute_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

clear_source_button = tk.Button(root, text="Clear Source Directory", command=lambda: clear_directory(source_dir_entry.get()))
clear_source_button.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

clear_dest_button = tk.Button(root, text="Clear Destination Directory", command=lambda: clear_directory(destination_dir_entry.get()))
clear_dest_button.grid(row=2, column=2, columnspan=2, padx=5, pady=5)

status_label = tk.Label(root, text="", background='#2B2B2B', foreground='white')
status_label.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

footer_label = tk.Label(root, text="Made by PanBarrier  discord.gg/W7SsqwCUS2", fg="#00ff81", background='#2B2B2B')
footer_label.grid(row=4, column=0, columnspan=4, pady=10)

root.mainloop()
