#chan
import threading as td
from pytube import YouTube
import tkinter as tk
import tkinter.filedialog
import tkinter.ttk as ttk
import pytube
import PIL.ImageTk, PIL.Image
import re
import os
import time
import webbrowser

video_size, audio_size = None, None
default_path = r"c:"


def set_path():
    global default_path
    default_path = tk.filedialog.askdirectory(initialdir=default_path)
    return default_path


def progress(stream: None, chunk: bytes, bytes_remaining: int):
    if video_size != None:
        bytes_done = human_bytes(video_size - bytes_remaining)
        prg["value"] = prg_max(bytes_done)
        return video_button.config(text=f"{bytes_done} Downloaded")
    else:
        bytes_done = human_bytes(audio_size - bytes_remaining)
        prg["value"] = prg_max(bytes_done)
        return audio_button.config(text=f"{bytes_done} Downloaded")


def prg_max(temp_size):
    pattern = re.compile(r"[0-9][0-9]?\.[0-9][0-9]?")
    matches = pattern.finditer(temp_size)
    for match in matches:
        return match.group(0)


def status(file_size, file_title, file_res):
    text.config(state=tk.NORMAL)
    text.delete(1.0, tk.END)
    h_size = human_bytes(file_size)
    text.insert(1.0, f"\nRes: {file_res}\nTitle :{file_title}\nLength: {h_size}")
    text.config(state=tk.DISABLED)


def human_bytes(file_size):
    by = float(file_size)
    kb = float(1024)
    mb = float(kb ** 2)
    gb = float(kb ** 3)
    if by < kb:
        return f"{by:.2f} " "Bite" if by < 1 else "Bites"
    elif kb <= by < mb:
        return f"{by/kb:.2f} KB"
    elif mb <= by < gb:
        return f"{by/mb:.2f} MB"
    elif gb <= by:
        return f"{by/gb:.2f} GB"


def audio_download():
    global audio_size, default_path
    try:
        audio_button.config(state=tk.DISABLED)
        yt = YouTube(
            url_entery.get(), on_progress_callback=progress
        ).streams.get_audio_only()
        audio_size = yt.filesize
        default_path = set_path()
        if default_path == "":
            raise ValueError("Did't Find Path!!")
        if os.path.isfile(f"{default_path}\\{yt.default_filename}.m4a"):
            raise ValueError("File Exists!!")
        prg["maximum"] = prg_max(human_bytes(audio_size))
        status(yt.filesize, yt.title, yt.audio_codec)
        yt.download(default_path)
        os.rename(
            f"{default_path}\\{yt.default_filename}",
            f"{default_path}\\{yt.default_filename}.m4a",
        )
        audio_size = None
        time.sleep(3)
        prg["value"] = 0
        text.config(state=tk.NORMAL)
        text.delete(1.0, tk.END)
        text.config(state=tk.DISABLED)
        audio_button.config(state=tk.NORMAL, text="Download Audio")
    except pytube.exceptions.RegexMatchError:
        text.config(state=tk.NORMAL)
        text.delete(1.0, tk.END)
        text.insert(1.0, "Invalid Link!!")
        audio_button.config(state=tk.NORMAL)
        time.sleep(4)
        text.delete(1.0, tk.END)
        text.config(state=tk.DISABLED)
    except ValueError as e:
        text.config(state=tk.NORMAL)
        text.delete(1.0, tk.END)
        text.insert(1.0, e)
        audio_button.config(state=tk.NORMAL)
        time.sleep(4)
        text.delete(1.0, tk.END)
        text.config(state=tk.DISABLED)


def video_download():
    global video_size, default_path
    try:
        video_button.config(state=tk.DISABLED)
        yt = YouTube(
            url_entery.get(), on_progress_callback=progress
        ).streams.get_highest_resolution()
        video_size = yt.filesize
        default_path = set_path()
        if default_path == "":
            raise ValueError("Did't Find Path!!")
        if os.path.isfile(f"{default_path}\\{yt.default_filename}"):
            raise ValueError("File Exists!!")
        status(yt.filesize, yt.title, yt.resolution)
        prg["maximum"] = prg_max(human_bytes(video_size))
        yt.download(default_path)
        os.rename(
            f"{default_path}\\{yt.default_filename}",
            f"{default_path}\\{yt.default_filename}.avi",
        )
        video_size = None
        time.sleep(3)
        prg["value"] = 0
        text.config(state=tk.NORMAL)
        text.delete(1.0, tk.END)
        text.config(state=tk.DISABLED)
        video_button.config(state=tk.NORMAL, text="Download Video")
    except pytube.exceptions.RegexMatchError:
        text.config(state=tk.NORMAL)
        text.delete(1.0, tk.END)
        text.insert(1.0, "Invalid Link!!")
        video_button.config(state=tk.NORMAL)
        time.sleep(4)
        text.delete(1.0, tk.END)
        text.config(state=tk.DISABLED)
    except ValueError as e:
        text.config(state=tk.NORMAL)
        text.delete(1.0, tk.END)
        text.insert(1.0, e)
        video_button.config(state=tk.NORMAL)
        time.sleep(4)
        text.delete(1.0, tk.END)
        text.config(state=tk.DISABLED)


def audio_thread():
    thread = td.Thread(target=audio_download)
    thread.setDaemon(True)
    thread.start()


def video_thread():
    thread = td.Thread(target=video_download)
    thread.setDaemon(True)
    thread.start()


def prg_thread():
    thread = td.Thread(target=prg_max)
    thread.setDaemon(True)
    thread.start()


def vid_url():
    if url_entery.get() == "":
        url_entery.delete(0, tk.END)
        url_entery.insert(0, "Video URL")


def clear_searches(event):
    url_entery.delete(0, tk.END)
    root.after(3000, vid_url)


def open_path():
    os.startfile(default_path)


def details():
    try:
        yt = YouTube(url_entery.get()).streams.get_highest_resolution()
        text.config(state=tk.NORMAL)
        text.delete(1.0, tk.END)
        text.insert(1.0, yt.title)
        webbrowser.open(url_entery.get())
        text.config(state=tk.DISABLED)
    except pytube.exceptions.RegexMatchError:
        text.config(state=tk.NORMAL)
        text.delete(1.0, tk.END)
        text.insert(1.0, "Invalid Link")
        video_button.config(state=tk.NORMAL)
        time.sleep(4)
        text.delete(1.0, tk.END)
        text.config(state=tk.DISABLED)


def logo_thread():
    thread = td.Thread(target=details)
    thread.setDaemon(True)
    thread.start()


def make_menu(w):
    global the_menu
    the_menu = tk.Menu(w, tearoff=0)
    the_menu.add_command(label="Cut")
    the_menu.add_command(label="Copy")
    the_menu.add_command(label="Paste")


def show_menu(e):
    w = e.widget
    the_menu.entryconfigure("Cut", command=lambda: w.event_generate("<<Cut>>"))
    the_menu.entryconfigure("Copy", command=lambda: w.event_generate("<<Copy>>"))
    the_menu.entryconfigure("Paste", command=lambda: w.event_generate("<<Paste>>"))
    the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root)


root = tk.Tk()
root.title("YAVD")
root.geometry("430x290")
root.configure(bg="black")
root.resizable(False, False)
root.iconbitmap("icon.ico")
logo = PIL.ImageTk.PhotoImage(PIL.Image.open("YV.png"))
image_button = tk.Button(
    root, image=logo, bg="black", fg="brown1", command=logo_thread, relief="flat"
)
image_button.grid(row=0, column=0, sticky="N")

url_entery = tk.Entry(root, width=70, relief="flat", bg="black", fg="brown1")
url_entery.grid(row=1, column=0, sticky="W")
url_entery.insert(0, "Video URL")
url_entery.bind("<Button-1>", clear_searches)
make_menu(root)
url_entery.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)
audio_button = tk.Button(
    root,
    text="Download Audio",
    command=audio_thread,
    relief="flat",
    bg="black",
    fg="brown1",
)
audio_button.grid(row=2, column=0)
video_button = tk.Button(
    root,
    text="Download Video",
    command=video_thread,
    relief="flat",
    bg="black",
    fg="brown1",
)
video_button.grid(row=2, column=0, sticky="w")
open_button = tk.Button(
    root, text="Open", command=open_path, relief="flat", bg="black", fg="brown1"
)
open_button.grid(row=2, column=0, ipadx=35, sticky="e")

s = ttk.Style()
s.theme_use("clam")
TROUGH_COLOR = "royal blue"
BAR_COLOR = "brown1"
s.configure(
    "bar.Horizontal.TProgressbar",
    troughcolor=TROUGH_COLOR,
    bordercolor=BAR_COLOR,
    background=BAR_COLOR,
    lightcolor=BAR_COLOR,
    darkcolor=BAR_COLOR,
)
prg = ttk.Progressbar(
    root,
    style="bar.Horizontal.TProgressbar",
    orient="horizontal",
    length="428",
    mode="determinate",
)
prg.grid(row=5, column=0, sticky="w")


text = tk.Text(
    root, width=53, height=8, wrap=tk.WORD, relief="flat", bg="black", fg="brown1",
)
text.grid(row=6, column=0)
text.insert(1.0, "HI!!")
text.config(state=tk.DISABLED)
root.mainloop()
