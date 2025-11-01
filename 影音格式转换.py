from tkinter import Tk, Label, Listbox
from tkinterdnd2 import DND_FILES, TkinterDnD

def handle_drop(event):
    # 获取拖入的文件路径（支持多文件）
    files = root.tk.splitlist(event.data)
    listbox.delete(0, 'end')  # 清空列表
    for file in files:
        listbox.insert('end', file)

# 使用 TkinterDnD 的窗口代替标准 Tk
root = TkinterDnD.Tk()
root.title("文件拖拽示例")
root.geometry("400x300")

# 创建可拖拽区域（这里用Listbox组件）
label = Label(root, text="拖拽文件到下方区域：")
label.pack(pady=10)

listbox = Listbox(root, width=50, height=10)
listbox.pack(padx=20, pady=10)

# 注册拖拽事件
listbox.drop_target_register(DND_FILES)
listbox.dnd_bind('<<Drop>>', handle_drop)

root.mainloop()