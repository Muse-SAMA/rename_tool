import os

def get_files_in_directory(directory):
    return [files.name for files in os.scandir(directory) if files.is_file()]

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