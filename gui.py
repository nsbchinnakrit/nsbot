import tkinter as tk
from tkinter import ttk, font, messagebox
from Gui.Widgetfunction import Widgetfunc, Temp
import subprocess, psutil, os, pywintypes, win32gui, win32process, json, requests, threading

proc_pid=0
temp_path={}
default_delay=0.01
stablemode_delay=0.04
total=0
roundend=0

class MainGUI(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)
        
        # Creating a Font object of "TkDefaultFont"
        self.defaultFont = font.nametofont("TkDefaultFont")

        # Overriding default-font with custom settings
        # i.e changing font-family, size and weight
        self.defaultFont.configure(family="Segoe UI", size=10)
        
        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        self.var_sv = tk.StringVar(value='GB')
        self.var_gamdmode = tk.IntVar(value=1)
        self.var_wq = tk.StringVar(value=1)
        self.var_team = tk.IntVar(value=1)
        self.var_showlog = tk.IntVar(value=0)
        self.var_shutdown = tk.IntVar(value=0)
        self.var_closegame = tk.IntVar(value=0)

        # ttk.Style().theme_use('default')
        ttk.Style().map("TNotebook.Tab", foreground=[("selected", 'black')]);
        ttk.Style().configure("TNotebook.Tab", background='black', foreground='gray');
        
        # Create widgets :)
        self.setup_widgets()

        self.widgetfunc = Widgetfunc(parent, var_sv=self.var_sv, var_gamdmode=self.var_gamdmode, var_wq=self.var_wq,
                        var_team=self.var_team, var_showlog=self.var_showlog, var_shutdown=self.var_shutdown,
                        var_closegame=self.var_closegame, team=self.team, entry1=self.entry1, entry2=self.entry2, entry3=self.entry3, entry4=self.entry4,
                        accentbutton=self.accentbutton, accentbutton2=self.accentbutton2, radio_1=self.radio_1, radio_2=self.radio_2, radio_3=self.radio_3,
                        solo=self.solo, acq=self.acq, rfq=self.rfq, gamemode1=self.gamemode1, gamemode2=self.gamemode2, gamemode3=self.gamemode3,
                        gamemode4=self.gamemode4, gamemode5=self.gamemode5, gamemode6=self.gamemode6, aboutround=self.aboutround, switch=self.switch, displaysizebtn=self.displaysizebtn,
                        shutdown=self.shutdown, closewindow=self.closewindow)

    def setup_widgets(self):
        # Create a Frame for Window Name Input ==================================================================
        self.widgets_frame = ttk.LabelFrame(self, text="window name", padding=(0, 0))
        self.widgets_frame.grid(
            row=0, column=0, padx=20, pady=(1, 1), sticky="nsew", rowspan=1 ,columnspan=3)
        self.widgets_frame.columnconfigure(index=0, weight=0)
        
        # Entry window name
        self.entry1 = ttk.Entry(self.widgets_frame, font=("Segoe UI",  10))
        self.entry1.insert(0, "Onmyoji")
        self.entry1.grid(row=0, column=1, padx=(15,0), pady=(0, 10), ipadx=80, sticky="nsew")

        # Accentbutton
        self.displaysizebtn = ttk.Button(
            self.widgets_frame, text="default size", style="Accent.TButton", command=lambda: self.widgetfunc.resize_wnd())
        self.displaysizebtn.grid(row=0, column=1, padx=10, pady=(0, 10), sticky="e")

        # Radiobuttons #=========================================================================================
        self.radio_1 = ttk.Radiobutton(
            self.widgets_frame, text="Globle", variable=self.var_sv, value='GB', command=lambda: self.widgetfunc.chang_to_gb())
        self.radio_1.grid(row=0, column=3, padx=(20, 15), pady=(10, 15), sticky="nsew")

        self.radio_2 = ttk.Radiobutton(
            self.widgets_frame, text="Japanese", state="", variable=self.var_sv, value='JP', command=lambda: self.widgetfunc.chang_to_jp())
        self.radio_2.grid(row=0, column=4, padx=(0, 0), pady=(10, 15), sticky="nsew")

        self.radio_3 = ttk.Radiobutton(
            self.widgets_frame, text="Chinese", state="", variable=self.var_sv, value='CN', command=lambda: self.widgetfunc.chang_to_cn())
        self.radio_3.grid(row=0, column=5, padx=(15,0), pady=(10, 15), sticky="nsew")
        
        # Tab #==============================================================================================
        # Panedwindow
        self.paned = ttk.PanedWindow(self)
        self.paned.grid(row=1, column=0, padx=(15,15), pady=(0, 15), ipady=1, sticky="nsew", rowspan=1, columnspan=2)

        # Notebook, pane #2
        self.pane = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane, weight=3)

        # Notebook, pane #2
        self.notebook = ttk.Notebook(self.pane)
        self.notebook.pack(fill="both", expand=True)

        #===================================================Tab #1=========================================================================================
        # Tab #1
        self.tab_1 = ttk.Frame(self.notebook)
        for index in [0, 1]:
            self.tab_1.columnconfigure(index=index, weight=1)
            self.tab_1.rowconfigure(index=index, weight=1)
        self.notebook.add(self.tab_1, text="   Game Mode Settings   ")
        

        # Team #=========================================================================================
        self.team_frame = ttk.LabelFrame(self.tab_1, text="Team Option", padding=(0, 0))
        self.team_frame.grid(row=0, column=0, padx=(15,0), pady=(5, 0), sticky="nsew", rowspan=1, columnspan=1)

        self.solo = ttk.Radiobutton(self.team_frame, text="Solo", variable=self.var_team, value='1')
        self.solo.grid(row=0, column=0, padx=15, pady=(5, 0), sticky="nsew")

        self.team = ttk.Radiobutton(self.team_frame, text="Team", variable=self.var_team, value='2')
        self.team.grid(row=1, column=0, padx=15, pady=(5, 0), sticky="nsew")
        
        # Wanted #=========================================================================================================================================
        self.wantedquest_frame = ttk.LabelFrame(self.tab_1, text="Wanted Quest", padding=(0, 0))
        self.wantedquest_frame.grid(row=0, column=0, padx=(15,0), pady=(90, 0), sticky="nsew", rowspan=1, columnspan=1)

        self.acq = ttk.Radiobutton(self.wantedquest_frame, text="Accept", variable=self.var_wq, value='2')
        self.acq.grid(row=0, column=0, padx=15, pady=(5, 0), sticky="nw")

        self.rfq = ttk.Radiobutton(self.wantedquest_frame, text="Refuse", variable=self.var_wq, value='1')
        self.rfq.grid(row=1, column=0, padx=15, pady=(5, 0), sticky="nw")
        
        # GameMode #=======================================================================================================================================
        self.gamemode_frame = ttk.LabelFrame(self.tab_1, text="Select Game Mode", padding=(0, 0))
        self.gamemode_frame.grid(row=0, column=1, padx=(15,15), pady=(5, 0), sticky="nsew", rowspan=1, columnspan=1)

        self.gamemode1 = ttk.Radiobutton(
            self.gamemode_frame, text="Soul/Evo", variable=self.var_gamdmode, value='1', command=lambda: self.widgetfunc.enable_team('500', default_delay))
        self.gamemode1.grid(row=0, column=1, padx=(30,0), pady=(10, 0), sticky="nw")

        self.gamemode2 = ttk.Radiobutton(
            self.gamemode_frame, text="Explore", state='', variable=self.var_gamdmode, value='2', command=lambda: self.widgetfunc.enable_team('500', stablemode_delay))
        self.gamemode2.grid(row=0, column=2, padx=(0,0), pady=(10, 0), sticky="nw")

        self.gamemode3 = ttk.Radiobutton(
            self.gamemode_frame, text="Realm Raid (3)", variable=self.var_gamdmode, value='3', command=lambda: self.widgetfunc.disabled_team('30', default_delay))
        self.gamemode3.grid(row=0, column=1, padx=(30,0), pady=(45, 0), sticky="nw")

        self.gamemode4 = ttk.Radiobutton(
            self.gamemode_frame, text="Guild Realm", variable=self.var_gamdmode, value='4', command=lambda: self.widgetfunc.disabled_team('200', default_delay))
        self.gamemode4.grid(row=0, column=2, padx=(0,0), pady=(45, 0), sticky="nw")

        self.gamemode5 = ttk.Radiobutton(
            self.gamemode_frame, text="Explore/Realm", variable=self.var_gamdmode, value='5', command=lambda: self.widgetfunc.explorerealm('4', stablemode_delay))
        self.gamemode5.grid(row=0, column=3, padx=(0,0), pady=(45, 0), sticky="nw")

        self.gamemode6 = ttk.Radiobutton(
            self.gamemode_frame, text="Event : Kujaku", state='normal',variable=self.var_gamdmode, value='6', command=lambda: self.widgetfunc.disabled_team('300', default_delay))
        self.gamemode6.grid(row=0, column=3, padx=(0,0), pady=(10, 0), sticky="nw")

        # Separator #=====================================================================================================================================
        self.separator = ttk.Separator(self.gamemode_frame)
        self.separator.grid(row=0, column=2, padx=(10, 10), pady=(88,0), ipadx=110, sticky="nw", columnspan=4)

        #Total Round #====================================================================================================================================
        self.round_frame = ttk.LabelFrame(self.gamemode_frame, text="Total Round", padding=(0, 0))
        self.round_frame.grid(row=0, column=1, padx=(15), pady=(0, 0), sticky="s", rowspan=1, columnspan=1, ipady=6)
        self.entry2 = ttk.Entry(self.round_frame, font=("Segoe UI",  10))
        self.entry2.insert(0, "500")
        self.entry2.grid(row=0, column=1, padx=10, pady=(10, 2), sticky="e")

        self.aboutround = ttk.Button(self.round_frame, text="info", command=lambda: self.widgetfunc.showaboutmode5())
        self.aboutround.config(default='disabled',)
        # self.aboutround.grid(row=0, column=1, padx=(80, 0), pady=(8, 0), sticky="s")
        self.aboutround.grid_forget()

        # Switch #========================================================================================================================================
        self.switch = ttk.Checkbutton(self.gamemode_frame, text="console log", style="Switch.TCheckbutton", variable=self.var_showlog)
        self.switch.grid(row=0, column=2, padx=(40,0), pady=(104, 14), sticky="e")

        # start button #==================================================================================================================================
        self.accentbutton = ttk.Button(self.gamemode_frame, text="Start", style="Accent.TButton", command=lambda: self.widgetfunc.botstart())
        self.accentbutton.grid(row=0, column=3, padx=15, pady=(106, 14), sticky="e")
        #===================================================Tab #1=========================================================================================

        #===================================================Tab #2=========================================================================================
         # Tab #2
        self.tab_2 = ttk.Frame(self.notebook)
        for index in [0, 1]:
            self.tab_2.columnconfigure(index=index, weight=1)
            self.tab_2.rowconfigure(index=index, weight=1)
        self.notebook.add(self.tab_2, text="   Other Settings   ")

        #Delay
        self.delay_frame = ttk.LabelFrame(self.tab_2, text="Find Image Delay", padding=(0, 0))
        self.delay_frame.grid(row=0, column=0, padx=(5), pady=(30, 5), sticky="nw", rowspan=1, columnspan=1)
        self.entry3 = ttk.Entry(self.delay_frame, font=("Segoe UI",  10))
        self.entry3.insert(0, default_delay)
        self.entry3.grid(row=0, column=0, padx=15, pady=(10, 10), sticky="nsew")
        self.secondtext = ttk.Label(self.delay_frame, text="  second  ", font=("Segoe UI",  10), padding=(0, 10))
        self.secondtext.grid(row=0, column=0, padx=(100,10), pady=(0, 0), sticky="nw")

        #Wanted Delay
        self.delay_frame2 = ttk.LabelFrame(self.tab_2, text="Check Wanted Delay", padding=(0, 0))
        self.delay_frame2.grid(row=0, column=1, padx=(5), pady=(30, 5), sticky="nw", rowspan=1, columnspan=1)
        self.entry4 = ttk.Entry(self.delay_frame2, font=("Segoe UI",  10))
        self.entry4.insert(0, "0")
        self.entry4.grid(row=0, column=0, padx=15, pady=(10, 10), sticky="nsew")
        self.secondtext = ttk.Label(self.delay_frame2, text="  second  ", font=("Segoe UI",  10), padding=(0, 10))
        self.secondtext.grid(row=0, column=0, padx=(100,10), pady=(0, 0), sticky="nw")

        #Loop Delay1
        self.delay_frame = ttk.LabelFrame(self.tab_2, text="Find Img Loop Delay", padding=(0, 0))
        self.delay_frame.grid(row=0, column=2, padx=(5), pady=(30, 5), sticky="nw", rowspan=1, columnspan=1)
        self.entry5 = ttk.Entry(self.delay_frame, font=("Segoe UI",  10))
        self.entry5.insert(0, "0")
        self.entry5.config(state='disabled')
        self.entry5.grid(row=0, column=0, padx=15, pady=(10, 10), sticky="nsew")
        self.secondtext = ttk.Label(self.delay_frame, text="  second  ", font=("Segoe UI",  10), padding=(0, 10))
        self.secondtext.grid(row=0, column=0, padx=(100,10), pady=(0, 0), sticky="nw")

        #################################################################################################################
        # Separator
        self.separator = ttk.Separator(self.tab_2)
        self.separator.grid(row=1, column=1, padx=(10, 10), pady=(11,0), ipadx=130, sticky="ne", columnspan=2)

        self.option_frame = ttk.LabelFrame(self.tab_2, text="ตัวเลือกเมื่อดำเนินการถึงรอบที่กำหนด", padding=(0, 0))
        self.option_frame.grid(row=1, column=0, padx=(5), pady=(1, 0), sticky="nw", rowspan=1, columnspan=2)

        self.shutdown = ttk.Checkbutton(self.option_frame, text="ปิดเครื่อง", style="Switch.TCheckbutton", variable=self.var_shutdown, command=lambda: self.widgetfunc.toggle_shutdown())
        self.shutdown.grid(row=1, column=0, padx=(15,0), pady=(12, 15), sticky="w")

        self.closewindow = ttk.Checkbutton(self.option_frame, text="ปิดหน้าต่างเกม", style="Switch.TCheckbutton", variable=self.var_closegame, command=lambda: self.widgetfunc.toggle_closewindow())
        self.closewindow.grid(row=1, column=0, padx=(100,10), pady=(12, 15), sticky="w", columnspan=2)

        self.other = ttk.Checkbutton(self.option_frame, text="Invalid", style="Switch.TCheckbutton", variable='', state='disabled')
        self.other.grid(row=1, column=0, padx=(215,10), pady=(12, 15), sticky="w", columnspan=2)

        # reset delay button
        self.resetdelay = ttk.Button(self.tab_2, text="Reset Delay", state='normal', style="Accent.TButton", command=lambda: self.widgetfunc.resetdelay())
        self.resetdelay.grid(row=1, column=1, padx=(160, 0), pady=(30, 20), sticky="w",columnspan=2)

        # start button
        self.accentbutton2 = ttk.Button(self.tab_2, text="Start", style="Accent.TButton", command=lambda: self.widgetfunc.botstart())
        self.accentbutton2.grid(row=1, column=2, padx=32, pady=(30, 20), sticky="e")
        #===================================================Tab #2=========================================================================================
        
        #===================================================Tab #3=========================================================================================
         # Tab #3
        self.tab_3 = ttk.Frame(self.notebook)
        for index in [0, 1]:
            self.tab_3.columnconfigure(index=index, weight=1)
            self.tab_3.rowconfigure(index=index, weight=1)
        self.notebook.add(self.tab_3, text="   About   ")

        # About
        self.aboutHead = ttk.Label(self.tab_3, text="NSBot Version %s"%Program.load_version("version"), font=("Segoe UI",  16, 'bold'), padding=(0, 10),)
        self.aboutHead.grid(row=0, column=0, padx=(15,0), pady=(0, 0), sticky="nw", columnspan=1)
        self.abouttext = ttk.Label(self.tab_3, text=changelog, font=("Segoe UI",  12), padding=(0, 0),)
        self.abouttext.grid(row=0, column=0, padx=(15,0), pady=(40, 0), sticky="nw")
        #===================================================Tab #3=========================================================================================

class Program():
    def load_version(*paramlist):
        with open('version.json', 'r', encoding='utf-8') as file:
            data = (json.load(file))
            result = {}
            if "version" in paramlist:
                result = data['version']
            if "changelog" in paramlist:
                result = data['changelog']
            if "shownote" in paramlist:
                result = data['shownote']
            if "releasenote" in paramlist:
                result = data['releasenote']
            return result
    
    def show_updatechange():
        version = Program.load_version("version")
        shownote = Program.load_version("shownote")
        releasenote = Program.load_version("releasenote")
        if shownote == 'True':
            messagebox.showinfo("NSBot %s" % version, " Release Note\n\n %s" % releasenote)
            with open("version.json", "r", encoding='utf-8') as file:
                data = json.load(file)
            # แก้ไขค่า "shownote" เป็น "False"
            data["shownote"] = "False"
            # เขียนค่าที่แก้ไขแล้วกลับเป็นไฟล์ JSON
            with open("version.json", "w", encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False)
        else:
            pass

    def get_api(*paramlist):
        api_url = f"https://api.github.com/repos/nsblollipop/NSBotUpdate/releases/latest"
        headers = {
        "Authorization": "Bearer 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",
        "Accept": "application/vnd.github.v3+json"}
        try:
            print('Connect to API with token')
            getresponse = requests.get(api_url, headers=headers)
            latest_version = getresponse.json()["tag_name"]
            result = {}
            if "getresponse" in paramlist:
                result["getresponse"] = getresponse
            if "latest_version" in paramlist:
                result = latest_version
            return result
        except KeyError:
            print ('Unable to connect GitHub API, change to connect without token')
            getresponse = requests.get(api_url)
            latest_version = getresponse.json()["tag_name"]
            result = {}
            if "getresponse" in paramlist:
                result["getresponse"] = getresponse
            if "latest_version" in paramlist:
                result = latest_version
            return result
        except:
            print ('Unable to connect GitHub API')
            result = {}
            if "latest_version" in paramlist:
                result = Program.load_version("version")
            print (result)
            return result
        
    def check_for_updates():
        latest_version = Program.get_api("latest_version")
        # latest_version = 'try update' #for test
        if latest_version != Program.load_version("version"):
            print("New version available")
            response = Program.get_api("getresponse")
            response = messagebox.askquestion("Check for update", "ตรวจพบเวอร์ชันใหม่ ต้องการดาวน์โหลดหรือไม่?")
            if response == 'yes':
                directory = './'
                target_file = 'update.exe'
                new_name = 'runupdate.exe'
                try:
                    for root, dirs, files in os.walk(directory):
                        if target_file in files:
                            file_path = os.path.join(root, new_name)
                            os.remove(new_name)
                except:
                    pass
                for root, dirs, files in os.walk(directory):
                    if target_file in files:
                        file_path = os.path.join(root, target_file)
                        new_file_path = os.path.join(root, new_name)
                        os.rename(file_path, new_file_path)
                else:
                    pass
                
                try:
                    file_name = "runupdate.bat"
                    file_content = "start runupdate.exe\ntaskkill /F /IM NSLaunch.exe\ntaskkill /F /IM runprocess.exe"
                    with open(file_name, "w") as file:
                        file.write(file_content)
                    subprocess.call(['runupdate.bat'], creationflags=subprocess.CREATE_NO_WINDOW)
                except:
                    pass
            else:
                pass
        else:
            directory = './'
            batchfile = "runupdate.bat"
            target_file = 'runupdate.exe'
            new_name = 'update.exe'
            try:
                for root, dirs, files in os.walk(directory):
                    if batchfile in files:
                        file_path = os.path.join(root, batchfile)
                        os.remove(file_path)
                    if target_file in files:
                        file_path = os.path.join(root, target_file)
                        os.remove(file_path)
            except:
                pass
            
    def on_closing():
        try:
            Temp.send_proc_pid()
        except:
            pass
        root.destroy()


if __name__ == "__main__":
    version = Program.load_version("version")
    changelog = Program.load_version("changelog")
    root = tk.Tk()
    root.resizable(False, False)
    root.title("NSBot %s"%version)
    root.iconbitmap(r'./screenshots/icon.ico')

    app = MainGUI(root)
    app.pack(fill="both", expand=False)
    root.update()
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))
    threading.Thread(target=Program.check_for_updates).start()
    threading.Thread(target=Program.show_updatechange).start()
    root.protocol("WM_DELETE_WINDOW", Program.on_closing)
    
    root.mainloop()
    
