from Module.GameControl import *
from Module.ThreadGame import *
from Module.Util import *
from Module.loadconfig import *
import time
import pyautogui, subprocess

_localVariable=threading.local()
_displayChat=0
_is3Realm=False
_cAttackRealm=0
cantattk=0
_setround=0
_firstcheck=True

CLICK_FINISH=(_displayChat+568, 387)
CLICK_FINISH2=(_displayChat+694, 113)
SLIDE_STORY_COORDINATE=[(_displayChat+200,200),(_displayChat+1000,200)]
START_SOUL_COORDINATE = (_displayChat+1075, 565)

class Explor3Realm(threading.Thread):
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
                
    def gameModeExplore_3Realm(self):
        global _cAttackRealm, _setround, _firstcheck
        while True: 
            detectAssistance = threading.Thread(target=self.detectAssistance())
            detectAssistance.setDaemon(True)
            detectAssistance.start

            position=(self.__gui.find_game_img(config['REALM']['IMAGE_REALM_EMPTY_TICKET2'], gray=1) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_EMPTY_TICKET2CN'],thread=0.91) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_EMPTY_TICKET2CN'],thread=0.99))
            position2=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_LIST_CHAPTER_PATH'])  
            position3=self.__gui.find_game_img(config[svselect]['IMAGE_REALM_GUILD_PATH'])
            position4=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE'])
            position5=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_BOX_PATH'])
            #time.sleep(5)
            if position5 != False:
                printWithTime("Box Found. (Func.1)")
                self.__gui.mouse_click_bg(position5)
                time.sleep(1)
                if position4 != False:
                    self.__gui.mouse_click_bg(position4)
                    time.sleep(1)
                    self.__gui.mouse_click_bg(position5)
                    time.sleep(1)
                    continue
                
            position4=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE'])
            if position != False or position3 != False:
                printWithTime("Change to Realm Raid")
                while True:
                    if self.__gui.find_game_img(config[svselect]['IMAGE_REALM_EMPTY_TICKET'],thread=0.97) !=False:
                        printWithTime("Close RealmPage...")
                        self.__gui.mouse_click_bg((_displayChat+1070, 120))
                        if _firstcheck == False:
                            _setround+=1
                            self.create_file(data=str(_setround))
                            _firstcheck = True
                        time.sleep(1)
                        break
                        #sys.exit()
                    if position4 != False and position3 == False:
                        self.__gui.mouse_click_bg(position4)
                        printWithTime('Close.')
                        #Click icon realm
                        time.sleep(1)
                        position=self.__gui.find_game_img(config[svselect]['IMAGE_REALM_RAID_PATH'])
                        if position != False:
                            printWithTime("Click icon realm raid...")
                            self.__gui.mouse_click_bg(position)
                            time.sleep(2)
                            continue
                        break
                    else:
                        self.gameModeRealmRaid()

            if position == False and position2 != False or self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_CHERRY_CAKE_PATH']) != False or self.__gui.find_game_img(config[svselect]['IMAGE_STORY_START_PATH']) != False:
                self.gameModeExplor()
            
            #Fail
            position=self.__gui.find_game_img(config['DEFAULT']['IMAGE_FAILED_PATH'])
            if position != False:
                printWithTime("Failed..")
                cantattk=0
                _cAttackRealm=0
                self.__gui.mouse_click_bg(position)
                continue

            #check finish
            if (self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1_PATH']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1S2_PATH']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1S3_PATH']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED2_PATH'])) != False:
                printWithTime("Finishing...")
                cantattk=0
                while True:
                    self.__gui.mouse_click_bg(CLICK_FINISH2)
                    if (self.__gui.find_game_img(config['SOUL']['IMAGE_SOUL_ROOM_DETECT_PATH']) or self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_BACK_PATH']) or self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_CHERRY_CAKE_PATH'])) != False or (self.__gui.find_game_img(config[svselect]['IMAGE_BUFF'])) != False:
                        break
                    if self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE']) != False or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_JADE_PATH']) != False:
                        _cAttackRealm=0
                        break
                break

            #soulmax
            if self.__gui.find_game_img(config[svselect]['IMAGE_SOULMAX']) != False:
                printWithTime("Soul Max")
                self.__gui.mouse_click_bg(CLICK_FINISH)
                time.sleep(1)
                continue
    
    def gameModeExplor(self):
        global _displayChat, _cAutoRotation, cantattk, _setround, _firstcheck
        while True:
            detectAssistance = threading.Thread(target=self.detectAssistance())
            detectAssistance.setDaemon(True)
            detectAssistance.start

            position=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_BOX_PATH'])
            position2=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE'])
            if position != False:
                printWithTime("Box Found. (Func.2)")
                self.__gui.mouse_click_bg(position)
                time.sleep(4)
                if position != False and position2 != False:
                    self.__gui.mouse_click_bg(position2)
                    time.sleep(1)
                self.__gui.mouse_click_bg(position)
                time.sleep(1)

            position=(self.__gui.find_game_img(config[svselect]['IMAGE_STORY_LIMIT_PATH']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_EMPTY_SUSHI']))
            if position != False or cantattk >= 12:
                printWithTime("Unable to process, please check.")
                total = str(self.__total)
                self.create_file(data=total)
                args = ['taskkill', '/F', '/PID', str(self.__pid)]
                subprocess.Popen(args)
                sys.exit()
                
            position=self.__gui.find_game_img(config[svselect]['IMAGE_STORY_AUTOFOOD_PATH'])
            if position != False:
                printWithTime("Click Auto Rotation")
                self.__gui.mouse_click_bg((_displayChat+117, 599))
                _cAutoRotation+=1
                if _cAutoRotation >= 3:
                    printWithTime("Exit!")
                    pyautogui.alert(text='auto rotation food runs out, stop working..', title='Exit!', button='OK')
                    args = ['taskkill', '/F', '/PID', str(self.__pid)]
                    subprocess.Popen(args)
                time.sleep(1)

            position=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_CHERRY_CAKE_PATH'])
            if position == False:
                time.sleep(1)
                position=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_LIST_CHAPTER_PATH'])  
                if _firstcheck == False and (self.__gui.find_game_img(config['REALM']['IMAGE_REALM_EMPTY_TICKET2'], gray=1) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_EMPTY_TICKET2CN'],thread=0.91) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_EMPTY_TICKET2CN'],thread=0.99)) != False:
                    _setround+=1
                    self.create_file(data=str(_setround))
                    _firstcheck = True
                    self.gameModeExplore_3Realm() 
                elif position != False:
                    _localVariable.isBossDetected=False
                    printWithTime("Entering last chapter..")
                    self.__gui.mouse_click_bg((position[0],position[1]+400))
                    time.sleep(1)
                    continue
                
            position=self.__gui.find_game_img(config[svselect]['IMAGE_STORY_START_PATH'])
            position2=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_BOX_PATH'])
            position3=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE'])
            if position != False:
                #time.sleep(0.5)
                if position2 != False and position3 != False:
                    printWithTime("Box Found (Func3)")
                    self.__gui.mouse_click_bg(position)
                    time.sleep(2)
                    if position2 != False:
                        while True:
                            self.__gui.mouse_click_bg(position3)
                            time.sleep(1)
                            if position3 == False and position2 != False:
                                self.__gui.mouse_click_bg(position2)
                                time.sleep(1)
                            break
                        break
                    else:
                        break
                elif position2 == False:
                    _localVariable.isBossDetected=False
                    printWithTime("Starting exploration.... ")
                    self.__gui.mouse_click_bg(position)
                    cantattk+=1
                    _firstcheck = False
                    continue
                else:
                    self.__gui.mouse_click_bg(position3)
                    time.sleep(1)
                    break
            
            position=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_FIGHT_PATH'])
            position2=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_CHERRY_CAKE_PATH'])
            position3=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_FIGHT_BOSS_PATH'])
            if position == False and position2 != False and position3 == False:
                position=(self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_FIGHT_PATH']) and self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_FIGHT_BOSS_PATH']))
                if position == False:
                    self.__gui.mouse_drag_bg(SLIDE_STORY_COORDINATE[1],SLIDE_STORY_COORDINATE[0])
                    _localVariable.detectCount -= 1
                    if _localVariable.detectCount < 1:
                        # self.__gui.mouse_drag_bg(SLIDE_STORY_COORDINATE[1],SLIDE_STORY_COORDINATE[0])
                        self.__gui.mouse_drag_bg(SLIDE_STORY_COORDINATE[0],SLIDE_STORY_COORDINATE[1])
                        _localVariable.detectCount=30
            position=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_FIGHT_BOSS_PATH'])
            if position != False:
                printWithTime("BOSS was detected: ")
                self.__gui.mouse_click_bg(position)
                _localVariable.isBossDetected=True
                _firstcheck = False
                cantattk+=1
                time.sleep(1)
                continue

            position=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_FIGHT_PATH'])
            if position != False:
                printWithTime("Monster was detected... ")
                self.__gui.mouse_click_bg(position)
                cantattk+=1
                time.sleep(1)
                continue

            #=========================================get ready=================================================
            position=self.__gui.find_game_img(config[svselect]['IMAGE_READY_PATH']) or self.__gui.find_game_img(config[svselect]['IMAGE_READY_PATH'])
            if position != False:
                printWithTime("Starting battle.... ")
                self.__gui.mouse_click_bg(position)
                #time.sleep(2)
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
            if (self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1_PATH']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1S2_PATH'])) != False:
                printWithTime("Finishing...")
                cantattk=0
                while True:
                    self.__gui.mouse_click_bg(CLICK_FINISH2)
                    if (self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_CHERRY_CAKE_PATH']) != False or 
                        self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_LIST_CHAPTER_PATH']) != False or 
                        self.__gui.find_game_img(config['DEFAULT']['IMAGE_BUFF']) != False):
                        time.sleep(1)
                        break
                    #soulmax
                    if self.__gui.find_game_img(config[svselect]['IMAGE_SOULMAX']) != False:
                        printWithTime("Soul Max")
                        self.__gui.mouse_click_bg(CLICK_FINISH)
                        time.sleep(1)
                        continue
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
    
    def gameModeRealmRaid(self):
        global _cAttackRealm, _displayChat, _is3Realm, _setround, _firstcheck
        while True:
            detectAssistance = threading.Thread(target=self.detectAssistance())
            detectAssistance.setDaemon(True)
            detectAssistance.start
            #If Found Daruma
            position=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_FN3R_PATH'])
            position2=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE'])
            if position and position2:
                printWithTime('3 Realm Raid Reward')
                time.sleep(2)
                self.__gui.mouse_click_bg(CLICK_FINISH2)
                time.sleep(2)
                _is3Realm = True

            #not enough ticket
            # if self.__gameMode == 6:
            position = (self.__gui.find_game_img(config['GB']['IMAGE_REALM_EMPTY_TICKET'], part=1, pos1=(1005, 10), pos2=(1105, 45), thread=0.88) or self.__gui.find_game_img(config['GB']['IMAGE_REALM_EMPTY_TICKET'], part=1, pos1=(1530, 10), pos2=(1630, 45), thread=0.97))
            positionCN = (self.__gui.find_game_img(config['CN']['IMAGE_REALM_EMPTY_TICKET'], part=1, pos1=(1005, 10), pos2=(1105, 45), thread=0.88) or self.__gui.find_game_img(config['CN']['IMAGE_REALM_EMPTY_TICKET'], part=1, pos1=(1530, 10), pos2=(1630, 45), thread=0.91))
            if  position or positionCN:
                time.sleep(1)
                printWithTime("Game Mode Story")
                self.__gui.mouse_click_bg((_displayChat+1063, 116))
                time.sleep(2)
                if _firstcheck == False:
                    _setround+=1
                    self.create_file(data=str(_setround))
                    _firstcheck = True
                self.gameModeExplore_3Realm()

            #Click icon realm
            position=self.__gui.find_game_img(config[svselect]['IMAGE_REALM_RAID_PATH'])
            if position != False:
                printWithTime("Click icon realm raid...")
                self.__gui.mouse_click_bg(position)
                time.sleep(3)
                continue
            
            #lock line up
            position=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_LOCK_PATH'])
            if position != False:
                printWithTime("Successfully lock lineup...")
                self.__gui.mouse_click_bg(position)
                continue
            
            if _is3Realm == False:
                position=(self.__gui.find_game_img(config['REALM']['IMAGE_REALM_3RAID_PATH']) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_3RAID2_PATH']))
                if position == False:
                    # printWithTime('Not Found 3Realm raid icon')
                    # _is3Realm = False
                    pass
                else:
                    printWithTime('set 3Realm raid state = True')
                    _is3Realm = True

            #Click Realm
            position=(self.__gui.find_game_img(config['REALM']['IMAGE_REALM_SECTION_PATH']) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_SECTIONFROG_PATH'], thread=0.97))
            position2=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_SECTION2_PATH'])
            positionatk=(position or position2)
            position3=self.__gui.find_game_img(config[svselect]['IMAGE_REALM_ATK_PATH'])
            position4=self.__gui.find_game_img(config[svselect]['IMAGE_REALM_REFRESH_PATH'],gray=0)
            position5=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE'])
            #This to Refresh#=========================================================================================================
            if _is3Realm != False and position4 != False:
                # print('[DEBUG] This should refresh')
                self.__gui.mouse_click_bg(position4)
                time.sleep(1)
                #This to Click OK button
                if self.__gui.find_game_img(config[svselect]['IMAGE_REALM_CANCEL']) != False:
                    self.__gui.mouse_click_bg((position4[0]-253,position4[1]-145))
                    printWithTime('set 3Realm raid state = False')
                    _is3Realm = False
                    time.sleep(1)
            
            #This Click Enemy#=========================================================================================================
            if _is3Realm == False and position5 != False:
                time.sleep(1)
                if _is3Realm == False and position5 != False:
                    if positionatk != False and _is3Realm == False:
                        self.__gui.mouse_click_bg(positionatk)
                        printWithTime("Click Enemy Section..")
                        _cAttackRealm+=1
                        _firstcheck = False
                        time.sleep(2)
                        if position3:
                            self.__gui.mouse_click_bg(position3)
                        else:
                            self.__gui.mouse_click_bg((positionatk[0]-77,positionatk[1]+167))
                        time.sleep(1)
                        # self.gameModeRealmRaid()
                #else====================================================================================================
            if positionatk == False and position4 != False:
                print('[DEBUG] This is "Enemy Cant Attalck"')
                time.sleep(1)
                self.__gui.mouse_click_bg(position4)
                time.sleep(1)
                #This to Click OK button
                if self.__gui.find_game_img(config[svselect]['IMAGE_REALM_CANCEL']) != False:
                    self.__gui.mouse_click_bg((position4[0]-253,position4[1]-145))
                    printWithTime('set 3Realm raid state = False')
                    _is3Realm = False
                    time.sleep(1)
            
            #=========================================get ready=================================================
            position=self.__gui.find_game_img(config[svselect]['IMAGE_READY_PATH'])
            if position != False:
                # printWithTime("Starting battle.... ")
                self.__gui.mouse_click_bg(position)
                time.sleep(2)
                continue

            #Fail
            position=self.__gui.find_game_img(config['DEFAULT']['IMAGE_FAILED_PATH'])
            if position != False:
                printWithTime("Failed..")
                _cAttackRealm=0
                while True:
                    if (self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE']) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_JADE_PATH'])) != False:
                        _cAttackRealm=0
                        break
                    self.__gui.mouse_click_bg(CLICK_FINISH2)

            #check finish
            if (self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1_PATH']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1S3_PATH']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED2_PATH'])) != False:
                printWithTime("Finishing...")
                #time.sleep(5)
                while True:
                    if (self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE']) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_JADE_PATH'])) != False:
                        _cAttackRealm=0
                        break
                    self.__gui.mouse_click_bg(CLICK_FINISH2)
                break
    
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
            self.gameModeExplore_3Realm()
            count+=1
            message="GameMode:Explor+Realm, completed %s, remaining %s round"%(str(count),str(self.__total-count))
            # self.create_file(data=str(count))
            printWithTime(message)


if __name__ == '__main__':
    load_config()
