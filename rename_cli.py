# 批量重命名一个目录下所有文件（不包括子文件夹）
# 确认路径合法->保存文件原名称，生成目标名称，保证目标名称不重复->重命名
# 输入路径、名称格式
import os
import sys

def is_valid_directory(directory):
    return os.path.isdir(directory)

def get_files_in_directory(directory):
    return [f for f in os.listdir(directory) 
            if os.path.isfile(os.path.join(directory,f))]

def rename_files_in_format(directory,base_name="File_",start_index=1,digits=3, sort_by_time=True):
    files = get_files_in_directory(directory)
    if sort_by_time:
        files.sort(
            key = lambda f:
                os.path.getctime(os.path.join(directory,f))
        )
    else:
        files.sort()

    print(f"共找到 {len(files)} 个文件，将进行重命名...")
    
    index = start_index
    for original_name in files:
        ext = os.path.splitext(original_name)[1] # 获得文件后缀
        new_name = f"{base_name}{str(index).zfill(digits)}{ext}"
        src = os.path.join(directory,original_name)
        dst = os.path.join(directory,new_name)
        
        if os.path.exists(dst):
            print(f"⚠️ 已存在，跳过：{new_name}")
        else:
            os.rename(src,dst)
            print(f"✅ {original_name} → {new_name}")
            index +=1
            
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

def get_int_input(prompt, default=None):
    while True:
        value = input(prompt).strip()
        if not value and default is not None:
            return default
        try:
            return int(value)
        except ValueError:
            print("❌ 请输入有效的数字。")

if __name__ == "__main__":
    print("🛠 批量文件重命名工具")
    
    directory = input("📂 请输入目标文件夹路径：").strip()
    if not is_valid_directory(directory):
        print("❌ 输入路径无效")
        sys.exit(1)
    
    mode_choice = get_int_input("1 File_001++(默认)\n2 手动批量重命名\n模式选择：",default=1)
            
    if(mode_choice==1):
        base_name = input("📝 请输入基础名称（默认 File_）：").strip() or "File_"
        start_index = get_int_input("🔢 请输入起始编号（默认 1）：", default=1)
        digits = get_int_input("0️⃣ 请输入编号位数（默认 3）：", default=3)
        rename_files_in_format(directory, base_name, start_index, digits)
            
    elif(mode_choice==2):
        rename_files_in_sequence(directory)
    
    else:
        print("❌ 无效模式，程序退出。")