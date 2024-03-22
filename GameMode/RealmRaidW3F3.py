from Module.GameControl import *
from Module.ThreadGame import *
from Module.Util import *
from Module.loadconfig import *
import time
import subprocess

_localVariable=threading.local()
_displayChat=0
_cAttackRealm=0
_is3Realm=False
_exit = True
_isFail=0
CLICK_FINISH2=(_displayChat+694, 113)
START_SOUL_COORDINATE = (_displayChat+1075, 565)

class RealmRaidW3F3(threading.Thread):
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

    def gameModeRealmRaid(self):
        global _cAttackRealm, _displayChat, _is3Realm, _isFail, _exit
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
            
            if (_exit == False and (_isFail <= 3) and (self.__gui.find_game_img(config['DEFAULT']['IMAGE_BACK'], gray=1) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_BACK2'], gray=1, thread=0.87)) != False):
                print("Exit Battle..")
                self.__gui.send_esc_down()
                time.sleep(0.4)
                self.__gui.mouse_click_bg((_displayChat+655, 383))
                _exit = True

            #not enough ticket
            # if self.__gameMode == 6:
            position = (self.__gui.find_game_img(config['GB']['IMAGE_REALM_EMPTY_TICKET'], part=1, pos1=(1005, 10), pos2=(1105, 45), thread=0.88) or self.__gui.find_game_img(config['GB']['IMAGE_REALM_EMPTY_TICKET'], part=1, pos1=(1530, 10), pos2=(1630, 45), thread=0.97))
            positionCN = (self.__gui.find_game_img(config['CN']['IMAGE_REALM_EMPTY_TICKET'], part=1, pos1=(1005, 10), pos2=(1105, 45), thread=0.88) or self.__gui.find_game_img(config['CN']['IMAGE_REALM_EMPTY_TICKET'], part=1, pos1=(1530, 10), pos2=(1630, 45), thread=0.91))
            if  position or positionCN:
                printWithTime("DONE... ")
                # pyautogui.alert(text='REALM RAID DONE', title='FINISH', button='OK')
                total = str(self.__total)
                self.create_file(data=total)
                args = ['taskkill', '/F', '/PID', str(self.__pid)]
                subprocess.Popen(args, creationflags=subprocess.CREATE_NO_WINDOW)
                sys.exit()

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
            if _is3Realm != False and _isFail >= 3 and position4 != False:
                # print('[DEBUG] This should refresh')
                self.__gui.mouse_click_bg(position4)
                time.sleep(1)
                #This to Click OK button
                if self.__gui.find_game_img(config[svselect]['IMAGE_REALM_CANCEL']) != False:
                    self.__gui.mouse_click_bg((position4[0]-253,position4[1]-145))
                    printWithTime('set 3Realm raid state = False')
                    _is3Realm = False
                    _isFail = 0
                    time.sleep(1)
            
            if _is3Realm != False and (_isFail < 3) and position5 != False:
                time.sleep(1)
                if positionatk != False and _is3Realm != False:
                        self.__gui.mouse_click_bg(positionatk)
                        printWithTime("Click Enemy Section..")
                        _cAttackRealm+=1
                        _exit = False
                        time.sleep(1)
                        if position3:
                            self.__gui.mouse_click_bg(position3)
                        else:
                            self.__gui.mouse_click_bg((positionatk[0]-77,positionatk[1]+167))
                        time.sleep(2)
                        while True:
                            if self.__gui.find_game_img(config[svselect]['IMAGE_COOP2_SEAL']) or self.__gui.find_game_img(config[svselect]['IMAGE_CHATDETECT']):
                                detectAssistance = threading.Thread(target=self.detectAssistance())
                                detectAssistance.setDaemon(True)
                                detectAssistance.start
                            if (self.__gui.find_game_img(config['DEFAULT']['IMAGE_BACK'], gray=1) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_BACK2'], gray=1, thread=0.78)) != False:
                                self.__gui.send_esc_down()
                                time.sleep(0.4)
                                self.__gui.mouse_click_bg((_displayChat+655, 383))
                                _exit = True
                                break

            #This Click Enemy#=========================================================================================================
            if _is3Realm == False and position5 != False:
                time.sleep(1)
                if _is3Realm == False and position5 != False:
                    if positionatk != False and _is3Realm == False:
                        self.__gui.mouse_click_bg(positionatk)
                        printWithTime("Click Enemy Section..")
                        _cAttackRealm+=1
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
                _isFail+=1
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
        while self.__total-count>0:
            seconds=0
            while seconds:
                time.sleep(1)
                seconds-=1
            print("\n\n==================Starting a new round==================")
            self.gameModeRealmRaid()
            count+=1
            message="GameMode:RealmRaid, completed %s, remaining %s round"%(str(count),str(self.__total-count))
            self.create_file(data=str(count))
            printWithTime(message)


if __name__ == '__main__':
    load_config()