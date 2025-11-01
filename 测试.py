import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import sys

def select_file():
    file_path = filedialog.askopenfilename(title="选择Python文件", filetypes=[("Python 文件", "*.py")])
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

def select_icon():
    icon_path = filedialog.askopenfilename(title="选择ICO文件", filetypes=[("icon文件", "*.ico")])
    icon_entry.delete(0, tk.END)
    icon_entry.insert(0, icon_path)

def select_audio():
    audio_folder = filedialog.askdirectory(title="选择MP3文件夹")
    audio_entry.delete(0, tk.END)
    audio_entry.insert(0, audio_folder)

def select_image():
    image_folder = filedialog.askdirectory(title="选择图片文件夹")
    image_entry.delete(0, tk.END)
    image_entry.insert(0, image_folder)

def select_output_folder():
    output_folder = filedialog.askdirectory(title="选择输出文件夹")
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_folder)

def package_exe():
    python_file = file_entry.get()
    icon_file = icon_entry.get() if include_icon.get() else ""  # 根据勾选状态确定是否包含ICO
    output_folder = output_entry.get()
    audio_file = audio_entry.get() if include_audio.get() else ""  # 根据勾选状态确定是否包含MP3
    image_file = image_entry.get() if include_image.get() else ""  # 根据勾选状态确定是否包含图片

    try:
        if getattr(sys, 'frozen', False):
            # 当运行于 PyInstaller 生成的 exe 文件中时，获取 exe 文件所在目录
            base_path = sys._MEIPASS
        else:
            # 在正常的 Python 环境中运行
            base_path = os.path.abspath(".")

        # 动态构建 PyInstaller 命令
        build_command = ["pyinstaller", "--onefile", f"--distpath={output_folder}", "--noconsole", python_file]
        
        # 添加ICO文件和MP3文件以及图片文件的条件
        if include_icon.get():
            build_command.append(f"--icon={icon_file}")
        if include_audio.get():
            build_command.append(f"--add-data={audio_file};audio")
        if include_image.get():
            build_command.append(f"--add-data={image_file};image")
        subprocess.run(build_command, check=True)
        messagebox.showinfo("打包完成", "打包完成！")
    except subprocess.CalledProcessError as e:
        tk.messagebox.showerror("打包错误", f"打包过程中发生错误：\n{e}")

# 创建主窗口
root = tk.Tk()
root.geometry("500x500")
root.title("Python to EXE Converter")
root.iconbitmap(os.path.abspath("D:/python打包exe/ruobao.ico"))  # 使用绝对路径

# 添加文件选择按钮和打包按钮
file_label = tk.Label(root, text="选择Python文件:")
file_label.pack()

file_entry = tk.Entry(root, width=50)
file_entry.pack()

browse_button = tk.Button(root, text="浏览", command=select_file)
browse_button.pack()

# 添加选择图标的部分
tubiao = tk.Label(root, text="选择ICO文件:")
tubiao.pack()

icon_entry = tk.Entry(root, width=50)
icon_entry.pack()

icon_button = tk.Button(root, text="选择ICO", command=select_icon)
icon_button.pack()

# 添加选择MP3文件夹的部分
audio_label = tk.Label(root, text="选择MP3文件夹:")
audio_label.pack()

audio_entry = tk.Entry(root, width=50)
audio_entry.pack()

audio_button = tk.Button(root, text="选择MP3文件", command=select_audio)
audio_button.pack()

#选择图片文件夹的部分
image_label =tk.Label(root,text="选择图片文件夹:")
image_label.pack()

image_entry = tk.Entry(root,width=50)
image_entry.pack()

image_button = tk.Button(root,text="选择图片文件",command=select_image)
image_button.pack()

# 添加选择输出文件夹的部分
output_label = tk.Label(root, text="选择输出文件夹:")
output_label.pack()

output_entry = tk.Entry(root, width=50)
output_entry.pack()

output_button = tk.Button(root, text="选择输出文件夹", command=select_output_folder)
output_button.pack()

# 添加复选框，允许用户选择是否包含ICO和MP3文件
include_icon = tk.BooleanVar()
include_icon.set(True)  # 默认包含ICO文件

icon_checkbox = tk.Checkbutton(root, text="包含ICO图标", variable=include_icon)
icon_checkbox.pack()

include_audio = tk.BooleanVar()
include_audio.set(True)  # 默认包含MP3文件

audio_checkbox = tk.Checkbutton(root, text="包含MP3音频", variable=include_audio)
audio_checkbox.pack()

include_image = tk.BooleanVar()
include_image.set(True)  #默认包含图片文件

image_checkbox = tk.Checkbutton(root, text="包含图片",variable=include_image)
image_checkbox.pack()

# 添加打包按钮
package_button = tk.Button(root, text="打包成EXE", command=package_exe)
package_button.pack()

# 启动主循环
root.mainloop()

