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

class Explore(threading.Thread):
    def __init__(self,Server, windowName,total,wanted,wtdelay,findimgdelay,pid):
        global svselect
        threading.Thread.__init__(self)
        self.__server=Server
        svselect=self.__server
        self.__hwnd=windowName
        self.__total=total
        self.__wanted=wanted
        self.__wtdelay=wtdelay
        self.__delay=findimgdelay
        self.__pid=pid
        self.__gui=GameControl(self.__hwnd,0, self.__delay)

    def gameModeExplore(self):
        global _isLeader, _cAutoRotation, cantattk, waittime
        CLICK_FINISH=(_displayChat+568, 387)
        CLICK_FINISH2=(_displayChat+694, 113)
        SLIDE_STORY_COORDINATE=[(_displayChat+200,200),(_displayChat+1000,200)]
        while True:
            detectAssistance = threading.Thread(target=self.detectAssistance())
            detectAssistance.setDaemon(True)
            detectAssistance.start

            position=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_ACCEPT_PATH'])
            if position != False:
                printWithTime("Accept Invite.")
                self.__gui.mouse_click_bg(position)  
                time.sleep(1)
                continue

            position=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_BOX_PATH'])
            if position != False:
                printWithTime("Box Found. (Func.2)")
                self.__gui.mouse_click_bg(position)
            if self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED2_PATH']) != False:
                self.__gui.mouse_click_bg(CLICK_FINISH)
            
            if self.__gui.find_game_img(config['SOUL']['IMAGE_SOUL_INVITE_PATH']) != False:
                waittime+=1
                if waittime>=12:
                    self.__gui.mouse_click_bg((_displayChat+960, 225))
                    time.sleep(2)
                    self.__gui.mouse_click_bg((_displayChat+444, 514))
                    waittime=0
            
            position=self.__gui.find_game_img(config[svselect]['IMAGE_SOUL_INVITE_DIALOG_PATH'])
            if position != False:
                printWithTime("Invited..")
                time.sleep(1)
                self.__gui.mouse_click_bg((_displayChat+position[0]+170,position[1]+100))
            
            position=(self.__gui.find_game_img(config[svselect]['IMAGE_STORY_LIMIT_PATH']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_EMPTY_SUSHI']))
            if position != False or cantattk >= 12:
                printWithTime("Unable to process, please check.")
                total = str(self.__total)
                self.create_file(data=total)
                args = ['taskkill', '/F', '/PID', str(self.__pid)]
                subprocess.Popen(args, creationflags=subprocess.CREATE_NO_WINDOW)
                sys.exit()
                    
            position=self.__gui.find_game_img(config[svselect]['IMAGE_SOUL_START_PATH'])
            position2=self.__gui.find_game_img(config['SOUL']['IMAGE_SOUL_INVITE_PATH'])
            if position != False and position2 == False:
                printWithTime("Start... ")
                self.__gui.mouse_click_bg(position)
                waittime=0
                time.sleep(1)

            position=self.__gui.find_game_img(config[svselect]['IMAGE_STORY_AUTOFOOD_PATH'])
            if position != False:
                printWithTime("Click Auto Rotation")
                self.__gui.mouse_click_bg((_displayChat+117, 599))
                _cAutoRotation+=1
                if _cAutoRotation >= 5:
                    printWithTime("Exit!")
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
                    printWithTime("Leader Detected in display..")
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
                printWithTime("BOSS was detected: ")
                self.__gui.mouse_click_bg(position)
                _localVariable.isBossDetected=True
                cantattk+=1
                time.sleep(1)
                continue

            position=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_FIGHT_PATH'])
            if (_isLeader and position) != False:
                printWithTime("Monster was detected... ")
                self.__gui.mouse_click_bg(position)
                cantattk+=1
                time.sleep(1)
                continue
            #=========================================get ready=================================================
            position=self.__gui.find_game_img(config[svselect]['IMAGE_READY_PATH'],thread=0.8)
            if position != False:
                printWithTime("Starting battle.... ")
                self.__gui.mouse_click_bg(position)
                time.sleep(2)
                continue

            #=========================================Finish=================================================
            #Fail
            position=self.__gui.find_game_img(config['DEFAULT']['IMAGE_FAILED_PATH'])
            if position != False:
                cantattk=0
                printWithTime("Failed..")
                self.__gui.mouse_click_bg(position)
                continue

            #check finish
            if (self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1_PATH']) or 
                self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1S2_PATH']) != False) and (
                self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_LIST_CHAPTER_PATH']) or 
                self.__gui.find_game_img(config['SOUL']['IMAGE_SOUL_ROOM_DETECT_PATH']) == False):
                printWithTime("Finishing...")
                cantattk=0
                while True:
                    if (self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_CHERRY_CAKE_PATH']) != False or 
                        self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_ACCEPT_PATH']) != False or 
                        self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_LIST_CHAPTER_PATH']) != False or 
                        self.__gui.find_game_img(config['DEFAULT']['IMAGE_BUFF']) != False):
                        time.sleep(1)
                        break
                    if self.__gui.find_game_img(config[svselect]['IMAGE_SOULMAX']) != False:
                        printWithTime("Soul Max")
                        self.__gui.mouse_click_bg(CLICK_FINISH)
                        time.sleep(1)
                        continue
                    self.__gui.mouse_click_bg(CLICK_FINISH2)
                    time.sleep(0.01)
                break

            #==========================================Reward settlement=============================================
            position=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_GET_REWARD_PATH'])
            if position != False:
                printWithTime("Get treasure.... ")
                self.__gui.send_esc_down()
                time.sleep(0.4)
                self.__gui.mouse_click_bg((_displayChat+655, 383))

            #soulmax
            if self.__gui.find_game_img(config[svselect]['IMAGE_SOULMAX']) != False:
                printWithTime("Soul Max")
                self.__gui.mouse_click_bg(CLICK_FINISH)
                time.sleep(1)
                continue

            
    
    def detectAssistance(self):
        global _displayChat
        wanteddelay = self.__wtdelay
        # while True:
        time.sleep(wanteddelay+0.001)
        position1 = self.__gui.find_game_img(config[svselect]['IMAGE_COOP2_SEAL'])
        position2 = self.__gui.find_game_img(config[svselect]['IMAGE_CHATSTICKER'])
        position3 = self.__gui.find_game_img(config[svselect]['IMAGE_CHATDETECT'])

        if _displayChat == 0 and position3:
            _displayChat = 525
            printWithTime('External chat detected..')

        if not position3 and position2:
            # time.sleep(0.1)
            self.__gui.mouse_click_bg(position2)
            _displayChat = 0
            printWithTime('ChatPanel detected, closed..')
            # time.sleep(0.1)

        if self.__wanted == 1 and position1:
            printWithTime("Refuse to accept the invitation for the wanted seal...")
            self.__gui.mouse_click_bg((position1[0] + 174, position1[1] + 308))
            # time.sleep(0.5)

        if self.__wanted == 2 and position1:
            self.__gui.mouse_click_bg((position1[0] + 174, position1[1] + 222))
            printWithTime("Accept wanted quest...")
            self.create_file2(data='True')
            # time.sleep(0.5)
            # continue

    def create_file(self, data='0'):
        temp_path = f"runprocess/temp{self.__pid}.txt"
        with open(temp_path, "w") as file:
            file.write(data)
            file.close
    
    def create_file2(self, data='False'):
        temp_path = f"runprocess/wanted{self.__pid}.txt"
        with open(temp_path, "w") as file:
            file.write(data)
            file.close

    def run(self):
        count=0
        _localVariable.detectCount=30
        while self.__total-count>0:
            seconds=0
            while seconds:
                time.sleep(1)
                seconds-=1
            print("\n\n==================Starting a new round==================")
            self.gameModeExplore()
            count+=1
            message="GameMode:Explor, completed %s, remaining %s round"%(str(count),str(self.__total-count))
            self.create_file(data=str(count))
            printWithTime(message)


if __name__ == '__main__':
    load_config()
