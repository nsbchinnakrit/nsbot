from Module.GameControl import *
from Module.ThreadGame import *
from Module.Util import *
from Module.loadconfig import *
import time
import pyautogui, subprocess

_localVariable=threading.local()
_displayChat=0
svselect=''
_cAutoRotation=False
cantattk=0
_idlecount=0

class SingleExplore(threading.Thread):
    def __init__(self,Server, windowName, beforetotal, total, pid, bondlingmode, pactsettings, crystal_use, tomb, snowball, azure, kuro, markboss):
        # global svselect
        threading.Thread.__init__(self)
        self.__sv=Server
        self.__hwnd=windowName
        self.__beforetotal=beforetotal
        self.__total=total
        self.__pid=pid
        self.__gui=GameControl(self.__hwnd,0)
    
        color_templates = {
        }

        gray_templates = {
            # EXPLORE
            "IMAGE_STORY_BOX_PATH": config['EXPLORE']['IMAGE_STORY_BOX_PATH'],
            "IMAGE_STORY_CHERRY_CAKE_PATH": config['EXPLORE']['IMAGE_STORY_CHERRY_CAKE_PATH'],
            "IMAGE_STORY_LIST_CHAPTER_PATH": config['EXPLORE']['IMAGE_STORY_LIST_CHAPTER_PATH'],
            "IMAGE_STORY_FIGHT_PATH": config['EXPLORE']['IMAGE_STORY_FIGHT_PATH'],
            "IMAGE_STORY_FIGHT_BOSS_PATH": config['EXPLORE']['IMAGE_STORY_FIGHT_BOSS_PATH'],
            "IMAGE_STORY_GET_REWARD_PATH": config['EXPLORE']['IMAGE_STORY_GET_REWARD_PATH'],

            # DEFAULT
            "IMAGE_EMPTY_SUSHI": config['DEFAULT']['IMAGE_EMPTY_SUSHI'],
            "IMAGE_EMPTY_SUSHI_CLOSE": config['DEFAULT']['IMAGE_EMPTY_SUSHI_CLOSE'],
            "IMAGE_FAILED_PATH": config['DEFAULT']['IMAGE_FAILED_PATH'],
            "IMAGE_FINISHED2_PATH": config['DEFAULT']['IMAGE_FINISHED2_PATH'],
            "IMAGE_FINISHED1_PATH": config['DEFAULT']['IMAGE_FINISHED1_PATH'],
            "IMAGE_FINISHED1S2_PATH": config['DEFAULT']['IMAGE_FINISHED1S2_PATH'],
            "IMAGE_INBATTLE": config[self.__sv]['IMAGE_INBATTLE'],

            # SOUL
            "IMAGE_SOUL_INVITE_CHECKBOX_PATH": config['SOUL']['IMAGE_SOUL_INVITE_CHECKBOX_PATH'],

            # REALM
            "IMAGE_REALM_CLOSE": config['REALM']['IMAGE_REALM_CLOSE'],

            # SERVER-SPECIFIC (self.__sv)
            "IMAGE_STORY_LIMIT_PATH": config[self.__sv]['IMAGE_STORY_LIMIT_PATH'],
            "IMAGE_REALM_CANCEL": config[self.__sv]['IMAGE_REALM_CANCEL'],
            "IMAGE_STORY_AUTOFOOD_PATH": config[self.__sv]['IMAGE_STORY_AUTOFOOD_PATH'],
            "IMAGE_STORY_START_PATH": config[self.__sv]['IMAGE_STORY_START_PATH'],
            "IMAGE_COOP2_SEAL": config[self.__sv]['IMAGE_COOP2_SEAL'],
            "IMAGE_CHATDETECT": config[self.__sv]['IMAGE_CHATDETECT'],
            "IMAGE_CHATSTICKER": config[self.__sv]['IMAGE_CHATSTICKER'],
            "IMAGE_READY_PATH": config[self.__sv]['IMAGE_READY_PATH'],
            "IMAGE_SOULMAX": config[self.__sv]['IMAGE_SOULMAX'],
            "IMAGE_STORY_REWARD_CONFIRMED_PATH": config[self.__sv]['IMAGE_STORY_REWARD_CONFIRMED_PATH'],
        
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


    def gameModeSingleExplore(self):
        global _isPaused, _displayChat, _cAutoRotation, cantattk, _idlecount
        CLICK_SOULMAX=(568, 387)
        CLICK_FINISH2=(35, 510)
        SLIDE_STORY_COORDINATE=[(_displayChat+200,200),(_displayChat+1000,200)]
        while True:
            detectAssistance = threading.Thread(target=self.detectAssistance())
            detectAssistance.setDaemon(True)
            detectAssistance.start
            
            position=self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_BOX_PATH'])
            position2=self.__gui.find_game_img(self.__gui.templates['IMAGE_REALM_CLOSE'])
            if position != False:
                logging.info("Box Found. (Func.2)")
                self.__gui.mouse_click_bg(position)
                time.sleep(4)
                if position != False and position2 != False:
                    self.__gui.mouse_click_bg(position2)
                    time.sleep(1)
                self.__gui.mouse_click_bg(position)
                time.sleep(1)

            position=(self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_LIMIT_PATH']) or self.__gui.find_game_img(self.__gui.templates['IMAGE_EMPTY_SUSHI']))
            if position != False:
                cantattk+=1
                logging.info("Unable to process, try (%s/3)"%cantattk)
                
            
            if cantattk >= 12 or (self.__gui.find_game_img(self.__gui.templates['IMAGE_EMPTY_SUSHI']) != False and self.__gui.find_game_img(self.__gui.templates['IMAGE_EMPTY_SUSHI_CLOSE']) == False) or (self.__gui.find_game_img(self.__gui.templates['IMAGE_REALM_CANCEL']) != False) and (self.__gui.find_game_img(self.__gui.templates['IMAGE_SOUL_INVITE_CHECKBOX_PATH'], thread=0.98) == False):
                logging.info("Unable to process, Exit!")
                total = str(self.__total)
                self.create_file(data=total)
                args = ['taskkill', '/F', '/PID', str(self.__pid)]
                subprocess.Popen(args)
                sys.exit()
            
                
            position=self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_AUTOFOOD_PATH'])
            if position != False:
                logging.info("Click Auto Rotation")
                self.__gui.mouse_click_bg((_displayChat+117, 599))
                _cAutoRotation+=1
                if _cAutoRotation >= 3:
                    logging.info("Exit!")
                    pyautogui.alert(text='auto rotation food runs out, stop working..', title='Exit!', button='OK')
                    args = ['taskkill', '/F', '/PID', str(self.__pid)]
                    subprocess.Popen(args, creationflags=subprocess.CREATE_NO_WINDOW)
                time.sleep(1)

            position=self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_CHERRY_CAKE_PATH'])
            if position == False:
                position=self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_LIST_CHAPTER_PATH'])  
                if position != False:
                    _localVariable.isBossDetected=False
                    logging.info("Entering last chapter.... ")
                    self.__gui.mouse_click_bg((position[0],position[1]+370))
                    _idlecount=0
                    time.sleep(1)
                    continue
                

            position=self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_START_PATH'])
            position2=self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_BOX_PATH'])
            position3=self.__gui.find_game_img(self.__gui.templates['IMAGE_REALM_CLOSE'])
            if position != False:
                #time.sleep(0.5)
                if position2 != False and position3 != False:
                    logging.info("Box Found (Func3)")
                    self.__gui.mouse_click_bg(position)
                    time.sleep(2)
                    if position2 != False:
                        while True:
                            self.__gui.mouse_click_bg(position3)
                            time.sleep(1)
                            if self.__gui.find_game_img(self.__gui.templates['IMAGE_COOP2_SEAL']) or (_displayChat == 0 and self.__gui.find_game_img(self.__gui.templates['IMAGE_CHATDETECT'])) or self.__gui.find_game_img(self.__gui.templates['IMAGE_CHATSTICKER']):
                                detectAssistance = threading.Thread(target=self.detectAssistance())
                                detectAssistance.setDaemon(True)
                                detectAssistance.start
                            if position3 == False and position2 != False:
                                self.__gui.mouse_click_bg(position2)
                                time.sleep(1)
                            break
                        break
                    else:
                        break
                elif position2 == False:
                    _localVariable.isBossDetected=False
                    logging.info("Starting exploration.... ")
                    self.__gui.mouse_click_bg(position)
                    continue
                else:
                    self.__gui.mouse_click_bg(position3)
                    time.sleep(1)
                    break
            
            position=self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_FIGHT_PATH'])
            position2=self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_CHERRY_CAKE_PATH'])
            position3=self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_FIGHT_BOSS_PATH'])
            if position == False and position2 != False and position3 == False:
                position=(self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_FIGHT_PATH']) and self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_FIGHT_BOSS_PATH']))
                if position == False:
                    self.__gui.mouse_drag_bg(SLIDE_STORY_COORDINATE[1],SLIDE_STORY_COORDINATE[0])
                    _localVariable.detectCount -= 1
                    if _localVariable.detectCount < 1:
                        # self.__gui.mouse_drag_bg(SLIDE_STORY_COORDINATE[1],SLIDE_STORY_COORDINATE[0])
                        self.__gui.mouse_drag_bg(SLIDE_STORY_COORDINATE[0],SLIDE_STORY_COORDINATE[1])
                        _localVariable.detectCount=30

            position=self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_FIGHT_BOSS_PATH'])
            if position != False:
                logging.info("BOSS was detected: ")
                self.__gui.mouse_click_bg(position)
                _localVariable.isBossDetected=True
                cantattk+=1
                _idlecount=0
                time.sleep(1)
                continue

            position=self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_FIGHT_PATH'])
            if position != False:
                logging.info("Monster was detected... ")
                self.__gui.mouse_click_bg(position)
                cantattk+=1
                _idlecount=0
                time.sleep(1)
                continue

            #=========================================get ready=================================================
            position=self.__gui.find_game_img(self.__gui.templates['IMAGE_READY_PATH']) or self.__gui.find_game_img(self.__gui.templates['IMAGE_READY_PATH'])
            if position != False:
                logging.info("Starting battle.... ")
                self.__gui.mouse_click_bg(position)
                #time.sleep(2)
                continue

            #=========================================Finish=================================================
            #Fail
            position=self.__gui.find_game_img(self.__gui.templates['IMAGE_FAILED_PATH'])
            if position != False:
                cantattk=0
                _idlecount=0
                logging.info("Battle End, Fail..")
                self.__gui.mouse_click_bg(position)
                continue

            position=self.__gui.find_game_img(self.__gui.templates['IMAGE_FINISHED2_PATH'])
            if position != False:
                cantattk=0
                _idlecount=0
                self.__gui.mouse_click_bg(position)
                continue


            #check finish
            if (self.__gui.find_game_img(self.__gui.templates['IMAGE_FINISHED1_PATH']) or self.__gui.find_game_img(self.__gui.templates['IMAGE_FINISHED1S2_PATH'])) != False:
                logging.info("Battle End, Victory!")
                cantattk=0
                _idlecount=0
                while True:
                    self.__gui.mouse_click_bg((_displayChat+CLICK_FINISH2[0], CLICK_FINISH2[1]))
                    if self.__gui.find_game_img(self.__gui.templates['IMAGE_COOP2_SEAL']) or (_displayChat == 0 and self.__gui.find_game_img(self.__gui.templates['IMAGE_CHATDETECT'])) or self.__gui.find_game_img(self.__gui.templates['IMAGE_CHATSTICKER']):
                        detectAssistance = threading.Thread(target=self.detectAssistance())
                        detectAssistance.setDaemon(True)
                        detectAssistance.start

                    if self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_CHERRY_CAKE_PATH']) != False or self.__gui.find_game_img(self.__gui.templates['IMAGE_EMPTY_SUSHI']) != False:
                        time.sleep(1)
                        break

                    if self.__gui.find_game_img(self.__gui.templates['IMAGE_SOULMAX']) != False:
                        logging.info("Soul Max")
                        self.__gui.mouse_click_bg((_displayChat+CLICK_SOULMAX[0], CLICK_SOULMAX[1]))
                        time.sleep(1)
                        continue
                break

            #==========================================Reward settlement=============================================
            # if (self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_BACK_PATH'])!= False
            #     or self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_REWARD_CONFIRMED_PATH']) != False or self.__gui.find_game_img(IMAGE_STORY_REWARD_CONFIRMEDCN_PATH) != False):
            position=self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_GET_REWARD_PATH'])
            if position != False:
                logging.info("Get treasure.... ")
                self.__gui.mouse_click_bg(position)
                time.sleep(0.5)
                self.__gui.mouse_click_bg((_displayChat+CLICK_FINISH2[0], CLICK_FINISH2[1]))

            position=self.__gui.find_game_img(self.__gui.templates['IMAGE_STORY_REWARD_CONFIRMED_PATH'])
            if position != False:
                logging.info("Confirm.... ")
                self.__gui.mouse_click_bg((_displayChat+CLICK_FINISH2[0], CLICK_FINISH2[1]))
            
            else:
                _idlecount+=1
    
    def detectAssistance(self):
        global _displayChat, _idlecount
        position1 = self.__gui.find_game_img(self.__gui.templates['IMAGE_COOP2_SEAL'])
        position2 = self.__gui.find_game_img(self.__gui.templates['IMAGE_CHATSTICKER'])
        position3 = self.__gui.find_game_img(self.__gui.templates['IMAGE_CHATDETECT'])
        position4 = self.__gui.find_game_img(self.__gui.templates['IMAGE_CLOSEWANTED'])
        wq_jade = config['VALUE']['WQ_JADE']
        wq_coin = config['VALUE']['WQ_COIN']
        wq_sushi = config['VALUE']['WQ_SUSHI']
        wq_food = config['VALUE']['WQ_FOOD']

        if _displayChat == 0 and position3:
            _displayChat = 525
            self.__gui.recheckRect()
            logging.info('External chat detected.')

        if (not position3) and position2:
            self.__gui.mouse_click_bg(position2)
            _displayChat = 0
            self.__gui.recheckRect()
            logging.info('ChatPanel detected, closed!')

        if position1:
            if (self.__gui.find_game_img(self.__gui.templates['IMAGE_WQ_JADE']) and wq_jade
            ) or (self.__gui.find_game_img(self.__gui.templates['IMAGE_WQ_COIN']) and wq_coin
            ) or (self.__gui.find_game_img(self.__gui.templates['IMAGE_WQ_SUSHI']) and wq_sushi
            ) or ((self.__gui.find_game_img(self.__gui.templates['IMAGE_WQ_FOODDOG']) or self.__gui.find_game_img(self.__gui.templates['IMAGE_WQ_FOODCAT'])) and wq_food):
                logging.info("Accept wanted quest!")
                self.__gui.mouse_click_bg(position1[0] + 174, position1[1] + 222)
                screenshot = self.__gui.takescreenshot('คนเหลี่ยมๆ')
                self.create_file2(data=screenshot)
            else:
                logging.info("Refuse to accept the invitation for the wanted seal.")
                self.__gui.mouse_click_bg((position1[0] + 279, position1[1] + 309))
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
            self.gameModeSingleExplore()
            count+=1
            message="completed %s, remaining %s round"%(str(count),str(self.__total-count))
            self.create_file(data=str(count))
            logging.info(message)


if __name__ == '__main__':
    load_config()
