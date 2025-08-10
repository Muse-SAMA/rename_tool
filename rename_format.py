import os

def get_files_in_directory(directory):
    return [files.name for files in os.scandir(directory) if files.is_file()]

# 确认和回滚
def confirm(prompt,default="y"):
    choice = input(f"{prompt}(y/n,默认{default}:)").strip().lower()
    if not choice:
        choice = default
    return (choice=="y")

def preview_and_confirm(rename_map):
    print("\n=== 预览重命名 ===")
    for old,new in rename_map:
        print(f"{old}->{new}")
    return confirm("是否确认执行以上重命名？")

# 获得文件夹中所有文件并排序
def get_sorted_files(directory, sort_by="time"):
    files = get_files_in_directory(directory)   # 获得全部文件（文件夹除外）
    if sort_by=="time":
        files.sort(
            key = lambda f:
                os.path.getctime(os.path.join(directory,f))
        )
    elif sort_by=="name":
        files.sort()
    else:
        raise ValueError("sort_by must be 'time' or 'name'")
    return files

def generate_new_name(base_name, index, digits, extension):
    return f"{base_name}{str(index).zfill(digits)}{extension}"

def rename_preview(directory,base_name="File_",start_index=1,digits=3, sort_by_time=True):
    files = get_sorted_files(directory)
        
    print(f"共找到 {len(files)} 个文件，将进行重命名...")
    
    rename_map = []
    history = []
    index = start_index
    for original_name in files:
        ext = os.path.splitext(original_name)[1] # 获得文件后缀
        while True:
            new_name = generate_new_name(base_name, index, digits, ext)
            dst = os.path.join(directory,new_name)
            index += 1
        
            if os.path.exists(dst):
                continue
            else:
                break
        
        rename_map.append((original_name, new_name))
        history.append((new_name, original_name))
    
    if not preview_and_confirm(rename_map):
        print("❌ 用户取消重命名。")
        history.clear()
    return history
    
def rollback(history,directory):
    if not history:
        print("⚠️ 没有可回退的记录。")
        return
    print("=== 回退重命名 ===")
    for new,old in history:
        src = os.path.join(directory,new)
        dst = os.path.join(directory,old)
        os.rename(src,dst)
        print(f"↩️ {new} → {old}")
    print("✅ 回退完成。")

# 批量按格式重命名
def rename_files_in_format(directory,base_name="File_",start_index=1,digits=3, sort_by_time=True):
    files = get_sorted_files(directory)
    
    index = start_index
    for original_name in files:
        ext = os.path.splitext(original_name)[1] # 获得文件后缀
        while True:
            new_name = generate_new_name(base_name, index, digits, ext)
            dst = os.path.join(directory,new_name)
        
            if os.path.exists(dst):
                print(f"⚠️ 已存在，跳过{new_name}")
                index += 1
                continue
            
            else:
                break
            
        src = os.path.join(directory,original_name)
        os.rename(src,dst)
        print(f"✅ {original_name} → {new_name}")
        index += 1
