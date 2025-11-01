from pydub import AudioSegment
import tkinter as tk
from tkinter import filedialog, messagebox


def select_input_file():
    file_path = filedialog.askopenfilename(title="选择音频文件", filetypes=[("音频文件", "*.wav;*.pcm;*.mp3"), ("所有文件", "*")])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, file_path)


def select_output_folder():
    output_folder = filedialog.askdirectory(title="选择输出文件夹")
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_folder)


def convert_to_mp3():
    input_file = input_entry.get()
    output_folder = output_entry.get()

    if not input_file or not output_folder:
        messagebox.showerror("错误", "请先选择输入文件和输出文件夹！")
        return

    try:
        # 加载音频文件
        audio = AudioSegment.from_file(input_file)

        # 设置输出文件路径
        output_file = f"{output_folder}/output.mp3"

        # 导出为MP3格式
        audio.export(output_file, format="mp3")

        messagebox.showinfo("成功", f"文件已成功转换为MP3格式，保存在：\n{output_file}")
    except Exception as e:
        messagebox.showerror("错误", f"转换失败：{e}")


# 创建GUI界面
root = tk.Tk()
root.geometry("500x300")
root.title("音频转换工具")

# 输入文件部分
input_label = tk.Label(root, text="选择音频文件:")
input_label.pack()

input_entry = tk.Entry(root, width=50)
input_entry.pack()

browse_input_button = tk.Button(root, text="浏览", command=select_input_file)
browse_input_button.pack()

# 输出文件夹部分
output_label = tk.Label(root, text="选择输出文件夹:")
output_label.pack()

output_entry = tk.Entry(root, width=50)
output_entry.pack()

browse_output_button = tk.Button(root, text="选择输出文件夹", command=select_output_folder)
browse_output_button.pack()

# 转换按钮
convert_button = tk.Button(root, text="转换为MP3", command=convert_to_mp3)
convert_button.pack()

root.mainloop()