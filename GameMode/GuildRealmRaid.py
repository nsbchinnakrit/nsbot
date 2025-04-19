from Module.GameControl import *
from Module.ThreadGame import *
from Module.Util import *
from Module.loadconfig import *
import time
import subprocess

_displayChat=0
_cAttackRealm=0
_idlecount=0
_scrollcount=0
_need1scrollup=False
SCROLL_DOWN=[(910, 520),(910, 165)]
CLICK_FINISH=(35, 510)
START_SOUL_COORDINATE = (1075, 565)

class GuildRealmRaid(threading.Thread):
    def __init__(self,Server, windowName, beforetotal, total, pid, bondlingmode, pactsettings, crystal_use, tomb, snowball, azure, kuro, markboss):
        global svselect
        threading.Thread.__init__(self)
        self.__server=Server
        svselect=self.__server
        self.__hwnd=windowName
        self.__beforetotal=beforetotal
        self.__total=total
        self.__pid=pid
        self.__gui=GameControl(self.__hwnd,0)

    def gameModeGuildRealmRaid(self):
        global _isPaused, _displayChat, _cAttackRealm, _idlecount, _scrollcount, _need1scrollup
        while True:
            detectAssistance = threading.Thread(target=self.detectAssistance())
            detectAssistance.setDaemon(True)
            detectAssistance.start

            #Room Back
            position=self.__gui.find_game_img(config['DEFAULT']['IMAGE_ROOM_BACK'])
            if position != False:
                logging.info("Exit Room..")
                self.__gui.mouse_click_bg(position)
                continue
            
            position=self.__gui.find_game_img(config[svselect]['IMAGE_REALM_RAID_PATH'])
            if position != False:
                logging.info("Enter Realm Raid")
                self.__gui.mouse_click_bg(position)
                time.sleep(2)
                continue

            #Click Guild Realm Page
            position=self.__gui.find_game_img(config[svselect]['IMAGE_REALM_GUILD_PATH'])
            if position != False:
                logging.info("Open Guild Realm Raid")
                self.__gui.mouse_click_bg(position)
                _need1scrollup = False
                continue

            #lock line up
            position=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_LOCK_PATH'])
            if position != False:
                logging.info("Successfully lock lineup..")
                self.__gui.mouse_click_bg(position)
                continue
            
            #KO or Page End
            position=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GUILDPAGEEND_PATH'])
            position2=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_KO_PATH'])
            if (position !=False and position2 !=False) or _scrollcount > 2:
                logging.info("Process Finish.. Exit!")
                total = str(self.__total)
                self.create_file(data=total)
                args = ['taskkill', '/F', '/PID', str(self.__pid)]
                subprocess.Popen(args, creationflags=subprocess.CREATE_NO_WINDOW)
                sys.exit()
                
            #If Can't Attack Enemy 
            position=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE'])
            if (_cAttackRealm >= 5) and (position != False):
                time.sleep(1)
                logging.info("Reopen Guild Realm Raid")
                _cAttackRealm = 0
                self.__gui.mouse_click_bg(position)
                self.__gui.mouse_click_bg(position)
                time.sleep(1)
                if position != False:
                    self.__gui.mouse_click_bg(position)
                    continue
            
            #Drag mouse down if enemy not found
            guildscroll=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GUILDSCROLL_PATH'])
            position=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_SECTION2_PATH'])
            positionGB=(self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GRAIDCOUNT'], part=1, pos1=(760, 500), pos2=(810, 525), thread=0.95) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GRAIDCOUNT'], part=1, pos1=(226, 492), pos2=(286, 529), thread=0.97))
            positionCN=(self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GRAIDCOUNT_CN'], part=1, pos1=(760, 500), pos2=(810, 525), thread=0.88) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GRAIDCOUNT_CN'], part=1, pos1=(226, 492), pos2=(286, 529), thread=0.97))
            position1= positionGB or positionCN
            position2=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GUILDPAGEEND_PATH']) #รูปเขตที่ตีไปแล้ว
            if (guildscroll != False and position1 == False) and position == False:
                logging.debug("Looking for enemy")
                if position2:
                    logging.debug("scroll up")
                    _scrollcount += 1
                    logging.debug("_scrollcount:%s"%_scrollcount)
                    while True:
                        if self.__gui.find_game_img(config[svselect]['IMAGE_COOP2_SEAL']) or (_displayChat == 0 and self.__gui.find_game_img(config[svselect]['IMAGE_CHATDETECT'])) or self.__gui.find_game_img(config[svselect]['IMAGE_CHATSTICKER']):
                            detectAssistance = threading.Thread(target=self.detectAssistance())
                            detectAssistance.setDaemon(True)
                            detectAssistance.start
                        if _scrollcount > 2:
                            break
                        if self.__gui.find_game_img(config['REALM']['IMAGE_REALM_SECTION2_PATH']):
                            break 
                        if self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GUILDPAGEEND_TOP_PATH'],thread=0.96):
                            break
                        self.__gui.mouse_drag_bg(SCROLL_DOWN[1],SCROLL_DOWN[0]) #up
                        time.sleep(1)
                          
                else:
                    logging.debug("scroll down")
                    if _need1scrollup == True:
                        self.__gui.mouse_drag_bg(SCROLL_DOWN[1],SCROLL_DOWN[0]) #scroll up 1 time for check on top 
                        _need1scrollup = False
                        continue
                    time.sleep(1)
                    _scrollcount += 1
                    logging.debug("_scrollcount:%s"%_scrollcount)
                    while True:
                        if self.__gui.find_game_img(config[svselect]['IMAGE_COOP2_SEAL']) or (_displayChat == 0 and self.__gui.find_game_img(config[svselect]['IMAGE_CHATDETECT'])) or self.__gui.find_game_img(config[svselect]['IMAGE_CHATSTICKER']):
                            detectAssistance = threading.Thread(target=self.detectAssistance())
                            detectAssistance.setDaemon(True)
                            detectAssistance.start
                        if _scrollcount > 2:
                            break
                        if self.__gui.find_game_img(config['REALM']['IMAGE_REALM_SECTION2_PATH']):
                            break 
                        if self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GUILDPAGEEND_PATH']):
                            break 
                        time.sleep(1)
                        self.__gui.mouse_drag_bg(SCROLL_DOWN[0],SCROLL_DOWN[1]) #down
                        
                        
            
            #Click Realm
            guild=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GUILDSCROLL_PATH'])
            position=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_SECTION2_PATH'])
            positionGB=(self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GRAIDCOUNT'], part=1, pos1=(760, 500), pos2=(810, 525), thread=0.95) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GRAIDCOUNT'], part=1, pos1=(226, 492), pos2=(286, 529), thread=0.97))
            positionCN=(self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GRAIDCOUNT_CN'], part=1, pos1=(760, 500), pos2=(810, 525), thread=0.85) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GRAIDCOUNT_CN'], part=1, pos1=(226, 492), pos2=(286, 529), thread=0.85))
            position1= positionGB or positionCN
            position2=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE'])
            # Click icon realm
            
            if (position and guild) != False and position1 == False:
                self.__gui.mouse_click_bg(position)
                _cAttackRealm+=1
                _idlecount=0
                _scrollcount=0
                _need1scrollup=True
                time.sleep(0.5)
                atk=self.__gui.find_game_img(config[svselect]['IMAGE_REALM_ATK_PATH'])
                logging.info("Click Attack..")
                if atk != False and position2 != False:
                    logging.debug("Click Attack by atk image")
                    self.__gui.mouse_click_bg(atk)
                    time.sleep(1)
                    continue
                if atk == False and position2 != False:
                    logging.debug("Click Attack by SECTION2 image")
                    self.__gui.mouse_click_bg((_displayChat+position[0]-24,position[1]+148))    
                    # self.__gui.mouse_click_bg((_displayChat+position[0]-24,position[1]+190))    
                    #If Can't Attack Enemy 
                    position=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE'])
                    position2=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CANTATTK_PATH'],gray=0)
                    if position2 != False:
                        time.sleep(1)
                        logging.info("Reopen Guild Realm Raid")
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
                logging.info("Failed..")
                self.__gui.mouse_click_bg(position)
                time.sleep(1)
                _cAttackRealm=0
                _idlecount=0
                continue
                
           #check finish
            if (self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1_PATH']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1S3_PATH']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED2_PATH'])) != False:
                logging.info("Finishing...")
                #time.sleep(5)
                while True:
                    if self.__gui.find_game_img(config[svselect]['IMAGE_COOP2_SEAL']) or (_displayChat == 0 and self.__gui.find_game_img(config[svselect]['IMAGE_CHATDETECT'])) or self.__gui.find_game_img(config[svselect]['IMAGE_CHATSTICKER']):
                        detectAssistance = threading.Thread(target=self.detectAssistance())
                        detectAssistance.setDaemon(True)
                        detectAssistance.start

                    if (self.__gui.find_game_img(config['REALM']['IMAGE_REALM_SECTION2_PATH']) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE']) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_GUILDSCROLL_PATH'])) != False:
                        time.sleep(1)
                        _cAttackRealm=0
                        _idlecount=0
                        break
                    self.__gui.mouse_click_bg((_displayChat+CLICK_FINISH[0], CLICK_FINISH[1]))
                break

            elif position1 != False:
                # logging.info("Round: 0/6 | Sleep for Wait 5s")
                time.sleep(5)
                _idlecount+=5

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
            self.gameModeGuildRealmRaid()
            # self.test()
            count+=1
            message="completed %s, remaining %s round"%(str(count),str(self.__total-count))
            self.create_file(data=str(count))
            logging.info(message)


if __name__ == '__main__':
    load_config()