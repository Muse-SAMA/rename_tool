# 批量重命名一个目录下所有文件（不包括子文件夹）
# 确认路径合法->保存文件原名称，生成目标名称，保证目标名称不重复->重命名
# 输入路径、名称格式
import os

def rename_files_in_directory(directory,base_name="File_",start_index=1,digits=3):
    if not os.path.exists(directory):
        print(f"指定路径不是一个有效目录：{directory}")
        return
    
    files = [
        f for f in os.listdir(directory) 
        if os.path.isfile(os.path.join(directory,f))
    ]
    files.sort(
        key = lambda f:
            os.path.getctime(os.path.join(directory,f))
    )
    
    print(f"共找到 {len(files)} 个文件，将进行重命名...")
    
    index = start_index
    for original_name in files:
        ext = os.path.splitext(original_name)[1]
        new_name = f"{base_name}{str(index).zfill(digits)}{ext}"
        src = os.path.join(directory,original_name)
        dst = os.path.join(directory,new_name)
        
        if os.path.exists(dst):
            print(f"⚠️ 目标文件已存在，跳过：{new_name}")
        else:
            os.rename(src,dst)
            print(f"✅ {original_name} → {new_name}")
            index +=1
            
if __name__ == "__main__":
    print("🛠 批量文件重命名工具")
    directory = input("📂 请输入目标文件夹路径：").strip()
    base_name = input("📝 请输入基础名称（默认 File_）：").strip() or "File_"
    start = input("🔢 请输入起始编号（默认 1）：").strip()
    digits = input("0️⃣ 请输入编号位数（默认 3）：").strip()
    
    try:
        start_index = int(start) if start else 1
        digit_count = int(digits) if digits else 3
        rename_files_in_directory(directory, base_name,start_index,digit_count)
    except ValueError:
        print("❌ 输入的编号或位数不是有效数字，请重新运行。")