from Module.GameControl import *
from Module.ThreadGame import *
from Module.Util import *
from Module.loadconfig import *
from Module.logsystem import MyLog
import time, subprocess
import logging
import win32con



_localVariable=threading.local()
_displayChat=0
cantattk=0
_idlecount=0
svselect='GB'

class Pve(threading.Thread):
    def __init__(self, windowName, total):
        global svselect
        threading.Thread.__init__(self)
        self.__hwnd=windowName
        self.__total=total
        self.__gui=GameControl(self.__hwnd,0)
# 
    def gameModePve(self):
        CLICK_SOULMAX=(568, 387)
        CLICK_FINISH2=(35, 510)
        while True:
            detectAssistance = threading.Thread(target=self.detectAssistance())
            detectAssistance.daemon = True
            detectAssistance.start

            if self.__gui.find_game_img(config['DEFAULT']['IMAGE_MAIL'], thread=0.96):
                logging.info("enter")
                self.enter_pve()
                time.sleep(1)

            ready=self.__gui.find_game_img(config[svselect]['IMAGE_READY_PATH'],thread=0.95, gray=0)
            if self.__gui.find_game_img(config[svselect]['IMAGE_READY_PATH'],thread=0.95, gray=0):
                logging.info("ready")
                self.__gui.mouse_click_bg(ready)
                time.sleep(1)

            #check finish
            if self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1_PATH']) != False or self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED2_PATH']) != False:
                logging.info("Finish")
                while True:
                    if self.__gui.find_game_img(config[svselect]['IMAGE_COOP2_SEAL']) or (_displayChat == 0 and self.__gui.find_game_img(config[svselect]['IMAGE_CHATDETECT'])) or self.__gui.find_game_img(config[svselect]['IMAGE_CHATSTICKER']):
                        detectAssistance = threading.Thread(target=self.detectAssistance())
                        detectAssistance.daemon = True
                        detectAssistance.start

                    if (self.__gui.find_game_img(config['DEFAULT']['IMAGE_MAIL'], thread=0.96) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_EMPTY_SUSHI'])) != False:
                        logging.info("break")
                        break

                    #soulmax
                    if self.__gui.find_game_img(config[svselect]['IMAGE_SOULMAX']) != False:
                        self.__gui.mouse_click_bg((_displayChat+CLICK_SOULMAX[0], CLICK_SOULMAX[1]))
                        # time.sleep(1)
                        continue
                    self.__gui.mouse_click_bg((_displayChat+841, 86))
                break

            #soulmax
            if self.__gui.find_game_img(config[svselect]['IMAGE_SOULMAX']) != False:
                self.__gui.mouse_click_bg((_displayChat+CLICK_SOULMAX[0], CLICK_SOULMAX[1]))
                time.sleep(1)
    
    def detectAssistance(self):
        global _displayChat, _idlecount
        position1 = self.__gui.find_game_img(config[svselect]['IMAGE_COOP2_SEAL'])
        position2 = self.__gui.find_game_img(config[svselect]['IMAGE_CHATSTICKER'])
        position3 = self.__gui.find_game_img(config[svselect]['IMAGE_CHATDETECT'])

        if _displayChat == 0 and position3:
            _displayChat = 525
            self.__gui.recheckRect()
            logging.info('External chat detected..')

        if (not position3) and position2:
            self.__gui.mouse_click_bg(position2)
            _displayChat = 0
            self.__gui.recheckRect()
            logging.info('ChatPanel detected, closed..')

        if position1:
            logging.info("Refuse to accept the invitation for the wanted seal...")
            self.__gui.takescreenshot('คนเหลี่ยมๆ')
            self.__gui.mouse_click_bg((position1[0] + 174, position1[1] + 308))

        
        if _idlecount >= 1200:
            logging.info("Idle Count = 1200, Exit.")
            total = str(self.__total)
            args = ['taskkill', '/F', '/PID', str(self.__pid)]
            subprocess.Popen(args)
            sys.exit()

    def run(self):
        count=0
        _localVariable.detectCount=10
        while self.__total-count>0:
            seconds=0
            while seconds:
                time.sleep(1)
                seconds-=1
            print("\n\n==================Starting a new round==================")
            # self.test_1()
            # self.gameModeTest()
            self.gameModePve()
            count+=1
            message="completed %s, remaining %s round"%(str(count),str(self.__total-count))
            print(message)
    
    
    def enter_pve(self):
        window_name = "Run-time Debug"
        hwnd = win32gui.FindWindow(None, window_name)
        control_id_value = 0x0
        child_hwnd = win32gui.FindWindowEx(hwnd, 0, None, None)
        while child_hwnd != 0:
            control_id = win32gui.GetDlgCtrlID(child_hwnd)
            if control_id == control_id_value:
                win32gui.SendMessage(child_hwnd, win32con.WM_SETTEXT, 0, "#pve,710716")
                time.sleep(0.5)
                win32gui.SendMessage(child_hwnd, win32con.WM_CHAR, 13, 0)
                time.sleep(1)
                return child_hwnd
            child_hwnd = win32gui.FindWindowEx(hwnd, child_hwnd, None, None)
        return 0


# windowName = ('阴阳师-网易游戏')
windowName = ('Onmyoji')
hwnd = win32gui.FindWindow(None, windowName)
total=100
accounts=[]

def main():
    # load_config()
    MyLog.init('INFO')
    print (hwnd)
    print('Start Bot')
    accounts.append(Pve(hwnd, total))
    account=threading.Thread(accounts[0].run())

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
    # handle the exception
        print("An exception occurred:", error)
        time.sleep(10)