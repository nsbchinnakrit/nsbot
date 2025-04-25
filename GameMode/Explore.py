from Module.GameControl import *
from Module.ThreadGame import *
from Module.Util import *
from Module.loadconfig import *
import time
import pyautogui, subprocess

_localVariable=threading.local()
_displayChat=0
self.__sv=''
_isLeader=False
_cAutoRotation=False
_isboss=False
cantattk=0
waittime=0
_idlecount=0

class Explore(threading.Thread):
    def __init__(self,Server, windowName, beforetotal, total, pid, bondlingmode, pactsettings, crystal_use, tomb, snowball, azure, kuro, markboss):
        # global self.__sv
        threading.Thread.__init__(self)
        self.__sv=Server
        self.__hwnd=windowName
        self.__beforetotal=beforetotal
        self.__total=total
        self.__pid=pid
        self.__gui=GameControl(self.__hwnd,0)

        color_templates = {
            "IMAGE_STORY_LEAD_PATH": config[self.__sv]['IMAGE_STORY_LEAD_PATH'],
        }

        gray_templates = {
            # EXPLORE
            "IMAGE_STORY_ACCEPT_PATH": config['EXPLORE']['IMAGE_STORY_ACCEPT_PATH'],
            "IMAGE_STORY_BOX_PATH": config['EXPLORE']['IMAGE_STORY_BOX_PATH'],
            "IMAGE_STORY_FIGHT_PATH": config['EXPLORE']['IMAGE_STORY_FIGHT_PATH'],
            "IMAGE_STORY_FIGHT_BOSS_PATH": config['EXPLORE']['IMAGE_STORY_FIGHT_BOSS_PATH'],
            "IMAGE_STORY_CHERRY_CAKE_PATH": config['EXPLORE']['IMAGE_STORY_CHERRY_CAKE_PATH'],
            "IMAGE_STORY_LIST_CHAPTER_PATH": config['EXPLORE']['IMAGE_STORY_LIST_CHAPTER_PATH'],
            "IMAGE_STORY_GET_REWARD_PATH": config['EXPLORE']['IMAGE_STORY_GET_REWARD_PATH'],

            # SOUL
            "IMAGE_SOUL_INVITE_PATH": config['SOUL']['IMAGE_SOUL_INVITE_PATH'],
            "IMAGE_SOUL_ROOM_DETECT_PATH": config['SOUL']['IMAGE_SOUL_ROOM_DETECT_PATH'],

            # DEFAULT
            "IMAGE_FINISHED2_PATH": config['DEFAULT']['IMAGE_FINISHED2_PATH'],
            "IMAGE_FINISHED1_PATH": config['DEFAULT']['IMAGE_FINISHED1_PATH'],
            "IMAGE_FINISHED1S2_PATH": config['DEFAULT']['IMAGE_FINISHED1S2_PATH'],
            "IMAGE_FAILED_PATH": config['DEFAULT']['IMAGE_FAILED_PATH'],
            "IMAGE_EMPTY_SUSHI": config['DEFAULT']['IMAGE_EMPTY_SUSHI'],
            "IMAGE_EMPTY_SUSHI_CLOSE": config['DEFAULT']['IMAGE_EMPTY_SUSHI_CLOSE'],
            "IMAGE_BUFF": config['DEFAULT']['IMAGE_BUFF'],
            "IMAGE_INBATTLE": config[self.__sv]['IMAGE_INBATTLE'],

            # self.__sv-specific (server-dependent)
            "IMAGE_SOUL_INVITE_DIALOG_PATH": config[self.__sv]['IMAGE_SOUL_INVITE_DIALOG_PATH'],
            "IMAGE_SOUL_START_PATH": config[self.__sv]['IMAGE_SOUL_START_PATH'],
            "IMAGE_STORY_AUTOFOOD_PATH": config[self.__sv]['IMAGE_STORY_AUTOFOOD_PATH'],
            "IMAGE_READY_PATH": config[self.__sv]['IMAGE_READY_PATH'],
            "IMAGE_SOULMAX": config[self.__sv]['IMAGE_SOULMAX'],
            "IMAGE_COOP2_SEAL": config[self.__sv]['IMAGE_COOP2_SEAL'],
            "IMAGE_CHATDETECT": config[self.__sv]['IMAGE_CHATDETECT'],
            "IMAGE_CHATSTICKER": config[self.__sv]['IMAGE_CHATSTICKER'],

            #WANTED Quest
            "IMAGE_CLOSEWANTED": config['DEFAULT']['IMAGE_CLOSEWANTED'],
            "IMAGE_WQ_JADE": config['DEFAULT']['IMAGE_WQ_JADE'],
            "IMAGE_WQ_COIN": config['DEFAULT']['IMAGE_WQ_COIN'],
            "IMAGE_WQ_SUSHI": config['DEFAULT']['IMAGE_WQ_SUSHI'],
            "IMAGE_WQ_FOODDOG": config['DEFAULT']['IMAGE_WQ_FOODDOG'],
            "IMAGE_WQ_FOODCAT": config['DEFAULT']['IMAGE_WQ_FOODCAT'],
        }

        self.load_templates(gray_templates, gray=1)
        self.load_templates(color_templates, gray=0)
    
    def load_templates(self, paths, gray=1):
        self.__gui.load_templates(paths, gray=gray)
        mode = "GRAY" if gray else "COLOR"
        logging.info("Event template loaded (%s): %d templates", mode, len(paths))


    def gameModeExplore(self):
        global _isLeader, _cAutoRotation, cantattk, waittime, _idlecount, _isboss
        CLICK_SOULMAX=(568, 387)
        CLICK_FINISH2=(35, 510)
        SLIDE_STORY_COORDINATE=[(_displayChat+200,200),(_displayChat+1000,200)]
        while True:
            detectAssistance = threading.Thread(target=self.detectAssistance())
            detectAssistance.setDaemon(True)
            detectAssistance.start

            IMAGE_STORY_ACCEPT_PATH=self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_ACCEPT_PATH'])
            if IMAGE_STORY_ACCEPT_PATH != False:
                logging.info("Accept Invite.")
                self.__gui.mouse_click_bg(IMAGE_STORY_ACCEPT_PATH)  
                _idlecount=0
                time.sleep(1)
                continue

            IMAGE_STORY_BOX_PATH=self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_BOX_PATH'])
            if IMAGE_STORY_BOX_PATH != False:
                logging.info("Box Found. (Func.2)")
                self.__gui.mouse_click_bg(IMAGE_STORY_BOX_PATH)
            if self.__gui.find_game_img(self.__gui.templates['IMAGE_FINISHED2_PATH']) != False:
                self.__gui.mouse_click_bg((_displayChat+CLICK_FINISH2[0], CLICK_FINISH2[1]))
            
            if self.__gui.find_game_img(self.__gui.templates['IMAGE_SOUL_INVITE_PATH']) != False:
                waittime+=1
                if waittime>=12:
                    self.__gui.mouse_click_bg((_displayChat+960, 225))
                    time.sleep(2)
                    self.__gui.mouse_click_bg((_displayChat+444, 514))
                    waittime=0
            
            IMAGE_SOUL_INVITE_DIALOG_PATH=self.__gui.find_game_img(self.__gui.templates['IMAGE_SOUL_INVITE_DIALOG_PATH'])
            if IMAGE_SOUL_INVITE_DIALOG_PATH != False:
                logging.info("Invited..")
                time.sleep(1)
                self.__gui.mouse_click_bg((_displayChat+IMAGE_SOUL_INVITE_DIALOG_PATH[0]+170,IMAGE_SOUL_INVITE_DIALOG_PATH[1]+100))
            
            if cantattk >= 12 or (self.__gui.find_game_img(self.__gui.templates['IMAGE_EMPTY_SUSHI']) != False and self.__gui.find_game_img(self.__gui.templates['IMAGE_EMPTY_SUSHI_CLOSE']) == False):
                logging.info("Unable to process, Exit!")
                total = str(self.__total)
                self.create_file(data=total)
                args = ['taskkill', '/F', '/PID', str(self.__pid)]
                subprocess.Popen(args)
                sys.exit()
                    
            IMAGE_SOUL_START_PATH=self.__gui.find_game_img(self.__gui.templates['IMAGE_SOUL_START_PATH'])
            IMAGE_SOUL_INVITE_PATH=self.__gui.find_game_img(self.__gui.templates['IMAGE_SOUL_INVITE_PATH'])
            if IMAGE_SOUL_START_PATH != False and IMAGE_SOUL_INVITE_PATH == False:
                logging.info("Start... ")
                self.__gui.mouse_click_bg(IMAGE_SOUL_START_PATH)
                waittime=0
                _idlecount=0
                time.sleep(1)

            IMAGE_STORY_AUTOFOOD_PATH=self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_AUTOFOOD_PATH'])
            if IMAGE_STORY_AUTOFOOD_PATH != False:
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
            IMAGE_STORY_LEAD_PATH=self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_LEAD_PATH'], part=1, pos1=(75, 245), pos2=(170, 300), gray=0, threshold=0.90)
            if _isLeader == False:
                if IMAGE_STORY_LEAD_PATH != False:
                    logging.info("Leader Detected in display..")
                    _isLeader=True
                else:
                    _isLeader=False
            
                #===============================================slide windows if not found monster
            IMAGE_STORY_FIGHT_PATH2=(self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_FIGHT_PATH']) or self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_FIGHT_BOSS_PATH']))
            IMAGE_STORY_CHERRY_CAKE_PATH=self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_CHERRY_CAKE_PATH'])
            if _isLeader != False and IMAGE_STORY_FIGHT_PATH2 == False and IMAGE_STORY_CHERRY_CAKE_PATH != False:
                time.sleep(1)
                if self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_FIGHT_PATH']) == False and self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_FIGHT_BOSS_PATH']) == False:
                    self.__gui.mouse_drag_bg(SLIDE_STORY_COORDINATE[1],SLIDE_STORY_COORDINATE[0])
                    _localVariable.detectCount -= 1
                    time.sleep(1)
                    if _localVariable.detectCount < 1:
                        # self.__gui.mouse_drag_bg(SLIDE_STORY_COORDINATE[1],SLIDE_STORY_COORDINATE[0])
                        self.__gui.mouse_drag_bg(SLIDE_STORY_COORDINATE[0],SLIDE_STORY_COORDINATE[1])
                        _localVariable.detectCount=30
                        time.sleep(1)
            
            IMAGE_STORY_FIGHT_BOSS_PATH=self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_FIGHT_BOSS_PATH'])
            if (_isLeader and IMAGE_STORY_FIGHT_BOSS_PATH) != False:
                logging.info("BOSS was detected: ")
                self.__gui.mouse_click_bg(IMAGE_STORY_FIGHT_BOSS_PATH)
                _isboss=True
                cantattk+=1
                _idlecount=0
                time.sleep(1)
                continue

            IMAGE_STORY_FIGHT_PATH=self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_FIGHT_PATH'])
            if (_isLeader and IMAGE_STORY_FIGHT_PATH) != False:
                logging.info("Monster was detected... ")
                self.__gui.mouse_click_bg(IMAGE_STORY_FIGHT_PATH)
                cantattk+=1
                _idlecount=0
                time.sleep(1)
                continue
            #=========================================get ready=================================================
            IMAGE_READY_PATH=self.__gui.find_game_img(self.__gui.templates['IMAGE_READY_PATH'],threshold=0.8)
            if IMAGE_READY_PATH != False:
                logging.info("Starting battle.... ")
                self.__gui.mouse_click_bg(IMAGE_READY_PATH)
                _idlecount=0
                time.sleep(2)
                continue

            #=========================================Finish=================================================
            #Fail
            IMAGE_FAILED_PATH=self.__gui.find_game_img(self.__gui.templates['IMAGE_FAILED_PATH'])
            if IMAGE_FAILED_PATH != False:
                cantattk=0
                _idlecount=0
                logging.info("Battle End, Fail..")
                self.__gui.mouse_click_bg(IMAGE_FAILED_PATH)
                continue

            IMAGE_FINISHED2_PATH=self.__gui.find_game_img(self.__gui.templates['IMAGE_FINISHED2_PATH'])
            if IMAGE_FINISHED2_PATH != False:
                cantattk=0
                _idlecount=0
                self.__gui.mouse_click_bg(IMAGE_FINISHED2_PATH)
                continue

            #check finish
            if (self.__gui.find_game_img(self.__gui.templates['IMAGE_FINISHED1_PATH']) or 
                self.__gui.find_game_img(self.__gui.templates['IMAGE_FINISHED1S2_PATH']) != False) and (
                self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_LIST_CHAPTER_PATH']) or 
                self.__gui.find_game_img(self.__gui.templates['IMAGE_SOUL_ROOM_DETECT_PATH']) == False):
                logging.info("Battle End, Victory!")
                cantattk=0
                _idlecount=0
                while True:
                    if self.__gui.find_game_img(self.__gui.templates['IMAGE_COOP2_SEAL']) or (_displayChat == 0 and self.__gui.find_game_img(self.__gui.templates['IMAGE_CHATDETECT'])) or self.__gui.find_game_img(self.__gui.templates['IMAGE_CHATSTICKER']):
                        detectAssistance = threading.Thread(target=self.detectAssistance())
                        detectAssistance.setDaemon(True)
                        detectAssistance.start
                    if (_isboss != True) and (self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_CHERRY_CAKE_PATH']) != False or 
                        self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_ACCEPT_PATH']) != False or 
                        self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_LIST_CHAPTER_PATH']) != False or 
                        self.__gui.find_game_img(self.__gui.templates['IMAGE_BUFF']) != False or 
                        self.__gui.find_game_img(self.__gui.templates['IMAGE_EMPTY_SUSHI']) != False):
                        time.sleep(1)
                        break
                    if (_isboss) and (self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_CHERRY_CAKE_PATH']) != False):
                        _isboss=False
                        continue
                    if self.__gui.find_game_img(self.__gui.templates['IMAGE_SOULMAX']) != False:
                        logging.info("Soul Max")
                        self.__gui.mouse_click_bg((_displayChat+CLICK_SOULMAX[0], CLICK_SOULMAX[1]))
                        time.sleep(1)
                        continue
                    self.__gui.mouse_click_bg((_displayChat+CLICK_FINISH2[0], CLICK_FINISH2[1]))
                    time.sleep(0.01)
                break

            #==========================================Reward settlement=============================================
            IMAGE_STORY_GET_REWARD_PATH=self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_GET_REWARD_PATH'])
            if IMAGE_STORY_GET_REWARD_PATH != False:
                logging.info("Get treasure.... ")
                self.__gui.send_esc_down()
                time.sleep(2)
                _idlecount=0
                self.__gui.mouse_click_bg((_displayChat+655, 383))

            #soulmax
            if self.__gui.find_game_img(self.__gui.templates['IMAGE_SOULMAX']) != False:
                logging.info("Soul Max")
                self.__gui.mouse_click_bg((_displayChat+CLICK_SOULMAX[0], CLICK_SOULMAX[1]))
                time.sleep(1)
                continue

            else:
                _idlecount+=1

            
    
    def detectAssistance(self):
        global _displayChat, _idlecount
        IMAGE_COOP2_SEAL = self.__gui.find_game_img(self.__gui.templates['IMAGE_COOP2_SEAL'])
        IMAGE_CHATSTICKER = self.__gui.find_game_img(self.__gui.templates['IMAGE_CHATSTICKER'])
        IMAGE_CHATDETECT = self.__gui.find_game_img(self.__gui.templates['IMAGE_CHATDETECT'])
        IMAGE_CLOSEWANTED = self.__gui.find_game_img(self.__gui.templates['IMAGE_CLOSEWANTED'])
        wq_jade = config['VALUE']['WQ_JADE']
        wq_coin = config['VALUE']['WQ_COIN']
        wq_sushi = config['VALUE']['WQ_SUSHI']
        wq_food = config['VALUE']['WQ_FOOD']

        if _displayChat == 0 and IMAGE_CHATDETECT:
            _displayChat = 525
            self.__gui.recheckRect()
            logging.info('External chat detected..')

        if (not IMAGE_CHATDETECT) and IMAGE_CHATSTICKER:
            self.__gui.mouse_click_bg(IMAGE_CHATSTICKER)
            _displayChat = 0
            self.__gui.recheckRect()
            logging.info('ChatPanel detected, closed..')

        if IMAGE_COOP2_SEAL:
            if (self.__gui.find_game_img(self.__gui.templates['IMAGE_WQ_JADE'], threshold=0.8) and wq_jade
            ) or (self.__gui.find_game_img(self.__gui.templates['IMAGE_WQ_COIN'], threshold=0.8) and wq_coin
            ) or (self.__gui.find_game_img(self.__gui.templates['IMAGE_WQ_SUSHI'], threshold=0.8) and wq_sushi
            ) or ((self.__gui.find_game_img(self.__gui.templates['IMAGE_WQ_FOODDOG'], threshold=0.8) or self.__gui.find_game_img(self.__gui.templates['IMAGE_WQ_FOODCAT'], threshold=0.8)) and wq_food):
                logging.info("Accept wanted quest...")
                self.__gui.mouse_click_bg((IMAGE_COOP2_SEAL[0] + 279, IMAGE_COOP2_SEAL[1] + 220))
                screenshot = self.__gui.takescreenshot('คนเหลี่ยมๆ')
                self.create_file2(data=screenshot)
            else:
                logging.info("Refuse to accept the invitation for the wanted seal...")
                self.__gui.mouse_click_bg((IMAGE_COOP2_SEAL[0] + 279, IMAGE_COOP2_SEAL[1] + 309))
                self.__gui.takescreenshot('คนเหลี่ยมๆ')
        
        if IMAGE_CLOSEWANTED != False:
            logging.info('Close Event Wanted!')
            self.__gui.mouse_click_bg(IMAGE_CLOSEWANTED)
        
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
