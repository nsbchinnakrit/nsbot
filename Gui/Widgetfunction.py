from tkinter import messagebox
import os, subprocess, tkinter as tk, win32process, psutil, win32gui

proc_pid=0
default_delay=0.01
stablemode_delay=0.04

class Widgetfunc():
    def __init__(self, parent, **kwargs):
        self.root = parent
        self.var_sv = kwargs.get('var_sv')
        self.var_gamdmode = kwargs.get('var_gamdmode')
        self.var_wq = kwargs.get('var_wq')
        self.var_team = kwargs.get('var_team')
        self.var_showlog = kwargs.get('var_showlog')
        self.var_shutdown = kwargs.get('var_shutdown')
        self.var_closegame = kwargs.get('var_closegame')
        self.team = kwargs.get('team')
        self.entry1 = kwargs.get('entry1')
        self.entry2 = kwargs.get('entry2')
        self.entry3 = kwargs.get('entry3')
        self.entry4 = kwargs.get('entry4')
        self.accentbutton = kwargs.get('accentbutton')
        self.accentbutton2 = kwargs.get('accentbutton2')
        self.radio_1 = kwargs.get('radio_1')
        self.radio_2 = kwargs.get('radio_2')
        self.radio_3 = kwargs.get('radio_3')
        self.solo = kwargs.get('solo')
        self.acq = kwargs.get('acq')
        self.rfq = kwargs.get('rfq')
        self.gamemode1 = kwargs.get('gamemode1')
        self.gamemode2 = kwargs.get('gamemode2')
        self.gamemode3 = kwargs.get('gamemode3')
        self.gamemode4 = kwargs.get('gamemode4')
        self.gamemode5 = kwargs.get('gamemode5')
        self.gamemode6 = kwargs.get('gamemode6')
        self.aboutround = kwargs.get('aboutround')
        self.switch = kwargs.get('switch')
        self.displaysizebtn = kwargs.get('displaysizebtn')
        self.shutdown = kwargs.get('shutdown')
        self.closewindow = kwargs.get('closewindow')
        # self.resetdelay = kwargs.get('resetdelay')
    
    def disabled_team(self, round='30', findimg='0.02'):
        self.var_team.set(1)
        self.team.config(state='disabled')
        self.entry2.delete(0, 100)
        self.entry2.insert(0, round)
        self.entry3.delete(0, 100)
        self.entry3.insert(0, findimg)
        self.aboutround.grid_forget()
    
    def explorerealm(self, round='30', findimg='0.02'):
        self.var_team.set(1)
        self.team.config(state='disabled')
        self.entry2.delete(0, 100)
        self.entry2.insert(0, round)
        self.entry3.delete(0, 100)
        self.entry3.insert(0, findimg)
        self.aboutround.config(width=6)
        self.aboutround.grid(row=0, column=1, padx=(98, 0), pady=(2, 0), sticky="s")
    
    def enable_team(self, round='500', findimg=default_delay):
        self.team.config(state='normal')
        self.entry2.delete(0, 100)
        self.entry2.insert(0, round)
        self.entry3.delete(0, 100)
        self.entry3.insert(0, findimg)
        self.aboutround.grid_forget()
    
    def showaboutmode5(self):
        messagebox.showinfo("Explore/Realm",
                             "รอบของโหมดนี้ จะนับจากการที่บัตรเขตเต็ม (30) และตอนที่บัตรเขตหมด\n\nตัวอย่าง : กำหนดรอบเป็น 2 แล้วบัตรเขตยังไม่ถึง 30 ระบบจะเปิดโหมดสำรวจ\nเมื่อบัตรเขตถึง 30 จะนับรอบ = 1 และเปิดโหมด RealmRaid และเมื่อบัตรเขตหมด จะนับรอบ = 2 : ถ้าหากมีรอบเยอะกว่านี้ = วนกลับไปเงื่อนไขแรกใหม่")
    
    def check_wanted(self):
        wanteddata='False'
        if proc_pid != 0:
            if Temp.read_wanted_temp() != wanteddata:
                self.coop_notify(data=wanteddata)
            else:
                self.root.after(1000, self.check_wanted)
        else:
            pass

    def coop_notify(self, data):
        def handle_click(event):
            temp_wanted_path = f"runprocess/wanted{proc_pid}.txt"
            if proc_pid != 0:
                with open(temp_wanted_path, "w") as file:
                    file.write(data)
                    file.close
                self.root.after(1000, self.check_wanted)
            else:
                pass
            self.root.attributes('-topmost', False)
            child.destroy()
        child = tk.Toplevel(self.root)
        child.title("NSBot Update")
        child.geometry('440x52')
        child.config(bg='#00BCFF')
        nofity_frame = tk.LabelFrame(child)
        nofity_frame.grid(padx=(15), pady=(15))
        nofity_Label = tk.Label(nofity_frame, text=f"ระบบพบการส่ง co-op quest โปรดตรวจสอบเควสหลังจบการทำงาน", font=("Segoe UI",  12))
        nofity_frame.pack(padx=(5), pady=(5))
        nofity_Label.pack(padx=(10), pady=(5))
        child.update()
        child.minsize(child.winfo_width(), child.winfo_height())
        x_cordinate = self.root.winfo_x() + int(self.root.winfo_width() / 2) - int(child.winfo_width() / 2)
        y_cordinate = self.root.winfo_y() + int(self.root.winfo_height() / 2) - int(child.winfo_height() / 2)
        child.geometry("+{}+{}".format(x_cordinate, y_cordinate-0))
        child.overrideredirect(1)
        self.root.attributes('-topmost', True)
        child.attributes('-topmost', True)
        child.bind('<Leave>', handle_click)
        child.mainloop()

    def update_round(self):
        global total, proc_pid
        if proc_pid != 0:
            try:
                self.entry2.config(state='normal')
                self.entry2.delete(0, 'end')
                self.entry2.insert(0, Temp.read_temp())
                self.entry2.config(state='disabled')
                self.root.after(1000, self.update_round)
            except:
                self.entry2.config(state='normal')
                self.entry2.delete(0, 'end')
                self.entry2.insert(0, total)
                self.alway_disable_btn()
        else:
                self.entry2.config(state='normal')
                self.entry2.delete(0, 'end')
                self.entry2.insert(0, total)
    
    def toggle_shutdown(self):
        self.var_closegame.set(0)
    
    def toggle_closewindow(self):
        self.var_shutdown.set(0)

    def set_shutdown(self):
        global total, roundend
        after_id = self.root.after(1000, self.set_shutdown)
        if int(total) <= int(roundend):
            subprocess.run(['shutdown', '-s', '-f', '-t', '10'], creationflags=subprocess.CREATE_NO_WINDOW)
            self.root.after_cancel(after_id)

    def set_closegame(self):
        global total, hwnd
        tid, pid = win32process.GetWindowThreadProcessId(hwnd)
        after_id = self.root.after(1000, self.set_closegame)
        if int(total) <= int(roundend):
            subprocess.run(['taskkill', '/F', '/PID', str(pid)], creationflags=subprocess.CREATE_NO_WINDOW)
            self.root.after_cancel(after_id)
    
    def force_kill(self):
        global proc_pid
        after_id = self.root.after(1000, self.force_kill)
        if proc_pid != 0:
            if int(total) <= int(roundend):
                try:
                    print ('Force Kill:%s'%proc_pid)
                    subprocess.run(['taskkill', '/F', '/PID', str(proc_pid)], creationflags=subprocess.CREATE_NO_WINDOW)
                    self.root.after_cancel(after_id)
                except:
                    self.root.after(1000, self.force_kill)
            else:
                pass
        else:
            self.root.after_cancel(after_id)

    def check_pid_alive(self):
        after_id = self.root.after(2000, self.check_pid_alive)
        try:
            psutil.Process(proc_pid)
        except psutil.NoSuchProcess:
            self.botstop()
            self.root.after_cancel(after_id)
        
    def chang_to_gb(self):
        global getserver
        getserver = 'GB'
        self.var_sv.set('GB')
        self.entry1.delete(0, 100)
        self.entry1.insert(0, "Onmyoji")
    
    def chang_to_cn(self):
        global getserver
        getserver = 'CN'
        self.var_sv.set('CN')
        self.entry1.delete(0, 100)
        self.entry1.insert(0, "阴阳师-网易游戏")
    
    def chang_to_jp(self):
        global getserver
        getserver = 'JP'
        self.var_sv.set('JP')
        self.entry1.delete(0, 100)
        self.entry1.insert(0, "Onmyoji")
    
    def resize_wnd(self):
        global hwnd
        GetwindowName=self.entry1.get()
        hwnd = win32gui.FindWindow(None, GetwindowName)
        x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
        w = x1 - x0
        h = y1 - y0
        if h == 679:
            print(hwnd)
        else:
            win32gui.MoveWindow(hwnd, x0, y0, 1493, 679, True)
    
    def resetdelay(self):
        if self.var_gamdmode.get() == 2:
            self.entry3.delete(0, 100)
            self.entry3.insert(0, stablemode_delay)
        else:
            self.entry3.delete(0, 100)
            self.entry3.insert(0, default_delay)
        self.entry4.delete(0, 100)
        self.entry4.insert(0, "0")

    def disable_button(self, thisstate='normal'):
        objects = [
            self.entry1, self.entry3, self.entry4,
            self.radio_1, self.radio_2, self.radio_3,
            self.solo, self.team, self.acq, self.rfq,
            self.gamemode1, self.gamemode2, self.gamemode3, self.gamemode4, self.gamemode5, self.gamemode6,
            self.switch, self.displaysizebtn,
            self.shutdown, self.closewindow
        ]
        # ปรับสถานะของวัตถุทั้งหมดในรายการ
        for obj in objects:
            obj.config(state=thisstate)
    
    def alway_disable_btn(self):
        if self.var_gamdmode.get() == 1 or self.var_gamdmode.get() == 2 or self.var_gamdmode.get() == 3 or self.var_gamdmode.get() == 4 or self.var_gamdmode.get() == 6:
                self.entry2.config(state='normal')
        else:
            self.team.config(state='disabled')

    def botstart(self):
        global proc_pid, gameMode, windowName, hwnd, total
        if self.var_gamdmode.get() == 1 and self.var_team.get() == 1: #Soul Single
            gameMode=str('SingleSoul')
        if self.var_gamdmode.get() == 1 and self.var_team.get() == 2: #Soul Team
            gameMode=str('Soul')
        if self.var_gamdmode.get() == 2 and self.var_team.get() == 1: #Explore Single:
            gameMode=str('SingleExplore')
        if self.var_gamdmode.get() == 2 and self.var_team.get() == 2: #Explore Team:
            gameMode=str('Explore')
        if self.var_gamdmode.get() == 4: # Guild Realm Raid:
            gameMode=str('GuildRealmRaid')
        if self.var_gamdmode.get() == 3: # 3Realm Raid:
            gameMode=str('RealmRaid')
            # gameMode=str('RealmRaidW3F3')
        if self.var_gamdmode.get() == 5: #3Realm Raid and Explore:
            gameMode=str('Explor3Realm')
        if self.var_gamdmode.get() == 6: #Event:
            gameMode=str('Event')
        if self.var_showlog.get() == 0:
            subprocesstype = subprocess.CREATE_NO_WINDOW
        if self.var_showlog.get() != 0:
            subprocesstype = subprocess.CREATE_NEW_CONSOLE
        self.resize_wnd()
        Server=self.var_sv.get()
        windowName=str(hwnd)
        total=int(self.entry2.get())
        wanted=self.var_wq.get()
        wtdelay=self.entry4.get()
        findimgdelay=self.entry3.get()
        shutd=self.var_shutdown.get()
        closewd=self.var_closegame.get()
        startupinfo = subprocess.STARTUPINFO()
        args = [gameMode, Server, windowName, str(total), wanted, wtdelay, findimgdelay]
        try:
            proc = subprocess.Popen(['runprocess/runprocess.exe'] + args, startupinfo=startupinfo, creationflags=subprocesstype)
        except OSError:
            proc = subprocess.Popen(['python', 'runprocess.py'] + args, startupinfo=startupinfo, creationflags=subprocesstype)
        except:
            pass
        proc_pid = (proc.pid)
        
        print('PID:%s | Start:%s' % (proc.pid, args))
        Temp.create_file()
        self.accentbutton.config(text="Stop", style="Different.TButton", command=self.botstop)
        self.accentbutton2.config(text="Stop", style="Different.TButton", command=self.botstop)
        self.disable_button('disabled')
        self.check_pid_alive()
        self.update_round()
        self.check_wanted()
        self.force_kill()
        if shutd == 1:
            print("Shutdown when end.")
            self.set_shutdown()
        if closewd == 1:
            print("Close Game Window when end.")
            self.set_closegame()
        
            
    def botstop(self):
        global proc_pid
        print('Killed PID:%s | GameMode:%s'% (proc_pid, gameMode))
        Temp.remove_tempfile()
        try:
            os.kill(proc_pid, 9)
            proc_pid = 0
            self.update_round()
        except OSError:
            proc_pid = 0
            self.accentbutton.config(text="Start", style="Accent.TButton", command=self.botstart)
            self.accentbutton2.config(text="Start", style="Accent.TButton", command=self.botstart)
            self.disable_button('enabled')
            self.alway_disable_btn()
            return False
        else:
            proc_pid = 0
            self.accentbutton.config(text="Start", style="Accent.TButton", command=self.botstart)
            self.accentbutton2.config(text="Start", style="Accent.TButton", command=self.botstart)
            self.disable_button('enabled')
            self.alway_disable_btn()
            return True


class Temp():
    def create_file():
        global temp_path
        temp_path = f"runprocess/temp{proc_pid}.txt"
        with open(temp_path, "w") as file:
            file.write("0")
            file.close

    def remove_tempfile():
        global temp_path, roundend
        temp_wanted_path = f"runprocess/wanted{proc_pid}.txt"
        try:
            with open(temp_path, "r") as file:
                data = file.read()
                roundend = data
            os.remove(temp_path)
            os.remove(temp_wanted_path)
        except:
            pass
    
    def send_proc_pid():
        global proc_pid
        if proc_pid != 0:
            print ('Kill PID:%s'%proc_pid)
            os.kill(proc_pid, 0)
            os.kill(proc_pid, 9)
            Temp.remove_tempfile()
        else:
            pass
        
    def read_temp():
        global temp_path, total, proc_pid, roundend
        while True:
            try:
                with open(temp_path, "r") as file:
                    data = file.read()
                    round_text = "%s / %s"%(data, total)
                    roundend = data
                    return round_text
            except FileNotFoundError:
                return roundend
            except proc_pid == 0:
                return roundend
    
    def read_wanted_temp():
        temp_wanted_path = f"runprocess/wanted{proc_pid}.txt"
        while True:
            try:
                with open(temp_wanted_path, "r") as file:
                    data = file.read()
                    return data
            except FileNotFoundError:
                round_text = "False"
                return round_text
            except proc_pid == 0:
                round_text = "False"
                return round_text
