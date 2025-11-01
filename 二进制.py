import struct
import tkinter as tk
from tkinter import filedialog


def select_file():
    file_path = filedialog.askopenfilename(title="选择文件", filetypes=[("所有文件", "*")])
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

def select_output_folder():
    output_folder = filedialog.askdirectory(title="选择输出文件夹")
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_folder)

def start():
    input_file = file_entry.get()
    output_folder = output_entry.get()

    if not input_file or not output_folder:
        tk.messagebox.showerror("错误", "请先选择输入文件和输出文件夹！")
        return

    try:
        with open(input_file, "rb") as f:
            data = f.read()

        output_path = f"{output_folder}/output.bin"  # 使用用户选择的输出文件夹路径
        with open(output_path, "wb") as binary_file:
            binary_file.write(data) 

        tk.messagebox.showinfo("成功", "文件转换完成！")
    except Exception as e:
        tk.messagebox.showerror("错误", f"文件转换失败：{e}")

root = tk.Tk()
root.geometry("500x500")
root.title("二进制")

file_label = tk.Label(root, text="选择文件:")
file_label.pack()

file_entry = tk.Entry(root, width=50)
file_entry.pack()

browse_button = tk.Button(root, text="浏览", command=select_file)
browse_button.pack()

# 添加选择输出文件夹的部分
output_label = tk.Label(root, text="选择输出文件夹:")
output_label.pack()

output_entry = tk.Entry(root, width=50)
output_entry.pack()

output_button = tk.Button(root, text="选择输出文件夹", command=select_output_folder)
output_button.pack()

convert_button = tk.Button(root, text="开始", command=start)
convert_button.pack()

root.mainloop()