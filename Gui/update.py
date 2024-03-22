import tkinter as tk
from tkinter import ttk, messagebox
import psutil, subprocess, shutil, os, zipfile, urllib.request, threading

program_dir = "./"
current_process_id = str(os.getpid())

stop_event = threading.Event()

def cleanup_files():
    exclude_files = [".git", "update2.py", "runupdate.exe"]
    for file_name in os.listdir(program_dir):
        file_path = os.path.join(program_dir, file_name)
        if os.path.isfile(file_path) and file_name not in exclude_files:
            try:
                os.remove(file_path)
            except PermissionError:
                show_error_dialog(f"Unable to delete {file_path}. Please make sure no other NSBot windows are open or contact the developer.")
                terminate_process("runupdate.exe")
        elif os.path.isdir(file_path) and file_name != ".git" and file_name != "extract_temporary":
            try:
                shutil.rmtree(file_path)
            except PermissionError:
                show_error_dialog(f"Unable to delete {file_path}. Please make sure no other NSBot windows are open or contact the developer.")
                terminate_process("runupdate.exe")

def download_progress_hook(progress_var, progress_label, download_progress, total_file_size):
    def reporthook(count, block_size, total_size):
        downloaded = count * block_size
        percent = int(downloaded * 100 / total_size)
        downloaded_size = downloaded / (1024 * 1024)  # แปลงขนาดไฟล์ให้เป็นเมกะไบต์
        if percent <= download_progress:
            progress_var.set(percent)
            progress_label.configure(text=f"Downloading update : {int(progress_var.get())}%   ({downloaded_size:.3f} MB of {total_file_size} MB)...")
        else:
            progress_var.set(download_progress)
            progress_label.configure(text=f"Downloading update : {int(progress_var.get())}%   ({downloaded_size:.3f} MB of {total_file_size} MB)...")

    return reporthook

def download_and_extract(progress_var, progress_label):
    response = get_api()
    try:
        version = response["tag_name"]
        extract_dir = "extract_temporary"
    except:
        show_error_dialog("เกิดข้อผิดพลาดขณะดาวน์โหลดไฟล์อัพเดท")
        root.destroy()
        return
    zip_url = f"https://github.com/nsblollipop/NSBotUpdate/releases/download/{version}/NSBotUpdate.zip"
    zip_file_name = "NSBotUpdate.zip"
    total_file_size = round((response["assets"][0]["size"]  / (1024 * 1024)), 3)
    

    download_progress = 100
    try:
        urllib.request.urlretrieve(
            zip_url, zip_file_name, reporthook=download_progress_hook(progress_var, progress_label, download_progress, total_file_size)
        )
        
    except urllib.error.HTTPError:
        show_error_dialog("HTTPError: ดาวน์โหลดไฟล์ล้มเหลว")
        root.destroy()
        return
    except:
        show_error_dialog("เกิดข้อผิดพลาดขณะดาวน์โหลดไฟล์อัพเดท")
        root.destroy()
        return
    
    
    try:
        progress_label.configure(text=f"Extracting file..")
        with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
    except:
        progress_label.configure(text=f"Extracting file..")
        show_error_dialog("เกิดข้อผิดพลาดขณะแตกไฟล์")
        root.destroy()
        return

    os.remove(zip_file_name)

    cleanup_files()

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
        
        progress_var.set(download_progress)
        progress_label.configure(text=f"Done..")

    shutil.rmtree(extract_temp_dir)
    subprocess.Popen(['NSLaunch.exe'])
    root.destroy()

def get_api():
    import requests
    api_url = f"https://api.github.com/repos/nsblollipop/NSBotUpdate/releases/latest"
    headers = {
    "Authorization": "Bearer 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",
    "Accept": "application/vnd.github.v3+json"}
    getresponse = requests.get(api_url, headers=headers)
    response = getresponse.json()
    if getresponse:
        print('Connect to API with token')
        return response
    else:
        print ('Unable to connect GitHub API, change to connect without token')
        getresponse = requests.get(api_url)
        response = getresponse.json()
        return response

def start_update():
    thread = threading.Thread(target=download_and_extract, args=(progress_var, progress_label))
    thread.daemon = True  # ตั้งค่าให้เป็น daemon thread
    thread.start()

def show_error_dialog(message):
    messagebox.showerror("Error", message)

def terminate_process(process_name):
    for process in psutil.process_iter():
        try:
            if process.name() == process_name:
                process.terminate()
        except psutil.AccessDenied:
            pass

def on_closing():
    try:
        file_name = "rmzip.bat"
        file_content = "del NSBotUpdate.zip\nren runupdate.exe update.exe\ndel rmzip.bat"
        with open(file_name, "w") as file:
            file.write(file_content)
    except:
        pass
    subprocess.Popen(['rmzip.bat'], creationflags=subprocess.CREATE_NEW_CONSOLE)
    root.destroy()

root = tk.Tk()
root.title("NSBot Updating..")
root.geometry("500x110")

# root.resizable(False, False)

progress_var = tk.DoubleVar()
progress_label = tk.Label(root, text="Downloading update : 0%")

progress_bar = ttk.Progressbar(
    root, variable=progress_var, length=460, mode='determinate'
)
update_Label = tk.Label(text="กำลังดาวน์โหลดอัพเดท..", font=("Segoe UI", 10))
cancelbutton2 = ttk.Button(text="cancel", command=on_closing)
update_Label.pack(padx=20, pady=(10, 5), anchor="w")
progress_bar.pack(pady=5)
progress_label.pack(side="left", padx=20, pady=(5, 5))
cancelbutton2.pack(side="right", padx=20, pady=(5, 5))



x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
root.geometry("+{}+{}".format(x_cordinate-250, y_cordinate-100))

start_update()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
