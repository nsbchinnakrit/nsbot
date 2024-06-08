from Module.GameControl import *
from Module.ThreadGame import *
from Module.Util import *
from Module.loadconfig import *
import time
import pyautogui, subprocess

_localVariable=threading.local()
_displayChat=0
svselect=''
_isLeader=False
_cAutoRotation=False
cantattk=0
waittime=0
_idlecount=0

class Explore(threading.Thread):
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

    def gameModeExplore(self):
        global _isLeader, _cAutoRotation, cantattk, waittime, _idlecount
        CLICK_SOULMAX=(568, 387)
        CLICK_FINISH2=(35, 510)
        SLIDE_STORY_COORDINATE=[(_displayChat+200,200),(_displayChat+1000,200)]
        while True:
            detectAssistance = threading.Thread(target=self.detectAssistance())
            detectAssistance.setDaemon(True)
            detectAssistance.start

            position=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_ACCEPT_PATH'])
            if position != False:
                logging.info("Accept Invite.")
                self.__gui.mouse_click_bg(position)  
                _idlecount=0
                time.sleep(1)
                continue

            position=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_BOX_PATH'])
            if position != False:
                logging.info("Box Found. (Func.2)")
                self.__gui.mouse_click_bg(position)
            if self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED2_PATH']) != False:
                self.__gui.mouse_click_bg((_displayChat+CLICK_FINISH2[0], CLICK_FINISH2[1]))
            
            if self.__gui.find_game_img(config['SOUL']['IMAGE_SOUL_INVITE_PATH']) != False:
                waittime+=1
                if waittime>=12:
                    self.__gui.mouse_click_bg((_displayChat+960, 225))
                    time.sleep(2)
                    self.__gui.mouse_click_bg((_displayChat+444, 514))
                    waittime=0
            
            position=self.__gui.find_game_img(config[svselect]['IMAGE_SOUL_INVITE_DIALOG_PATH'])
            if position != False:
                logging.info("Invited..")
                time.sleep(1)
                self.__gui.mouse_click_bg((_displayChat+position[0]+170,position[1]+100))
            
            if cantattk >= 12 or (self.__gui.find_game_img(config['DEFAULT']['IMAGE_EMPTY_SUSHI']) != False and self.__gui.find_game_img(config['DEFAULT']['IMAGE_EMPTY_SUSHI_CLOSE']) == False):
                logging.info("Unable to process, Exit!")
                total = str(self.__total)
                self.create_file(data=total)
                args = ['taskkill', '/F', '/PID', str(self.__pid)]
                subprocess.Popen(args)
                sys.exit()
                    
            position=self.__gui.find_game_img(config[svselect]['IMAGE_SOUL_START_PATH'])
            position2=self.__gui.find_game_img(config['SOUL']['IMAGE_SOUL_INVITE_PATH'])
            if position != False and position2 == False:
                logging.info("Start... ")
                self.__gui.mouse_click_bg(position)
                waittime=0
                _idlecount=0
                time.sleep(1)

            position=self.__gui.find_game_img(config[svselect]['IMAGE_STORY_AUTOFOOD_PATH'])
            if position != False:
                logging.info("Click Auto Rotation")
                self.__gui.mouse_click_bg((_displayChat+117, 599))
                _cAutoRotation+=1
                if _cAutoRotation >= 5:
                    logging.info("Exit!")
                    pyautogui.alert(text='auto rotation food runs out, stop working..', title='Exit!', button='OK')
                    args = ['taskkill', '/F', '/PID', str(self.__pid)]
                    subprocess.Popen(args, creationflags=subprocess.CREATE_NO_WINDOW)
                    sys.exit()
                time.sleep(1)
                continue

            #-=======================================================================================================
            position=self.__gui.find_game_img((config[svselect]['IMAGE_STORY_LEAD_PATH']), part=1, pos1=(80, 250), pos2=(135, 300), gray=0, thread=0.99)
            if _isLeader == False:
                if position != False:
                    logging.info("Leader Detected in display..")
                    _isLeader=True
                else:
                    _isLeader=False
            
                #===============================================slide windows if not found monster
            position=(self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_FIGHT_PATH']) or self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_FIGHT_BOSS_PATH']))
            position2=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_CHERRY_CAKE_PATH'])
            if _isLeader != False and position == False and position2 != False:
                time.sleep(1)
                if self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_FIGHT_PATH']) == False and self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_FIGHT_BOSS_PATH']) == False:
                    self.__gui.mouse_drag_bg(SLIDE_STORY_COORDINATE[1],SLIDE_STORY_COORDINATE[0])
                    _localVariable.detectCount -= 1
                    time.sleep(1)
                    if _localVariable.detectCount < 1:
                        # self.__gui.mouse_drag_bg(SLIDE_STORY_COORDINATE[1],SLIDE_STORY_COORDINATE[0])
                        self.__gui.mouse_drag_bg(SLIDE_STORY_COORDINATE[0],SLIDE_STORY_COORDINATE[1])
                        _localVariable.detectCount=30
                        time.sleep(1)
            
            position=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_FIGHT_BOSS_PATH'])
            if (_isLeader and position) != False:
                logging.info("BOSS was detected: ")
                self.__gui.mouse_click_bg(position)
                _localVariable.isBossDetected=True
                cantattk+=1
                _idlecount=0
                time.sleep(1)
                continue

            position=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_FIGHT_PATH'])
            if (_isLeader and position) != False:
                logging.info("Monster was detected... ")
                self.__gui.mouse_click_bg(position)
                cantattk+=1
                _idlecount=0
                time.sleep(1)
                continue
            #=========================================get ready=================================================
            position=self.__gui.find_game_img(config[svselect]['IMAGE_READY_PATH'],thread=0.8)
            if position != False:
                logging.info("Starting battle.... ")
                self.__gui.mouse_click_bg(position)
                _idlecount=0
                time.sleep(2)
                continue

            #=========================================Finish=================================================
            #Fail
            position=self.__gui.find_game_img(config['DEFAULT']['IMAGE_FAILED_PATH'])
            if position != False:
                cantattk=0
                _idlecount=0
                logging.info("Failed..")
                self.__gui.mouse_click_bg(position)
                continue

            position=self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED2_PATH'])
            if position != False:
                cantattk=0
                _idlecount=0
                self.__gui.mouse_click_bg(position)
                continue

            #check finish
            if (self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1_PATH']) or 
                self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1S2_PATH']) != False) and (
                self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_LIST_CHAPTER_PATH']) or 
                self.__gui.find_game_img(config['SOUL']['IMAGE_SOUL_ROOM_DETECT_PATH']) == False):
                logging.info("Finishing...")
                cantattk=0
                _idlecount=0
                while True:
                    if self.__gui.find_game_img(config[svselect]['IMAGE_COOP2_SEAL']) or (_displayChat == 0 and self.__gui.find_game_img(config[svselect]['IMAGE_CHATDETECT'])) or self.__gui.find_game_img(config[svselect]['IMAGE_CHATSTICKER']):
                        detectAssistance = threading.Thread(target=self.detectAssistance())
                        detectAssistance.setDaemon(True)
                        detectAssistance.start
                    if (self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_CHERRY_CAKE_PATH']) != False or 
                        self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_ACCEPT_PATH']) != False or 
                        self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_LIST_CHAPTER_PATH']) != False or 
                        self.__gui.find_game_img(config['DEFAULT']['IMAGE_BUFF']) != False or 
                        self.__gui.find_game_img(config['DEFAULT']['IMAGE_EMPTY_SUSHI']) != False):
                        time.sleep(1)
                        break
                    if self.__gui.find_game_img(config[svselect]['IMAGE_SOULMAX']) != False:
                        logging.info("Soul Max")
                        self.__gui.mouse_click_bg((_displayChat+CLICK_SOULMAX[0], CLICK_SOULMAX[1]))
                        time.sleep(1)
                        continue
                    self.__gui.mouse_click_bg((_displayChat+CLICK_FINISH2[0], CLICK_FINISH2[1]))
                    time.sleep(0.01)
                break

            #==========================================Reward settlement=============================================
            position=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_GET_REWARD_PATH'])
            if position != False:
                logging.info("Get treasure.... ")
                self.__gui.send_esc_down()
                time.sleep(0.4)
                _idlecount=0
                self.__gui.mouse_click_bg((_displayChat+655, 383))

            #soulmax
            if self.__gui.find_game_img(config[svselect]['IMAGE_SOULMAX']) != False:
                logging.info("Soul Max")
                self.__gui.mouse_click_bg((_displayChat+CLICK_SOULMAX[0], CLICK_SOULMAX[1]))
                time.sleep(1)
                continue

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
            ) or (self.__gui.find_game_img(config['DEFAULT']['IMAGE_WQ_FOODDOG'], thread=0.8) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_WQ_FOODCAT'], thread=0.8) and wq_food):
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
        _localVariable.detectCount=30
        while self.__total-count>0:
            seconds=0
            while seconds:
                time.sleep(1)
                seconds-=1
            logging.info("\n\n==================Starting a new round==================")
            self.gameModeExplore()
            count+=1
            message="completed %s, remaining %s round"%(str(count),str(self.__total-count))
            self.create_file(data=str(count))
            logging.info(message)


if __name__ == '__main__':
    load_config()
