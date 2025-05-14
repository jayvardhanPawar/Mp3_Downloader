import tkinter as tk
from tkinter import ttk, messagebox
import os
import re
import string
import subprocess
import yt_dlp

class MP3Downloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube MP3 Downloader (Jay)")
        self.root.geometry("500x300")

        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Search label and entry
        ttk.Label(main_frame, text="Enter Song Name or YouTube URL:").grid(row=0, column=0, sticky=tk.W)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(main_frame, textvariable=self.search_var, width=40)
        self.search_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        # Download button
        self.download_button = ttk.Button(main_frame, text="Download MP3", command=self.download_mp3)
        self.download_button.grid(row=1, column=1, padx=5, pady=5)

        # Status label
        self.status_label = ttk.Label(main_frame, text="")
        self.status_label.grid(row=2, column=0, columnspan=2, pady=10)

    def sanitize_filename(self, name):
        valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
        return ''.join(c for c in name if c in valid_chars)

    def download_mp3(self):
        query = self.search_var.get().strip()
        if not query:
            messagebox.showerror("Error", "Please enter a song name or YouTube URL")
            return

        self.status_label.config(text="Downloading...")
        self.root.update()

        # Specify ffmpeg location - update this path to where you installed ffmpeg
        ffmpeg_location = r"C:\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe"  # Update this path

        output_template = os.path.join("downloads", "%(title).100s.%(ext)s")
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'noplaylist': True,
            'quiet': True,
            'ffmpeg_location': ffmpeg_location,  # Add ffmpeg location
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        try:
            if not re.match(r'^https?://', query):
                query = f"ytsearch1:{query}"

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=True)
                title = info.get('title', 'Downloaded')
                self.status_label.config(text=f"Downloaded: {title}")
                messagebox.showinfo("Success", f"Downloaded: {title}")
        except Exception as e:
            self.status_label.config(text="Error occurred")
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    root = tk.Tk()
    app = MP3Downloader(root)
    root.mainloop()
