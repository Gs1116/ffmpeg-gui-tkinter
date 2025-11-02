import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import sys
import tempfile

def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    ffmpeg_exe = os.path.join(base_dir, 'ffmpeg.exe')
    
    if not os.path.exists(ffmpeg_exe):
        ffmpeg_exe = extract_ffmpeg()
    
    return ffmpeg_exe

def extract_ffmpeg():
    temp_dir = tempfile.gettempdir()
    ffmpeg_path = os.path.join(temp_dir, 'ffmpeg_temp.exe')
    
    if os.path.exists(ffmpeg_path):
        return ffmpeg_path
    
    try:
        if getattr(sys, 'frozen', False):
            import pkgutil
            ffmpeg_data = pkgutil.get_data(__name__, 'ffmpeg.exe')
        else:
            with open('ffmpeg.exe', 'rb') as f:
                ffmpeg_data = f.read()
        
        with open(ffmpeg_path, 'wb') as f:
            f.write(ffmpeg_data)
        
        return ffmpeg_path
    except Exception as e:
        messagebox.showerror("错误", f"无法提取 ffmpeg: {str(e)}")
        return None

SUPPORTED_FORMATS = {
    "视频": {
        "MP4": {"ext": ".mp4", "cmd": "-c:v libx264 -crf 23 -preset veryfast -c:a aac"},
        "MKV": {"ext": ".mkv", "cmd": "-c:v libx264 -c:a aac"},
        "AVI": {"ext": ".avi", "cmd": "-c:v libx264 -c:a aac"},
        "FLV": {"ext": ".flv", "cmd": "-c:v libx264 -c:a aac"},
        "MOV": {"ext": ".mov", "cmd": "-c:v libx264 -c:a aac"},
        "WMV": {"ext": ".wmv", "cmd": "-c:v wmv2 -c:a wmav2"}, 
        "MPG": {"ext": ".mpg", "cmd": "-c:v mpeg2video -q:v 2"}, 
        "GIF": {"ext": ".gif", "cmd": "-vf fps=10,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"}
    },
    "音频": {
        "MP3": {"ext": ".mp3", "cmd": "-c:a libmp3lame -q:a 2"},
        "WAV": {"ext": ".wav", "cmd": "-c:a pcm_s16le"},
        "WMA": {"ext": ".wma", "cmd": "-c:a wmav2"},
        "M4A": {"ext": ".m4a", "cmd": "-c:a aac"},
        "FLAC": {"ext": ".flac", "cmd": "-c:a flac"},
        "AC3": {"ext": ".ac3", "cmd": "-c:a ac3"},
        "AAC": {"ext": ".aac", "cmd": "-c:a aac"},
        "MP2": {"ext": ".mp2", "cmd": "-c:a mp2"},
        "OGG": {"ext": ".ogg", "cmd": "-c:a libvorbis"},       
        "WV": {"ext": ".wv", "cmd": "-c:a wavpack"}       
    },
    "图片": {
        "PNG": {"ext": ".png", "cmd": ""},
        "JPG": {"ext": ".jpg", "cmd": "-c:v mjpeg -q:v 2"},
        "WEBP": {"ext": ".webp", "cmd": "-c:v libwebp -q:v 80"},
        "BMP": {"ext": ".bmp", "cmd": ""},
        "GIF": {"ext": ".gif", "cmd": "-vf split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"},
        "TIF": {"ext": ".tif", "cmd": ""},
        "TGA": {"ext": ".tga", "cmd": ""},
    }
}

def select_file(entry):
    file_path = filedialog.askopenfilename(
        title="选择文件",
        filetypes=[("所有文件", "*.*")]
    )
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def select_output_folder(entry):
    output_folder = filedialog.askdirectory(title="选择输出文件夹")
    entry.delete(0, tk.END)
    entry.insert(0, output_folder)

def convert(section, input_entry, output_entry, format_var):
    input_file = input_entry.get()
    output_folder = output_entry.get()
    selected_format = format_var.get()

    if not input_file:
        messagebox.showerror("错误", f"请先选择{section}文件！")
        return
    if not output_folder:
        messagebox.showerror("错误", "请先选择输出文件夹！")
        return
    if not selected_format:
        messagebox.showerror("错误", "请选择目标格式！")
        return

    ffmpeg_path = get_ffmpeg_path()
    if not ffmpeg_path or not os.path.exists(ffmpeg_path):
        messagebox.showerror("错误", "找不到 ffmpeg，转换无法进行！")
        return

    file_name = os.path.basename(input_file)
    output_file = os.path.join(output_folder, os.path.splitext(file_name)[0] + SUPPORTED_FORMATS[section][selected_format]["ext"])

    build_command = [
        ffmpeg_path,  # 使用提取的 ffmpeg 路径
        "-i", input_file,
        *SUPPORTED_FORMATS[section][selected_format]["cmd"].split(),
        output_file
    ]

    try:
        subprocess.run(build_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        messagebox.showinfo("成功", f"{section}转换完成！")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("错误", f"转换过程中发生错误：\n{e.stderr.decode()}")

root = tk.Tk()
root.geometry("800x500")
root.title("多媒体格式转换工具")

video_frame = tk.LabelFrame(root, text="视频处理", padx=10, pady=10)
audio_frame = tk.LabelFrame(root, text="音频处理", padx=10, pady=10)
image_frame = tk.LabelFrame(root, text="图片处理", padx=10, pady=10)

video_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
audio_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
image_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

video_file_entry = tk.Entry(video_frame, width=30)
video_file_entry.pack()
video_browse_button = tk.Button(video_frame, text="浏览", command=lambda: select_file(video_file_entry))
video_browse_button.pack()
video_output_entry = tk.Entry(video_frame, width=30)
video_output_entry.pack()
video_output_button = tk.Button(video_frame, text="选择输出文件夹", command=lambda: select_output_folder(video_output_entry))
video_output_button.pack()
video_format_var = tk.StringVar(video_frame)
video_format_var.set(list(SUPPORTED_FORMATS["视频"].keys())[0])
video_format_option = ttk.Combobox(video_frame, textvariable=video_format_var, values=list(SUPPORTED_FORMATS["视频"].keys()))
video_format_option.pack()
video_convert_button = tk.Button(video_frame, text="开始转换", command=lambda: convert("视频", video_file_entry, video_output_entry, video_format_var))
video_convert_button.pack()

audio_file_entry = tk.Entry(audio_frame, width=30)
audio_file_entry.pack()
audio_browse_button = tk.Button(audio_frame, text="浏览", command=lambda: select_file(audio_file_entry))
audio_browse_button.pack()
audio_output_entry = tk.Entry(audio_frame, width=30)
audio_output_entry.pack()
audio_output_button = tk.Button(audio_frame, text="选择输出文件夹", command=lambda: select_output_folder(audio_output_entry))
audio_output_button.pack()
audio_format_var = tk.StringVar(audio_frame)
audio_format_var.set(list(SUPPORTED_FORMATS["音频"].keys())[0])
audio_format_option = ttk.Combobox(audio_frame, textvariable=audio_format_var, values=list(SUPPORTED_FORMATS["音频"].keys()))
audio_format_option.pack()
audio_convert_button = tk.Button(audio_frame, text="开始转换", command=lambda: convert("音频", audio_file_entry, audio_output_entry, audio_format_var))
audio_convert_button.pack()

image_file_entry = tk.Entry(image_frame, width=30)
image_file_entry.pack()
image_browse_button = tk.Button(image_frame, text="浏览", command=lambda: select_file(image_file_entry))
image_browse_button.pack()
image_output_entry = tk.Entry(image_frame, width=30)
image_output_entry.pack()
image_output_button = tk.Button(image_frame, text="选择输出文件夹", command=lambda: select_output_folder(image_output_entry))
image_output_button.pack()
image_format_var = tk.StringVar(image_frame)
image_format_var.set(list(SUPPORTED_FORMATS["图片"].keys())[0])
image_format_option = ttk.Combobox(image_frame, textvariable=image_format_var, values=list(SUPPORTED_FORMATS["图片"].keys()))
image_format_option.pack()
image_convert_button = tk.Button(image_frame, text="开始转换", command=lambda: convert("图片", image_file_entry, image_output_entry, image_format_var))
image_convert_button.pack()

root.mainloop()