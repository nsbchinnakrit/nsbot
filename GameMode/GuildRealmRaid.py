<<<<<<< HEAD
from Module.GameControl import *
from Module.ThreadGame import *
from Module.Util import *
from Module.loadconfig import *
import time
import subprocess

_displayChat=0
_cAttackRealm=0
SCROLL_DOWN=[(910, 500),(910, 386)]
CLICK_FINISH=(_displayChat+694, 113)
START_SOUL_COORDINATE = (_displayChat+1075, 565)

class GuildRealmRaid(threading.Thread):
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

    def gameModeGuildRealmRaid(self):
        global _isPaused, _displayChat, _cAttackRealm
        while True:
            detectAssistance = threading.Thread(target=self.detectAssistance())
            detectAssistance.setDaemon(True)
            detectAssistance.start
            
            position=self.__gui.find_game_img(config[svselect]['IMAGE_REALM_RAID_PATH'])
            if position != False:
                printWithTime("Click icon realm raid...")
                self.__gui.mouse_click_bg(position)
                time.sleep(2)
                continue

            #Click Guild Realm Page
            position=self.__gui.find_game_img(config[svselect]['IMAGE_REALM_GUILD_PATH'])
            if position != False:
                printWithTime("Open Guild Realm Page..")
                self.__gui.mouse_click_bg(position)
                continue

            #lock line up
            position=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_LOCK_PATH'])
            if position != False:
                printWithTime("Successfully lock lineup...")
                self.__gui.mouse_click_bg(position)
                continue
            
            #KO or Page End
            position=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GUILDPAGEEND_PATH'])
            position2=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_KO_PATH'])
            if position !=False and position2 !=False:
                total = str(self.__total)
                self.create_file(data=total)
                args = ['taskkill', '/F', '/PID', str(self.__pid)]
                subprocess.Popen(args, creationflags=subprocess.CREATE_NO_WINDOW)
                sys.exit()
                
            #If Can't Attack Enemy 
            position=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE'])
            if (_cAttackRealm >= 5) and (position != False):
                time.sleep(1)
                printWithTime("Reopening Guild Realm Raid")
                _cAttackRealm = 0
                self.__gui.mouse_click_bg(position)
                self.__gui.mouse_click_bg(position)
                time.sleep(1)
                if position != False:
                    self.__gui.mouse_click_bg(position)
                    continue
            
            #Drag mouse down if enemy not found
            guildscroll=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GUILDSCROLL_PATH'])
            position=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_SECTION_PATH'])
            positionGB=(self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GRAIDCOUNT'], part=1, pos1=(760, 500), pos2=(810, 525), thread=0.88) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GRAIDCOUNT'], part=1, pos1=(226, 492), pos2=(286, 529), thread=0.97))
            positionCN=(self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GRAIDCOUNT_CN'], part=1, pos1=(760, 500), pos2=(810, 525), thread=0.88) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GRAIDCOUNT_CN'], part=1, pos1=(226, 492), pos2=(286, 529), thread=0.97))
            position1= positionGB or positionCN
            position2=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GUILDPAGEEND_PATH'])
            if (guildscroll != False and position1 == False) and position == False:
                printWithTime("Looking for enemy")
                if position2:
                    self.__gui.mouse_drag_bg(SCROLL_DOWN[1],SCROLL_DOWN[0])
                else:
                    self.__gui.mouse_drag_bg(SCROLL_DOWN[0],SCROLL_DOWN[1])
                    continue
            
            #Click Realm
            guild=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GUILDSCROLL_PATH'])
            position=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_SECTION_PATH'])
            positionGB=(self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GRAIDCOUNT'], part=1, pos1=(760, 500), pos2=(810, 525), thread=0.88) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GRAIDCOUNT'], part=1, pos1=(226, 492), pos2=(286, 529), thread=0.97))
            positionCN=(self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GRAIDCOUNT_CN'], part=1, pos1=(760, 500), pos2=(810, 525), thread=0.88) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GRAIDCOUNT_CN'], part=1, pos1=(226, 492), pos2=(286, 529), thread=0.97))
            position1= positionGB or positionCN
            position2=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE'])
            # Click icon realm
            
            if (position and guild) != False and position1 == False:
                printWithTime("Enemy was found...")
                self.__gui.mouse_click_bg(position)
                _cAttackRealm+=1
                time.sleep(0.5)
                atk=self.__gui.find_game_img(config[svselect]['IMAGE_REALM_ATK_PATH'])
                
                if atk != False and position2 != False:
                    self.__gui.mouse_click_bg(atk)
                    continue
                if atk == False and position2 != False:
                    self.__gui.mouse_click_bg((_displayChat+position[0]-77,position[1]+194))    
                    self.__gui.mouse_click_bg((_displayChat+position[0]-77,position[1]+190))    
                    #If Can't Attack Enemy 
                    position=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE'])
                    position2=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CANTATTK_PATH'],gray=0)
                    if position2 != False:
                        time.sleep(1)
                        printWithTime("Reopening Guild Realm Raid")
                        self.__gui.mouse_click_bg(position)
                        self.__gui.mouse_click_bg(position)
                        time.sleep(1)
                        if position != False:
                            self.__gui.mouse_click_bg(position)
                            continue
                    else:
                        self.__gui.mouse_click_bg((35, 51))
                        continue 


            #Fail
            position=self.__gui.find_game_img(config['DEFAULT']['IMAGE_FAILED_PATH'])
            if position != False:
                printWithTime("Failed..")
                self.__gui.mouse_click_bg(START_SOUL_COORDINATE)
                _cAttackRealm=0
                continue
                
           #check finish
            if (self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1_PATH']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1S3_PATH']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED2_PATH'])) != False:
                printWithTime("Finishing...")
                #time.sleep(5)
                while True:
                    if (self.__gui.find_game_img(config['REALM']['IMAGE_REALM_SECTION_PATH']) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE']) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GUILDSCROLL_PATH'])) != False:
                        time.sleep(1)
                        _cAttackRealm=0
                        break
                    self.__gui.mouse_click_bg(CLICK_FINISH)
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
            self.gameModeGuildRealmRaid()
            # self.test()
            count+=1
            message="GameMode:Guild RealmRaid, completed %s, remaining %s round"%(str(count),str(self.__total-count))
            self.create_file(data=str(count))
            printWithTime(message)


if __name__ == '__main__':
=======
from Module.GameControl import *
from Module.ThreadGame import *
from Module.Util import *
from Module.loadconfig import *
import time
import subprocess

_displayChat=0
_cAttackRealm=0
SCROLL_DOWN=[(910, 500),(910, 386)]
CLICK_FINISH=(_displayChat+694, 113)
START_SOUL_COORDINATE = (_displayChat+1075, 565)

class GuildRealmRaid(threading.Thread):
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

    def gameModeGuildRealmRaid(self):
        global _isPaused, _displayChat, _cAttackRealm
        while True:
            detectAssistance = threading.Thread(target=self.detectAssistance())
            detectAssistance.setDaemon(True)
            detectAssistance.start
            
            position=self.__gui.find_game_img(config[svselect]['IMAGE_REALM_RAID_PATH'])
            if position != False:
                printWithTime("Click icon realm raid...")
                self.__gui.mouse_click_bg(position)
                time.sleep(2)
                continue

            #Click Guild Realm Page
            position=self.__gui.find_game_img(config[svselect]['IMAGE_REALM_GUILD_PATH'])
            if position != False:
                printWithTime("Open Guild Realm Page..")
                self.__gui.mouse_click_bg(position)
                continue

            #lock line up
            position=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_LOCK_PATH'])
            if position != False:
                printWithTime("Successfully lock lineup...")
                self.__gui.mouse_click_bg(position)
                continue
            
            #KO or Page End
            position=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GUILDPAGEEND_PATH'])
            position2=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_KO_PATH'])
            if position !=False and position2 !=False:
                total = str(self.__total)
                self.create_file(data=total)
                args = ['taskkill', '/F', '/PID', str(self.__pid)]
                subprocess.Popen(args, creationflags=subprocess.CREATE_NO_WINDOW)
                sys.exit()
                
            #If Can't Attack Enemy 
            position=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE'])
            if (_cAttackRealm >= 5) and (position != False):
                time.sleep(1)
                printWithTime("Reopening Guild Realm Raid")
                _cAttackRealm = 0
                self.__gui.mouse_click_bg(position)
                self.__gui.mouse_click_bg(position)
                time.sleep(1)
                if position != False:
                    self.__gui.mouse_click_bg(position)
                    continue
            
            #Drag mouse down if enemy not found
            guildscroll=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GUILDSCROLL_PATH'])
            position=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_SECTION_PATH'])
            positionGB=(self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GRAIDCOUNT'], part=1, pos1=(760, 500), pos2=(810, 525), thread=0.88) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GRAIDCOUNT'], part=1, pos1=(226, 492), pos2=(286, 529), thread=0.97))
            positionCN=(self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GRAIDCOUNT_CN'], part=1, pos1=(760, 500), pos2=(810, 525), thread=0.88) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GRAIDCOUNT_CN'], part=1, pos1=(226, 492), pos2=(286, 529), thread=0.97))
            position1= positionGB or positionCN
            position2=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GUILDPAGEEND_PATH'])
            if (guildscroll != False and position1 == False) and position == False:
                printWithTime("Looking for enemy")
                if position2:
                    self.__gui.mouse_drag_bg(SCROLL_DOWN[1],SCROLL_DOWN[0])
                else:
                    self.__gui.mouse_drag_bg(SCROLL_DOWN[0],SCROLL_DOWN[1])
                    continue
            
            #Click Realm
            guild=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GUILDSCROLL_PATH'])
            position=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_SECTION_PATH'])
            positionGB=(self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GRAIDCOUNT'], part=1, pos1=(760, 500), pos2=(810, 525), thread=0.88) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GRAIDCOUNT'], part=1, pos1=(226, 492), pos2=(286, 529), thread=0.97))
            positionCN=(self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GRAIDCOUNT_CN'], part=1, pos1=(760, 500), pos2=(810, 525), thread=0.88) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GRAIDCOUNT_CN'], part=1, pos1=(226, 492), pos2=(286, 529), thread=0.97))
            position1= positionGB or positionCN
            position2=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE'])
            # Click icon realm
            
            if (position and guild) != False and position1 == False:
                printWithTime("Enemy was found...")
                self.__gui.mouse_click_bg(position)
                _cAttackRealm+=1
                time.sleep(0.5)
                atk=self.__gui.find_game_img(config[svselect]['IMAGE_REALM_ATK_PATH'])
                
                if atk != False and position2 != False:
                    self.__gui.mouse_click_bg(atk)
                    continue
                if atk == False and position2 != False:
                    self.__gui.mouse_click_bg((_displayChat+position[0]-77,position[1]+194))    
                    self.__gui.mouse_click_bg((_displayChat+position[0]-77,position[1]+190))    
                    #If Can't Attack Enemy 
                    position=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE'])
                    position2=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CANTATTK_PATH'],gray=0)
                    if position2 != False:
                        time.sleep(1)
                        printWithTime("Reopening Guild Realm Raid")
                        self.__gui.mouse_click_bg(position)
                        self.__gui.mouse_click_bg(position)
                        time.sleep(1)
                        if position != False:
                            self.__gui.mouse_click_bg(position)
                            continue
                    else:
                        self.__gui.mouse_click_bg((35, 51))
                        continue 


            #Fail
            position=self.__gui.find_game_img(config['DEFAULT']['IMAGE_FAILED_PATH'])
            if position != False:
                printWithTime("Failed..")
                self.__gui.mouse_click_bg(START_SOUL_COORDINATE)
                _cAttackRealm=0
                continue
                
           #check finish
            if (self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1_PATH']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1S3_PATH']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED2_PATH'])) != False:
                printWithTime("Finishing...")
                #time.sleep(5)
                while True:
                    if (self.__gui.find_game_img(config['REALM']['IMAGE_REALM_SECTION_PATH']) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE']) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GUILDSCROLL_PATH'])) != False:
                        time.sleep(1)
                        _cAttackRealm=0
                        break
                    self.__gui.mouse_click_bg(CLICK_FINISH)
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
            self.gameModeGuildRealmRaid()
            # self.test()
            count+=1
            message="GameMode:Guild RealmRaid, completed %s, remaining %s round"%(str(count),str(self.__total-count))
            self.create_file(data=str(count))
            printWithTime(message)


if __name__ == '__main__':
>>>>>>> 5aba08ced5481b6f7896a7cef616b87c6e9f4d1e
    load_config()