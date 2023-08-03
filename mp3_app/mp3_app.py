import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from pytube import YouTube


class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 player Converter")
        self.root.resizable(False, False)

        self.create_widgets()
        self.apply_styles()

    def create_widgets(self):
        label = tk.Label(self.root, text="YouTube Downloader", font=("Helvetica", 24, "bold"), background="#212a54")
        label.pack(pady=5)

        file_frame = tk.Frame(self.root)
        file_frame.pack(padx=20, pady=5, fill="x")

        link_text = ScrolledText(self.root, wrap=tk.WORD, height=10, width=80, font=("Helvetica", 10),
                                 background="#494b54")
        link_text.pack(padx=20, pady=(0, 5))
        self.link_text = link_text
        self.link_text.config(state="disabled")

        self.link_entry = tk.Entry(self.root, width=80, bg="#7f828f")
        self.link_entry.pack(padx=20, pady=(0, 5))

        add_button = ttk.Button(self.root, text="Add Link", command=self.add_link)
        add_button.pack(padx=20, pady=(0, 5))

        delete_button = ttk.Button(self.root, text="Delete Links", command=self.delete_links)
        delete_button.pack(padx=20, pady=(0, 5))

        download_button = ttk.Button(self.root, text="Download Videos", command=self.download_videos)
        download_button.pack(padx=20, pady=(0, 5))

        self.output_text = ScrolledText(self.root, wrap=tk.WORD, height=10, width=40, font=("Ariel", 10),
                                        background="#494b54")
        self.output_text.pack(padx=20, pady=(0, 10))
        self.output_text.config(state="disabled")

    def load_links(self, file_path):
        with open(file_path, "r") as file:
            text = file.read()
            self.link_text.delete(1.0, tk.END)
            self.link_text.insert(tk.END, text)

    def save_links(self, file_path):
        with open(file_path, "w") as file:
            file.write(self.link_text.get(1.0, tk.END))

    def add_link(self):
        link = self.link_entry.get()
        if link:
            self.link_text.insert(tk.END, link + "\n")
            self.link_entry.delete(0, tk.END)

    def delete_links(self):
        self.link_text.delete(1.0, tk.END)

    def download_videos(self):
        self.output_text.delete(1.0, tk.END)
        file_path = "../mp3_player"
        self.save_links(file_path)

        with open(file_path, "r") as file:
            text = file.readlines()

        for row in text:
            link = row.strip()
            yt = YouTube(link)

            self.output_text.insert(tk.END, f"Downloading: {yt.title}\n")
            yd = yt.streams.get_highest_resolution()
            yd.download('./MP3 player')
            self.output_text.insert(tk.END, f"Downloaded: {yt.title}\n")

        self.output_text.update()

    def apply_styles(self):
        self.root.configure(bg="#212a54")

        style = ttk.Style()
        style.configure("TButton", padding=5, relief="flat", background="black", foreground="black")
        style.map("TButton", background=[("active", "#333333")])

        # Adding hover effect
        style.map("TButton",
                  background=[("active", "#333333"),
                              ("!active", "black")])


if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
