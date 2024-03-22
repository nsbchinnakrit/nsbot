import tkinter as tk, threading, urllib.request, zipfile, os, shutil, subprocess, psutil, sys
from tkinter import messagebox

def cleanup_files():
# ระบุโฟลเดอร์ของโปรแกรม
    program_dir = "./"
    # ลบไฟล์ในโฟลเดอร์ของโปรแกรม (ยกเว้นโฟลเดอร์ .git และ extract_temporary)
    for file_name in os.listdir(program_dir):
        file_path = os.path.join(program_dir, file_name)
        if os.path.isfile(file_path) and file_name != ".git" and file_name not in ["runupdate.exe"]:
            try:
                os.remove(file_path)
            except PermissionError:
                messagebox.showerror("Error", "ไม่สามารถลบ {}\nกรุณาตรวจสอบว่า NSBot หน้าต่างอื่น เปิดอยู่หรือไม่\nหรือติดต่อผู้พัฒนา".format(file_path))
                for process in psutil.process_iter():
                    try:
                        if process.name() == "runupdate.exe":
                            # ปิดกระบวนการที่เกี่ยวข้องกับ gui.exe
                            process.terminate()
                    except psutil.AccessDenied:
                        pass
        elif os.path.isdir(file_path) and file_name != ".git" and file_name != "extract_temporary":
            try:
                shutil.rmtree(file_path)
            except PermissionError:
                messagebox.showerror("Error", "ไม่สามารถลบ {}\nกรุณาตรวจสอบว่า NSBot หน้าต่างอื่น เปิดอยู่หรือไม่\nหรือติดต่อผู้พัฒนา".format(file_path))
                for process in psutil.process_iter():
                    try:
                        if process.name() == "runupdate.exe":
                            # ปิดกระบวนการที่เกี่ยวข้องกับ gui.exe
                            process.terminate()
                    except psutil.AccessDenied:
                        pass
    # ย้ายไฟล์และโฟลเดอร์จาก extract_temporary ไปยังโฟลเดอร์ของโปรแกรม
    extract_temp_dir = os.path.join(program_dir, "extract_temporary")
    for file_name in os.listdir(extract_temp_dir):
        file_path = os.path.join(extract_temp_dir, file_name)
        if os.path.isfile(file_path) or os.path.isdir(file_path):
            if file_name in ["update.exe"]:
                destination_path = os.path.join(program_dir, file_name)
                if not os.path.exists(destination_path):
                    shutil.move(file_path, program_dir)
            else:
                destination_path = os.path.join(program_dir, file_name)
                if os.path.exists(destination_path):
                    if os.path.isfile(destination_path):
                        os.remove(destination_path)
                    else:
                        shutil.rmtree(destination_path)
                shutil.move(file_path, program_dir)
    # ลบโฟลเดอร์ extract_temporary
    shutil.rmtree(extract_temp_dir)
def download_and_extract():
    version = get_api()
    zip_url = f"https://github.com/nsblollipop/NSBotUpdate/releases/download/{version}/NSBotUpdate.zip"
    zip_file_name = "NSBotUpdate.zip"
    extract_dir = "extract_temporary"
    try: #ดาวน์โหลดไฟล์
        urllib.request.urlretrieve(zip_url, zip_file_name)
    except urllib.error.HTTPError:
        messagebox.showerror("HTTPError", "เกิดข้อผิดพลาด ไม่สามารถดาวน์โหลดไฟล์สำหรับอัพเดท")
        root.destroy()
    except:
        messagebox.showerror("Error", "เกิดข้อผิดพลาดเกี่ยวกับการดาวน์โหลดไฟล์")
        root.destroy()

    try: #แตกไฟล์
        with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
    except:
        messagebox.showerror("Error", "เกิดข้อผิดพลาดขณะติดตั้งอัพเดท")
        root.destroy()

    os.remove(zip_file_name)

    cleanup_files()
    subprocess.Popen(['NSLaunch.exe'])
    root.destroy()

def start_download_and_extract():
    # สร้างเธรดสำหรับดาวน์โหลดและแตกไฟล์
    thread = threading.Thread(target=download_and_extract)
    # กำหนดให้เธรดทำงานเป็นแบบ Daemon เพื่อปิดโปรแกรมได้หากผู้ใช้ปิดหน้าต่าง
    thread.daemon = True
    # เริ่มเธรด
    thread.start()

def on_closing():
    if messagebox.askokcancel("ออก", "คุณต้องการออกจากโปรแกรมหรือไม่?"):
        root.destroy()

def get_api():
    import requests
    api_url = f"https://api.github.com/repos/nsblollipop/NSBotUpdate/releases/latest"
    headers = {
    "Authorization": "Bearer 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",
    "Accept": "application/vnd.github.v3+json"}
    try:
        print ('API Connect With token')
        getresponse = requests.get(api_url, headers=headers)
        latest_version = getresponse.json()["tag_name"]
        print ("Check latest version : %s"%latest_version)
        return latest_version
    except:
        print ('API Connect Without token')
        getresponse = requests.get(api_url)
        latest_version = getresponse.json()["tag_name"]
        print ("Check latest version : %s"%latest_version)
        return latest_version

def move(event):
    root.geometry(f'+{event.x_root-137}+{event.y_root-33}')

if __name__ == "__main__":
    root = tk.Tk()
    root.config(bg='#C3C3C3')
    root.geometry('272x62')
    root.title("NSBot Update")

    update_frame = tk.LabelFrame(root)
    update_frame.grid(padx=(15), pady=(15))
    update_Label = tk.Label(update_frame, text="\n\nกำลังดาวน์โหลดอัพเดท กรุณารอสักครู่..\n\n", font=("Segoe UI",  12))
    update_frame.pack(padx=(5), pady=(5))
    update_Label.pack(padx=(10), pady=(5))
    root.update()

    try:
        start_download_and_extract()
    except:
        sys.exit()
        
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))
    root.overrideredirect(1)
    root.attributes('-topmost', True)
    root.bind('<B1-Motion>',move)
    root.mainloop()