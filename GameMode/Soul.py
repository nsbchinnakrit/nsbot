import time
import pyautogui
from Module.GameControl import *
from Module.ThreadGame import *
from Module.loadconfig import *
from Module.Util import *
import threading, subprocess

_displayChat = 0
cantattk=0
_idlecount=0
CLICK_SOULMAX=(568, 387)
START_SOUL_COORDINATE = (1075, 565)

class Soul(threading.Thread):
    def __init__(self,Server, windowName, beforetotal, total, pid, bondlingmode, pactsettings, crystal_use, tomb, snowball, azure, kuro):
        global svselect
        threading.Thread.__init__(self)
        self.__server=Server
        svselect=self.__server
        self.__hwnd=windowName
        self.__beforetotal=beforetotal
        self.__total=total
        self.__pid=pid
        self.__gui=GameControl(self.__hwnd,0)

    def gameModeSoul(self):
        global _displayChat, cantattk, _idlecount
        while True:
            detectAssistance = threading.Thread(target=self.detectAssistance())
            detectAssistance.setDaemon(True)
            detectAssistance.start

            position = self.__gui.find_game_img(config[svselect]['IMAGE_SOUL_START_PATH'], thread=0.96)
            position2 = self.__gui.find_game_img(config['SOUL']['IMAGE_SOUL_INVITE_PATH'], part=1, pos1=(460, 160), pos2=(680, 420))
            if (position) and (not position2):
                time.sleep(0.1)
                logging.info("Starting...")
                self.__gui.mouse_click_bg(position)
                cantattk+=1
                _idlecount=0
                time.sleep(1)
                # return
            
            if cantattk >= 12 or (self.__gui.find_game_img(config['DEFAULT']['IMAGE_EMPTY_SUSHI']) != False and self.__gui.find_game_img(config['DEFAULT']['IMAGE_EMPTY_SUSHI_CLOSE']) != False) or (self.__gui.find_game_img(config[svselect]['IMAGE_REALM_CANCEL']) != False) and (self.__gui.find_game_img(config['SOUL']['IMAGE_SOUL_INVITE_CHECKBOX_PATH'], thread=0.98) == False):
                logging.info("Unable to process, Exit!")
                total = str(self.__total)
                self.create_file(data=total)
                args = ['taskkill', '/F', '/PID', str(self.__pid)]
                subprocess.Popen(args)
                sys.exit()

            position = self.__gui.find_game_img(config['SOUL']['IMAGE_SOUL_AUTOACCEPT_PATH'])
            if position:
                logging.info("Accept Invited..")
                self.__gui.mouse_click_bg(position)
                time.sleep(1)
                # return

            position = self.__gui.find_game_img(config['SOUL']['IMAGE_SOUL_INVITE_CHECKBOX_PATH'], thread=0.98)
            if position:
                logging.info("Accept Invited..")
                self.__gui.mouse_click_bg(position)
                time.sleep(0.5)
                self.__gui.mouse_click_bg((_displayChat + position[0] + 247, position[1] + 77))
                time.sleep(1)
                # return
            
            #=========================================get ready=================================================
            position=self.__gui.find_game_img(config[svselect]['IMAGE_READY_PATH'],thread=0.8)
            if position != False:
                self.__gui.mouse_click_bg(position)
                time.sleep(2)
                continue

            if (
                self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED0_PATH']) or 
                self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1_PATH']) or
                self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1S2_PATH']) or
                self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED2_PATH'])
            ):
                cantattk=0
                _idlecount=0
                while True:
                    if self.__gui.find_game_img(config[svselect]['IMAGE_COOP2_SEAL']) or (_displayChat == 0 and self.__gui.find_game_img(config[svselect]['IMAGE_CHATDETECT'])) or self.__gui.find_game_img(config[svselect]['IMAGE_CHATSTICKER']):
                        detectAssistance = threading.Thread(target=self.detectAssistance())
                        detectAssistance.setDaemon(True)
                        detectAssistance.start

                    if (
                        self.__gui.find_game_img(config['SOUL']['IMAGE_SOUL_ROOM_DETECT_PATH']) or
                        self.__gui.find_game_img(config['SOUL']['IMAGE_SOUL_INVITE_CHECKBOX_PATH']) or
                        self.__gui.find_game_img(config[svselect]['IMAGE_SOUL_START_PATH']) or
                        self.__gui.find_game_img(config['DEFAULT']['IMAGE_MAIL'],thread=0.96) or
                        self.__gui.find_game_img(config['SOUL']['IMAGE_SOUL_AUTOACCEPT_PATH']) or 
                        self.__gui.find_game_img(config['DEFAULT']['IMAGE_EMPTY_SUSHI'])
                    ):
                        break

                    if self.__gui.find_game_img(config[svselect]['IMAGE_SOULMAX']) != False:
                        logging.info("Soul Max")
                        self.__gui.mouse_click_bg((_displayChat+CLICK_SOULMAX[0], CLICK_SOULMAX[1]))
                        time.sleep(1)

                    if self.__gui.find_game_img(config[svselect]['IMAGE_SOUL_PETREWARD_PATH']):
                        logging.info("Claim Pet Reward.")
                        self.__gui.mouse_click_bg((_displayChat + 950, 450))
                    self.__gui.mouse_click_bg(START_SOUL_COORDINATE)
                break

            position = self.__gui.find_game_img(config['DEFAULT']['IMAGE_FAILED_PATH'], gray=0)
            if position:
                cantattk=0
                _idlecount=0
                logging.info("Failed...")
                self.__gui.mouse_click_bg(position)
            
            if self.__gui.find_game_img(config[svselect]['IMAGE_SOUL_PETREWARD_PATH']):
                logging.info("Claim Pet Reward.")
                self.__gui.mouse_click_bg((_displayChat + 950, 450))
                time.sleep(1)
            
            if self.__gui.find_game_img(config[svselect]['IMAGE_SOULMAX']) != False:
                logging.info("Soul Max")
                self.__gui.mouse_click_bg((_displayChat+CLICK_SOULMAX[0], CLICK_SOULMAX[1]))
                time.sleep(1)

            else:
                _idlecount+=1

    def detectAssistance(self):
        global _displayChat, _idlecount
        position1 = self.__gui.find_game_img(config[svselect]['IMAGE_COOP2_SEAL'])
        position2 = self.__gui.find_game_img(config[svselect]['IMAGE_CHATSTICKER'])
        position3 = self.__gui.find_game_img(config[svselect]['IMAGE_CHATDETECT'])
        position4 = self.__gui.find_game_img(config['DEFAULT']['IMAGE_CLOSEWANTED'])
        wq_jade = config['VALUE']['WQ_JADE']
        wq_coin = config['VALUE']['WQ_COIN']
        wq_sushi = config['VALUE']['WQ_SUSHI']
        wq_food = config['VALUE']['WQ_FOOD']

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
            if (self.__gui.find_game_img(config['DEFAULT']['IMAGE_WQ_JADE'], thread=0.8) and wq_jade
            ) or (self.__gui.find_game_img(config['DEFAULT']['IMAGE_WQ_COIN'], thread=0.8) and wq_coin
            ) or (self.__gui.find_game_img(config['DEFAULT']['IMAGE_WQ_SUSHI'], thread=0.8) and wq_sushi
            ) or ((self.__gui.find_game_img(config['DEFAULT']['IMAGE_WQ_FOODDOG'], thread=0.8) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_WQ_FOODCAT'], thread=0.8)) and wq_food):
                logging.info("Accept wanted quest...")
                self.__gui.mouse_click_bg((position1[0] + 174, position1[1] + 222))
                screenshot = self.__gui.takescreenshot('คนเหลี่ยมๆ')
                self.create_file2(data=screenshot)
            else:
                logging.info("Refuse to accept the invitation for the wanted seal...")
                self.__gui.mouse_click_bg((position1[0] + 174, position1[1] + 308))
                self.__gui.takescreenshot('คนเหลี่ยมๆ')
        
        if position4 != False:
            logging.info('Close Event Wanted!')
            self.__gui.mouse_click_bg(position4)
        
        if _idlecount >= 1200:
            logging.info("Idle Count = 1200, Exit.")
            total = str(self.__total)
            self.create_file(data=total)
            args = ['taskkill', '/F', '/PID', str(self.__pid)]
            subprocess.Popen(args)
            sys.exit()


    def create_file(self, data='0'):
        temp_path = f"runprocess/temp{self.__pid}.txt"
        try:
            with open(temp_path, "w") as file:
                file.write(data)
                file.close
        except Exception as error:
            logging.error(error)
    
    def create_file2(self, data='False'):
        temp_path = f"runprocess/wanted{self.__pid}.txt"
        try:
            with open(temp_path, "w") as file:
                file.write(data)
                file.close
        except Exception as error:
            logging.error(error)

    def run(self):
        count=self.__beforetotal
        self.create_file(data=str(count))
        while self.__total-count>0:
            seconds=0
            while seconds:
                time.sleep(1)
                seconds-=1
            logging.info("\n\n==================Starting a new round==================")
            self.gameModeSoul()
            count+=1
            message="completed %s, remaining %s round"%(str(count),str(self.__total-count))
            self.create_file(data=str(count))
            logging.info(message)


if __name__ == '__main__':
    load_config()