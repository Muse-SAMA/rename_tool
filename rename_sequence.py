import os
import sys
import tkinter as tk
from tkinter import messagebox
import subprocess
from datetime import datetime
from datetime import datetime
import tempfile
import atexit

class PreviewRenamer:
    def __init__(self, file_list, change_file_type=False):
        self.file_list = file_list
        self.index = 0
        self.change_file_type = change_file_type
        self.temp_files = []    # 记录临时文件，退出时删除
        atexit.register(self.cleanup_temp_files)

        self.root = tk.Tk()
        self.root.title("当前重命名文件预览")
        # 设置窗口大小
        self.root.geometry("")
        self.root.minsize(400,300)
        # 预览区
        self.preview_frame = tk.Frame(self.root)
        self.preview_frame.pack(padx=10,pady=10,fill="both",expand=True)
        # 输入框
        self.entry = tk.Entry(self.root,width=50)
        self.entry.pack(pady=5)
        # 按钮
        btn_frame = tk.Frame(self.root)
        btn_frame.pack()
        tk.Button(btn_frame,text="确定", command=self.rename_and_next).pack(side=tk.LEFT,padx=5)
        tk.Button(btn_frame,text="跳过", command=self.skip_file).pack(side=tk.LEFT,padx=5)
        tk.Button(btn_frame,text="打开文件", command=self.open_file).pack(side=tk.LEFT,padx=5)
        # 回车确定，esc跳过
        self.root.bind("<Return>",lambda event: self.rename_and_next())
        self.root.bind("<Escape>",lambda event: self.skip_file())

        self.show_file()
        self.root.mainloop()

    def jpg_to_png(self, jpg_path):
        tmp_dir = tempfile.gettempdir() # 创建临时路径
        png_path = os.path.join(tmp_dir, os.path.basename(jpg_path)+".png")
        # magick_path = r"D:\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
        subprocess.run([
            "magick", 
            jpg_path, 
            png_path
        ], check=True)

        self.temp_files.append(png_path)
        return png_path

    def cleanup_temp_files(self):
        # 退出时删除所有生成的临时文件
        for f in self.temp_files:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except Exception:
                pass

    def clear_preview(self):
        for widget in self.preview_frame.winfo_children():
            widget.destroy()

    def show_file(self):
        if self.index >= len(self.file_list):
            messagebox.showinfo("完成","所有文件已处理")
            self.root.destroy()
            return
        
        file_path = self.file_list[self.index]
        self.root.title(f"({self.index+1}/{len(self.file_list)}) {os.path.basename(file_path)}")
        ext = os.path.splitext(file_path)[1].lower()
        self.entry.delete(0,tk.END) # 清空输入框
        self.clear_preview()

        try:
            if ext in [".png",".gif",".jpg",".jpeg"]:
                if ext in [".jpg",".jpeg"]:
                    file_path = self.jpg_to_png(file_path)

                img = tk.PhotoImage(file=file_path)

                screen_w = self.root.winfo_screenwidth()
                screen_h = self.root.winfo_screenheight()
                
                img_w, img_h = img.width(), img.height()
                max_w = int(screen_w*0.6)
                max_h = int(screen_h*0.5)
                scale_w = img_w // max_w + 1 if img_w > max_w else 1
                scale_h = img_h // max_h + 1 if img_h > max_h else 1
                scale = max(scale_w,scale_h)

                if scale > 1:
                    img = img.subsample(scale,scale)

                img_label = tk.Label(self.preview_frame,image=img)
                img_label.image = img
                img_label.pack()
            elif ext in [".txt",".md",".py",".json"]:
                with open(file_path,"r",encoding="utf-8",errors="ignore") as f:
                    text = "".join(f.readlines()[:20])
                text_frame = tk.Frame(self.preview_frame)
                text_frame.pack(fill="both",expand=True)

                text_widget = tk.Text(text_frame,wrap="word",height=min(20,text.count("\n")+2))
                text_widget.insert("1.0",text)
                text_widget.config(state="disabled")

                scroll = tk.Scrollbar(text_frame,command=text_widget.yview)
                text_widget.config(yscrollcommand=scroll.set)
                text_widget.pack(side="left",fill="both",expand=True)
                scroll.pack(side="right",fill="y")
            else:
                info = f"文件类型：{ext or '未知'}"
                "大小：{os.path.getsize(file_path)//1024}KB"
                "修改时间: {datetime.fromtimestamp(os.path.getmtime(file_path))}"
                tk.Label(self.preview_frame, text=info,justify="left").pack()

        except Exception as e:
            tk.Label(self.preview_frame, text=f"无法预览：{e}").pack()

        self.root.update_idletasks()
        self.root.geometry("")

    def rename_and_next(self):
        new_name = self.entry.get().strip()
        if not new_name:
            messagebox.showwarning("错误","文件名不能为空")
            return
        
        old_path = self.file_list[self.index]
        ext = "" if self.change_file_type else os.path.splitext(old_path)[1]
        new_path = os.path.join(os.path.dirname(old_path),new_name+ext)
        
        if os.path.exists(new_path):
            messagebox.showerror("错误","目标文件已存在")
            return
        
        os.rename(old_path,new_path)
        self.file_list[self.index] = new_path
        self.index += 1
        self.show_file()

    def skip_file(self):
        self.index += 1
        self.show_file()

    def open_file(self):
        file_path = self.file_list[self.index]
        if sys.platform.startswith("darwin"):   # 检查是否为mac
            subprocess.call(("open",file_path))
        elif os.name =="nt":    # windows
            os.startfile(file_path)
        elif os.name == "posix":    # Unix
            subprocess.call(("xdg-open",file_path))

def get_files_in_directory(directory):
    return [files.name for files in os.scandir(directory) if files.is_file()]

def rename_files_in_sequence_with_preview(directory, change_file_type=False):
    files = get_files_in_directory(directory)
    file_paths = [os.path.join(directory,f) for f in files]
    PreviewRenamer(file_paths,change_file_type)

def rename_single_file_or_folder_with_preview(src, change_file_type=False):
    PreviewRenamer([src],change_file_type)

"""
# 手动重命名文件
def rename_files_in_sequence(directory, change_file_type=False):
    # 获得全部文件（文件夹除外）
    files = get_files_in_directory(directory)
    # 显示当前文件名称，输入目标文件名称
    for original_name in files:
        ext = "" if change_file_type else os.path.splitext(original_name)[1]
        
        while True:
            user_input = input(f"重命名{original_name}为：").strip()
            if not user_input:
                print("❌ 文件名不能为空，请重新输入。")
                continue
            
            new_file = f"{user_input}{ext}"
            dst = os.path.join(directory,new_file)
            if os.path.exists(dst):
                print(f"⚠️ {new_file}已存在，请重新输入。")
                continue
            
            break
                
        src = os.path.join(directory,original_name)
        os.rename(src,dst)
        print(f"✅ {original_name} → {new_file}")
        
# 重命名单个文件
def rename_single_file_or_folder(src, change_file_type=False):
    original_name = os.path.basename(src)
    dir = os.path.dirname(src)
    ext = "" if change_file_type else os.path.splitext(original_name)[1]
    while True:
        user_input = input(f"重命名{original_name}为：").strip()
        if not user_input:
            print("❌ 文件名不能为空，请重新输入。")
            continue
        
        new_file = f"{user_input}{ext}"
        dst = os.path.join(dir,new_file)
        if os.path.exists(dst):
            print(f"⚠️ {new_file}已存在，请重新输入。")
            continue

        break
        
    os.rename(src,dst)
"""