import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import threading
from datetime import datetime

class VideoMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FFmpeg音视频合并工具")
        self.root.geometry("850x650")
        self.root.resizable(True, True)
        self.root.configure(bg="#E92A2A")
        
        # 设置应用图标（如果有ffmpeg图标的话）
        try:
            self.root.iconbitmap("ffmpeg.ico")
        except:
            pass
        
        # 创建样式
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", padding=6, font=("Arial", 10))
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        self.style.configure("Title.TLabel", background="#f0f0f0", font=("Arial", 16, "bold"))
        self.style.configure("Section.TLabel", background="#f0f0f0", font=("Arial", 12, "bold"))
        self.style.configure("Status.TLabel", background="#e0e0e0", font=("Arial", 9))
        self.style.configure("TCombobox", font=("Arial", 10))
        self.style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        self.style.configure("Treeview", font=('Arial', 9), rowheight=25)
        
        # 创建主框架
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ttk.Label(self.main_frame, text="FFmpeg音视频合并工具", style="Title.TLabel")
        title_label.pack(pady=(0, 15))
        
        # 创建选项卡
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 创建各个功能选项卡
        self.create_concatenate_tab()
        self.create_add_audio_tab()
        self.create_replace_audio_tab()
        self.create_mix_audio_tab()
        
        # 输出文件设置
        output_frame = ttk.LabelFrame(self.main_frame, text="输出设置")
        output_frame.pack(fill=tk.X, pady=15)
        
        ttk.Label(output_frame, text="输出文件:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.output_path = tk.StringVar()
        output_entry = ttk.Entry(output_frame, textvariable=self.output_path, width=60)
        output_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        
        ttk.Button(output_frame, text="浏览...", command=self.browse_output).grid(row=0, column=2, padx=5, pady=5)
        
        # 合并按钮
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="开始合并", command=self.start_merge, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清除所有", command=self.clear_all, style="TButton").pack(side=tk.LEFT, padx=5)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, style="Status.TLabel")
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 设置默认输出路径
        self.set_default_output_path()
    
    def set_default_output_path(self):
        """设置默认输出路径"""
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_path.set(os.path.join(desktop, f"merged_video_{timestamp}.mp4"))
    
    def create_concatenate_tab(self):
        """创建视频拼接选项卡"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="拼接视频")
        
        # 说明
        desc_label = ttk.Label(tab, text="将多个视频文件按顺序拼接成一个视频", style="Section.TLabel")
        desc_label.pack(pady=(10, 5), anchor="w")
        
        # 文件列表框架
        list_frame = ttk.LabelFrame(tab, text="视频文件列表 (按顺序)")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 创建Treeview
        columns = ("no", "path")
        self.concatenate_tree = ttk.Treeview(
            list_frame, columns=columns, show="headings", selectmode="extended"
        )
        
        # 设置列
        self.concatenate_tree.heading("no", text="序号")
        self.concatenate_tree.column("no", width=50, anchor="center")
        self.concatenate_tree.heading("path", text="文件路径")
        self.concatenate_tree.column("path", width=600, anchor="w")
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.concatenate_tree.yview)
        self.concatenate_tree.configure(yscrollcommand=scrollbar.set)
        
        # 布局
        self.concatenate_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 按钮框架
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(btn_frame, text="添加文件", command=self.add_concatenate_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="移除选中", command=self.remove_concatenate_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="上移", command=lambda: self.move_item(self.concatenate_tree, -1)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="下移", command=lambda: self.move_item(self.concatenate_tree, 1)).pack(side=tk.LEFT, padx=5)
    
    def create_add_audio_tab(self):
        """创建添加音频选项卡"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="添加背景音乐")
        
        # 说明
        desc_label = ttk.Label(tab, text="为视频添加背景音乐", style="Section.TLabel")
        desc_label.pack(pady=(10, 5), anchor="w")
        
        # 文件选择框架
        file_frame = ttk.Frame(tab)
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(file_frame, text="视频文件:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.video_path = tk.StringVar()
        video_entry = ttk.Entry(file_frame, textvariable=self.video_path, width=70)
        video_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        ttk.Button(file_frame, text="浏览...", command=lambda: self.browse_file(self.video_path, [("视频文件", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv")])).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(file_frame, text="音频文件:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.audio_path = tk.StringVar()
        audio_entry = ttk.Entry(file_frame, textvariable=self.audio_path, width=70)
        audio_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")
        ttk.Button(file_frame, text="浏览...", command=lambda: self.browse_file(self.audio_path, [("音频文件", "*.mp3 *.wav *.aac *.flac *.ogg")])).grid(row=1, column=2, padx=5, pady=5)
        
        # 选项框架
        option_frame = ttk.LabelFrame(tab, text="音频选项")
        option_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(option_frame, text="音频音量:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.audio_volume = tk.StringVar(value="1.0")
        volume_entry = ttk.Entry(option_frame, textvariable=self.audio_volume, width=10)
        volume_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        ttk.Label(option_frame, text="(0.1-2.0, 1.0为原始音量)").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        self.audio_loop = tk.BooleanVar(value=False)
        ttk.Checkbutton(option_frame, text="循环音频以适应视频长度", variable=self.audio_loop).grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="w")
        
        self.keep_original_audio = tk.BooleanVar(value=True)
        ttk.Checkbutton(option_frame, text="保留原始视频音频", variable=self.keep_original_audio).grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="w")
    
    def create_replace_audio_tab(self):
        """创建替换音频选项卡"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="替换音频")
        
        # 说明
        desc_label = ttk.Label(tab, text="替换视频中的音频", style="Section.TLabel")
        desc_label.pack(pady=(10, 5), anchor="w")
        
        # 文件选择框架
        file_frame = ttk.Frame(tab)
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(file_frame, text="视频文件:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.replace_video_path = tk.StringVar()
        video_entry = ttk.Entry(file_frame, textvariable=self.replace_video_path, width=70)
        video_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        ttk.Button(file_frame, text="浏览...", command=lambda: self.browse_file(self.replace_video_path, [("视频文件", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv")])).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(file_frame, text="音频文件:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.replace_audio_path = tk.StringVar()
        audio_entry = ttk.Entry(file_frame, textvariable=self.replace_audio_path, width=70)
        audio_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")
        ttk.Button(file_frame, text="浏览...", command=lambda: self.browse_file(self.replace_audio_path, [("音频文件", "*.mp3 *.wav *.aac *.flac *.ogg")])).grid(row=1, column=2, padx=5, pady=5)
    
    def create_mix_audio_tab(self):
        """创建混音选项卡"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="混音")
        
        # 说明
        desc_label = ttk.Label(tab, text="混合视频原始音频和新音频", style="Section.TLabel")
        desc_label.pack(pady=(10, 5), anchor="w")
        
        # 文件选择框架
        file_frame = ttk.Frame(tab)
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(file_frame, text="视频文件:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.mix_video_path = tk.StringVar()
        video_entry = ttk.Entry(file_frame, textvariable=self.mix_video_path, width=70)
        video_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        ttk.Button(file_frame, text="浏览...", command=lambda: self.browse_file(self.mix_video_path, [("视频文件", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv")])).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(file_frame, text="音频文件:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.mix_audio_path = tk.StringVar()
        audio_entry = ttk.Entry(file_frame, textvariable=self.mix_audio_path, width=70)
        audio_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")
        ttk.Button(file_frame, text="浏览...", command=lambda: self.browse_file(self.mix_audio_path, [("音频文件", "*.mp3 *.wav *.aac *.flac *.ogg")])).grid(row=1, column=2, padx=5, pady=5)
        
        # 选项框架
        option_frame = ttk.LabelFrame(tab, text="混音选项")
        option_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(option_frame, text="原始音频音量:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.original_volume = tk.StringVar(value="1.0")
        orig_vol_entry = ttk.Entry(option_frame, textvariable=self.original_volume, width=10)
        orig_vol_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(option_frame, text="新音频音量:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.new_volume = tk.StringVar(value="0.5")
        new_vol_entry = ttk.Entry(option_frame, textvariable=self.new_volume, width=10)
        new_vol_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(option_frame, text="(0.1-2.0, 1.0为原始音量)").grid(row=0, column=2, rowspan=2, padx=5, pady=5, sticky="w")
    
    def browse_file(self, path_var, filetypes):
        """浏览文件"""
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            path_var.set(filename)
    
    def browse_output(self):
        """浏览输出文件"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4文件", "*.mp4"), ("所有文件", "*.*")]
        )
        if filename:
            self.output_path.set(filename)
    
    def add_concatenate_files(self):
        """添加拼接文件"""
        files = filedialog.askopenfilenames(
            title="选择视频文件",
            filetypes=[("视频文件", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv"), ("所有文件", "*.*")]
        )
        
        if files:
            for file in files:
                self.concatenate_tree.insert("", tk.END, values=(len(self.concatenate_tree.get_children()) + 1, file))
    
    def remove_concatenate_files(self):
        """移除选中的拼接文件"""
        selected_items = self.concatenate_tree.selection()
        for item in selected_items:
            self.concatenate_tree.delete(item)
        
        # 重新编号
        for i, item in enumerate(self.concatenate_tree.get_children()):
            self.concatenate_tree.item(item, values=(i+1, self.concatenate_tree.item(item)["values"][1]))
    
    def move_item(self, treeview, direction):
        """上移或下移列表项"""
        selected_items = treeview.selection()
        if not selected_items:
            return
        
        for item in selected_items:
            index = treeview.index(item)
            if direction == -1 and index > 0:  # 上移
                prev_item = treeview.get_children()[index-1]
                treeview.move(item, treeview.parent(prev_item), index-1)
            elif direction == 1 and index < len(treeview.get_children()) - 1:  # 下移
                next_item = treeview.get_children()[index+1]
                treeview.move(item, treeview.parent(next_item), index+1)
        
        # 重新编号
        for i, item in enumerate(treeview.get_children()):
            treeview.item(item, values=(i+1, treeview.item(item)["values"][1]))
    
    def validate_float(self, value, min_val=0.1, max_val=2.0, default=1.0):
        """验证浮点数输入"""
        try:
            num = float(value)
            if min_val <= num <= max_val:
                return num
            return default
        except ValueError:
            return default
    
    def start_merge(self):
        """开始合并操作"""
        current_tab = self.notebook.index(self.notebook.select())
        output_path = self.output_path.get().strip()
        
        if not output_path:
            messagebox.showerror("错误", "请指定输出文件路径")
            return
        
        # 根据当前选项卡执行不同的合并操作
        if current_tab == 0:  # 拼接视频
            files = [self.concatenate_tree.item(item)["values"][1] for item in self.concatenate_tree.get_children()]
            if len(files) < 2:
                messagebox.showerror("错误", "请添加至少两个视频文件")
                return
            
            self.status_var.set("开始拼接视频...")
            threading.Thread(target=self.concatenate_videos, args=(files, output_path), daemon=True).start()
            
        elif current_tab == 1:  # 添加背景音乐
            video = self.video_path.get().strip()
            audio = self.audio_path.get().strip()
            
            if not video or not audio:
                messagebox.showerror("错误", "请选择视频文件和音频文件")
                return
            
            volume = self.validate_float(self.audio_volume.get())
            loop = self.audio_loop.get()
            keep_original = self.keep_original_audio.get()
            
            self.status_var.set("开始添加背景音乐...")
            threading.Thread(target=self.add_background_audio, args=(video, audio, output_path, volume, loop, keep_original), daemon=True).start()
            
        elif current_tab == 2:  # 替换音频
            video = self.replace_video_path.get().strip()
            audio = self.replace_audio_path.get().strip()
            
            if not video or not audio:
                messagebox.showerror("错误", "请选择视频文件和音频文件")
                return
            
            self.status_var.set("开始替换音频...")
            threading.Thread(target=self.replace_audio, args=(video, audio, output_path), daemon=True).start()
            
        elif current_tab == 3:  # 混音
            video = self.mix_video_path.get().strip()
            audio = self.mix_audio_path.get().strip()
            
            if not video or not audio:
                messagebox.showerror("错误", "请选择视频文件和音频文件")
                return
            
            orig_vol = self.validate_float(self.original_volume.get())
            new_vol = self.validate_float(self.new_volume.get())
            
            self.status_var.set("开始混音处理...")
            threading.Thread(target=self.mix_audios, args=(video, audio, output_path, orig_vol, new_vol), daemon=True).start()
    
    def concatenate_videos(self, files, output):
        """拼接多个视频文件"""
        # 创建临时文件列表
        list_file = "concat_list.txt"
        with open(list_file, "w", encoding="utf-8") as f:
            for file in files:
                f.write(f"file '{file}'\n")
        
        try:
            cmd = [
                "ffmpeg",
                "-f", "concat",
                "-safe", "0",
                "-i", list_file,
                "-c", "copy",
                output
            ]
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            
            # 实时更新状态
            for line in process.stdout:
                if "time=" in line:
                    time_str = line.split("time=")[1].split(" ")[0]
                    self.status_var.set(f"处理中: {time_str}")
            
            process.communicate()
            
            if process.returncode == 0:
                self.status_var.set(f"视频拼接完成: {output}")
                messagebox.showinfo("完成", f"视频拼接成功!\n输出文件: {output}")
            else:
                self.status_var.set("拼接失败，请检查文件格式")
                messagebox.showerror("错误", "视频拼接失败，请检查文件格式是否一致")
        except Exception as e:
            self.status_var.set(f"错误: {str(e)}")
            messagebox.showerror("错误", f"处理过程中发生错误: {str(e)}")
        finally:
            # 删除临时文件
            try:
                os.remove(list_file)
            except:
                pass
    
    def add_background_audio(self, video, audio, output, volume=1.0, loop=False, keep_original=True):
        """为视频添加背景音乐"""
        try:
            # 基本命令
            cmd = ["ffmpeg", "-i", video, "-i", audio]
            
            # 处理音频
            if loop:
                # 循环音频
                cmd.extend([
                    "-filter_complex",
                    f"[1:a]volume={volume},aloop=loop=-1:size=2e+09[a];" +
                    f"[0:a][a]amix=inputs={2 if keep_original else 1}[outa]"
                ])
            else:
                # 不循环音频
                cmd.extend([
                    "-filter_complex",
                    f"[1:a]volume={volume}[a];" +
                    f"[0:a][a]amix=inputs={2 if keep_original else 1}:duration=first[outa]"
                ])
            
            # 输出设置
            cmd.extend([
                "-map", "0:v",
                "-map", "[outa]",
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                output
            ])
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            
            # 实时更新状态
            for line in process.stdout:
                if "time=" in line:
                    time_str = line.split("time=")[1].split(" ")[0]
                    self.status_var.set(f"处理中: {time_str}")
            
            process.communicate()
            
            if process.returncode == 0:
                self.status_var.set(f"添加背景音乐完成: {output}")
                messagebox.showinfo("完成", f"成功添加背景音乐!\n输出文件: {output}")
            else:
                self.status_var.set("添加背景音乐失败")
                messagebox.showerror("错误", "添加背景音乐失败")
        except Exception as e:
            self.status_var.set(f"错误: {str(e)}")
            messagebox.showerror("错误", f"处理过程中发生错误: {str(e)}")
    
    def replace_audio(self, video, audio, output):
        """替换视频中的音频"""
        try:
            cmd = [
                "ffmpeg",
                "-i", video,
                "-i", audio,
                "-c:v", "copy",
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-shortest",
                output
            ]
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            
            # 实时更新状态
            for line in process.stdout:
                if "time=" in line:
                    time_str = line.split("time=")[1].split(" ")[0]
                    self.status_var.set(f"处理中: {time_str}")
            
            process.communicate()
            
            if process.returncode == 0:
                self.status_var.set(f"音频替换完成: {output}")
                messagebox.showinfo("完成", f"音频替换成功!\n输出文件: {output}")
            else:
                self.status_var.set("音频替换失败")
                messagebox.showerror("错误", "音频替换失败")
        except Exception as e:
            self.status_var.set(f"错误: {str(e)}")
            messagebox.showerror("错误", f"处理过程中发生错误: {str(e)}")
    
    def mix_audios(self, video, audio, output, orig_vol=1.0, new_vol=0.5):
        """混合视频原始音频和新音频"""
        try:
            cmd = [
                "ffmpeg",
                "-i", video,
                "-i", audio,
                "-filter_complex",
                f"[0:a]volume={orig_vol}[a0];" +
                f"[1:a]volume={new_vol}[a1];" +
                "[a0][a1]amix=inputs=2:duration=first[outa]",
                "-map", "0:v",
                "-map", "[outa]",
                "-c:v", "copy",
                "-c:a", "aac",
                output
            ]
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            
            # 实时更新状态
            for line in process.stdout:
                if "time=" in line:
                    time_str = line.split("time=")[1].split(" ")[0]
                    self.status_var.set(f"处理中: {time_str}")
            
            process.communicate()
            
            if process.returncode == 0:
                self.status_var.set(f"混音完成: {output}")
                messagebox.showinfo("完成", f"混音成功!\n输出文件: {output}")
            else:
                self.status_var.set("混音失败")
                messagebox.showerror("错误", "混音失败")
        except Exception as e:
            self.status_var.set(f"错误: {str(e)}")
            messagebox.showerror("错误", f"处理过程中发生错误: {str(e)}")
    
    def clear_all(self):
        """清除所有输入"""
        # 清除拼接列表
        for item in self.concatenate_tree.get_children():
            self.concatenate_tree.delete(item)
        
        # 清除添加背景音乐选项卡
        self.video_path.set("")
        self.audio_path.set("")
        self.audio_volume.set("1.0")
        self.audio_loop.set(False)
        self.keep_original_audio.set(True)
        
        # 清除替换音频选项卡
        self.replace_video_path.set("")
        self.replace_audio_path.set("")
        
        # 清除混音选项卡
        self.mix_video_path.set("")
        self.mix_audio_path.set("")
        self.original_volume.set("1.0")
        self.new_volume.set("0.5")
        
        # 重置输出路径
        self.set_default_output_path()
        
        self.status_var.set("已清除所有输入")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoMergerApp(root)
    root.mainloop()