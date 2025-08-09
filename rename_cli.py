# 批量重命名一个目录下所有文件（不包括子文件夹）
# 确认路径合法->保存文件原名称，生成目标名称，保证目标名称不重复->重命名
# 输入路径、名称格式
import os
import sys

# 输入路径时自动去掉多余引号+转为绝对路径
def normalize_path(path):
    return os.path.abspath(path.strip().strip('"').strip("'"))

def collect_paths():
    targets = []
    print("📂 请输入文件或文件夹路径（回车空行结束输入）：")
    while True:
        path = input(">").strip()
        if not path:    # 无输入跳过
            break
        path = normalize_path(path)
        if not os.path.exists(path):
            print("❌ 路径无效，请重新输入。")
            continue
        
        #检查是否为已添加路径的子路径
        conflict = False
        for t in targets:
            if os.path.commonpath([t["path"],path]) == t["path"]:
                print(f"⚠️ 已添加父路径 {t['path']}，不能再添加其子路径 {path}。")
                conflict = True
                break
        if conflict:
            continue
        
        if os.path.isfile(path):
            targets.append({"type":"file","path":path})
        elif os.path.isdir(path):
            choice = input(
                f"📁 检测到文件夹：{path}\n"
                "1 重命名该文件夹\n"
                "2 重命名该文件夹下所有文件（默认）\n请选择："
            ).strip() or "2"
            if choice == "1":
                targets.append({"type":"folder","path":path})
            elif choice == "2":
                targets.append({"type":"folder_files","path":path})
            else:
                print("⚠️ 选择无效，已跳过该路径。")
    return targets

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

def get_int_input(prompt, default=None):
    while True:
        value = input(prompt).strip()
        if not value and default is not None:
            return default
        try:
            return int(value)
        except ValueError:
            print("❌ 请输入有效的数字。")

def main():
    print("🛠 批量文件重命名工具")
    # 模式选择
    mode_choice = get_int_input("1 File_001++(默认)\n2 手动批量重命名\n模式选择：",default=1)
            
    if(mode_choice==1):
        directory = input("📂 请输入目标文件夹路径：").strip()
        if not directory:   # 用户直接回车
            print("❌ 输入路径不能为空")
            sys.exit(1)
        directory = normalize_path(directory)
        if not os.path.isdir(directory):
            print(f"{directory}")
            print("❌ 输入路径无效")
            sys.exit(1)
        base_name = input("📝 请输入基础名称（默认 File_）：").strip() or "File_"
        start_index = get_int_input("🔢 请输入起始编号（默认 1）：", default=1)
        digits = get_int_input("0️⃣ 请输入编号位数（默认 3）：", default=3)
        rename_files_in_format(directory, base_name, start_index, digits)
            
    elif(mode_choice==2):
        # 批量文件选择
        targets = collect_paths()
        if not targets:
            print("❌ 没有选择任何文件或文件夹，程序结束。")
            return
        print("✅ 已选择以下文件：")
        for t in targets:
            print(f"- {t['type']}: {t['path']}")
        
        for t in targets:
            if t["type"]=="file" or t["type"]=="folder":
                rename_single_file_or_folder(t["path"])
            elif t["type"]=="folder_files":
                rename_files_in_sequence(t["path"])
        
    else:
        print("❌ 无效模式，程序退出。")

if __name__ == "__main__":
    main()
    
    
    
    