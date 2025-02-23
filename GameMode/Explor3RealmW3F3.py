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
_exit = True
cantattk=0
_setround=0
_firstcheck=True
_isFail=0
_idlecount=0

CLICK_SOULMAX=(568, 387)
CLICK_FINISH2=(35, 510)
SLIDE_STORY_COORDINATE=[(_displayChat+200,200),(_displayChat+1000,200)]
START_SOUL_COORDINATE = (1075, 565)

class Explor3RealmW3F3(threading.Thread):
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
                
    def gameModeExplore_3Realm(self):
        global _cAttackRealm, _setround, _firstcheck, _idlecount, _isFail
        while True: 
            logging.debug("Working in [gameModeExplore_3Realm]")
            detectAssistance = threading.Thread(target=self.detectAssistance())
            detectAssistance.setDaemon(True)
            detectAssistance.start

            if self.__gui.find_game_img(config[svselect]['IMAGE_REALM_CANCEL_BATTLE'], thread=0.70):
                logging.info("Exit Battle..")
                time.sleep(0.4)
                self.__gui.mouse_click_bg((_displayChat+655, 383))
                _exit = True
                
            position=(self.__gui.find_game_img(config['REALM']['IMAGE_REALM_EMPTY_TICKET2'], thread=0.90) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_EMPTY_TICKET2CN'], thread=0.90))
            position2=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_LIST_CHAPTER_PATH'])  
            position3=self.__gui.find_game_img(config[svselect]['IMAGE_REALM_GUILD_PATH'])
            position4=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE'])
            position5=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_BOX_PATH'])
            #time.sleep(5)
            if position5 != False:
                logging.info("Box Found. (Func.1)")
                self.__gui.mouse_click_bg(position5)
                _idlecount=0
                time.sleep(1)
                if position4 != False:
                    self.__gui.mouse_click_bg(position4)
                    time.sleep(1)
                    self.__gui.mouse_click_bg(position5)
                    time.sleep(1)
                    continue
                
            position4=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE'])
            if position != False or position3 != False:
                logging.info("Change to Realm Raid")
                while True:
                    time.sleep(1)
                    if self.__gui.find_game_img(config[svselect]['IMAGE_COOP2_SEAL']) or (_displayChat == 0 and self.__gui.find_game_img(config[svselect]['IMAGE_CHATDETECT'])) or self.__gui.find_game_img(config[svselect]['IMAGE_CHATSTICKER']):
                        detectAssistance = threading.Thread(target=self.detectAssistance())
                        detectAssistance.setDaemon(True)
                        detectAssistance.start

                    if self.__gui.find_game_img(config[svselect]['IMAGE_REALM_EMPTY_TICKET'],thread=0.97) !=False:
                        logging.info("Close RealmPage...")
                        self.__gui.mouse_click_bg((_displayChat+1070, 120))
                        if _firstcheck == False:
                            _setround+=1
                            _idlecount=0
                            self.create_file(data=str(_setround))
                            _firstcheck = True
                        time.sleep(1)
                        break
                        #sys.exit()
                    if position4 != False and position3 == False:
                        self.__gui.mouse_click_bg(position4)
                        logging.info('Close Explore Page.')
                        #Click icon realm
                        time.sleep(1)
                        self.gameModeRealmRaid()
                        break
                    else:
                        self.gameModeRealmRaid()

            if position == False and position2 != False or self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_CHERRY_CAKE_PATH']) != False or self.__gui.find_game_img(config[svselect]['IMAGE_STORY_START_PATH']) != False:
                self.gameModeExplor()
            
            #Fail
            position=self.__gui.find_game_img(config['DEFAULT']['IMAGE_FAILED_PATH'])
            if position != False:
                logging.info("Failed..")
                cantattk=0
                _cAttackRealm=0
                _idlecount=0
                self.__gui.mouse_click_bg(position)
                continue

            #check finish
            if (self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1_PATH']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1S2_PATH']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1S3_PATH']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED2_PATH'])) != False:
                logging.info("Finishing...")
                cantattk=0
                _idlecount=0
                while True:
                    self.__gui.mouse_click_bg((_displayChat+CLICK_FINISH2[0], CLICK_FINISH2[1]))
                    if self.__gui.find_game_img(config[svselect]['IMAGE_COOP2_SEAL']) or (_displayChat == 0 and self.__gui.find_game_img(config[svselect]['IMAGE_CHATDETECT'])) or self.__gui.find_game_img(config[svselect]['IMAGE_CHATSTICKER']):
                        detectAssistance = threading.Thread(target=self.detectAssistance())
                        detectAssistance.setDaemon(True)
                        detectAssistance.start
                    if (self.__gui.find_game_img(config['SOUL']['IMAGE_SOUL_ROOM_DETECT_PATH']
                        ) or self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_BACK_PATH']
                        ) or self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_CHERRY_CAKE_PATH'])) != False or (
                        self.__gui.find_game_img(config[svselect]['IMAGE_BUFF'])) != False:
                        break
                    if self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE']) != False or self.__gui.find_game_img(
                        config['REALM']['IMAGE_REALM_JADE_PATH']) != False or self.__gui.find_game_img(config['DEFAULT']['IMAGE_EMPTY_SUSHI']) != False:
                        _cAttackRealm=0
                        break
                break

            #soulmax
            if self.__gui.find_game_img(config[svselect]['IMAGE_SOULMAX']) != False:
                logging.info("Soul Max")
                self.__gui.mouse_click_bg((_displayChat+CLICK_SOULMAX[0], CLICK_SOULMAX[1]))
                time.sleep(1)
                continue

            else:
                _idlecount+=1
    
    def gameModeExplor(self):
        global _displayChat, _cAutoRotation, cantattk, _setround, _firstcheck, _idlecount, _isFail
        while True:
            logging.debug("Working in [gameModeExplor]")
            detectAssistance = threading.Thread(target=self.detectAssistance())
            detectAssistance.setDaemon(True)
            detectAssistance.start

            position=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_BOX_PATH'])
            position2=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE'])
            position3=self.__gui.find_game_img(config[svselect]['IMAGE_REALM_GUILD_PATH'])    

            if position != False:
                logging.info("Box Found. (Func.2)")
                self.__gui.mouse_click_bg(position)
                time.sleep(4)
                if position != False and position2 != False:
                    self.__gui.mouse_click_bg(position2)
                    time.sleep(1)
                self.__gui.mouse_click_bg(position)
                time.sleep(1)

            if cantattk >= 12 or (self.__gui.find_game_img(config['DEFAULT']['IMAGE_EMPTY_SUSHI']) != False and self.__gui.find_game_img(config['DEFAULT']['IMAGE_EMPTY_SUSHI_CLOSE']) == False) and (self.__gui.find_game_img(config['SOUL']['IMAGE_SOUL_INVITE_CHECKBOX_PATH'], thread=0.98) == False):
                logging.info("Unable to process, Exit!")
                total = str(self.__total)
                self.create_file(data=total)
                args = ['taskkill', '/F', '/PID', str(self.__pid)]
                subprocess.Popen(args)
                sys.exit()
            
            if position2 != False and position3 != False:
                logging.debug("Return to Main function")
                self.gameModeExplore_3Realm()
                
            position=self.__gui.find_game_img(config[svselect]['IMAGE_STORY_AUTOFOOD_PATH'])
            if position != False:
                logging.info("Click Auto Rotation")
                self.__gui.mouse_click_bg((_displayChat+117, 599))
                _cAutoRotation+=1
                if _cAutoRotation >= 3:
                    logging.info("Exit!")
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
                    _idlecount=0
                    self.create_file(data=str(_setround))
                    _firstcheck = True
                    self.gameModeExplore_3Realm() 
                elif position != False:
                    _localVariable.isBossDetected=False
                    logging.info("Entering last chapter..")
                    self.__gui.mouse_click_bg((position[0],position[1]+370))
                    _idlecount=0
                    time.sleep(1)
                    continue
                
            position=self.__gui.find_game_img(config[svselect]['IMAGE_STORY_START_PATH'])
            position2=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_BOX_PATH'])
            position3=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE'])
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
                            if self.__gui.find_game_img(config[svselect]['IMAGE_COOP2_SEAL']) or (_displayChat == 0 and self.__gui.find_game_img(config[svselect]['IMAGE_CHATDETECT'])) or self.__gui.find_game_img(config[svselect]['IMAGE_CHATSTICKER']):
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
                    cantattk+=1
                    _firstcheck = False
                    _idlecount=0
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
                logging.info("BOSS was detected: ")
                self.__gui.mouse_click_bg(position)
                _localVariable.isBossDetected=True
                _firstcheck = False
                cantattk+=1
                _idlecount=0
                time.sleep(1)
                continue

            position=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_FIGHT_PATH'])
            if position != False:
                logging.info("Monster was detected... ")
                self.__gui.mouse_click_bg(position)
                cantattk+=1
                _idlecount=0
                time.sleep(1)
                continue

            #=========================================get ready=================================================
            position=self.__gui.find_game_img(config[svselect]['IMAGE_READY_PATH']) or self.__gui.find_game_img(config[svselect]['IMAGE_READY_PATH'])
            if position != False:
                logging.info("Starting battle.... ")
                self.__gui.mouse_click_bg(position)
                #time.sleep(2)
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
            if (self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1_PATH']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1S2_PATH'])) != False:
                logging.info("Finishing...")
                cantattk=0
                _idlecount=0
                while True:
                    self.__gui.mouse_click_bg((_displayChat+CLICK_FINISH2[0], CLICK_FINISH2[1]))
                    if self.__gui.find_game_img(config[svselect]['IMAGE_COOP2_SEAL']) or (_displayChat == 0 and self.__gui.find_game_img(config[svselect]['IMAGE_CHATDETECT'])) or self.__gui.find_game_img(config[svselect]['IMAGE_CHATSTICKER']):
                        detectAssistance = threading.Thread(target=self.detectAssistance())
                        detectAssistance.setDaemon(True)
                        detectAssistance.start

                    if (self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_CHERRY_CAKE_PATH']) != False or 
                        self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_LIST_CHAPTER_PATH']) != False or 
                        self.__gui.find_game_img(config['DEFAULT']['IMAGE_BUFF']) != False or 
                        self.__gui.find_game_img(config['DEFAULT']['IMAGE_EMPTY_SUSHI']) != False):
                        time.sleep(1)
                        break
                    #soulmax
                    if self.__gui.find_game_img(config[svselect]['IMAGE_SOULMAX']) != False:
                        logging.info("Soul Max")
                        self.__gui.mouse_click_bg((_displayChat+CLICK_SOULMAX[0], CLICK_SOULMAX[1]))
                        time.sleep(1)
                        continue
                break

            #==========================================Reward settlement=============================================
            position=self.__gui.find_game_img(config['EXPLORE']['IMAGE_STORY_GET_REWARD_PATH'])
            if position != False:
                logging.info("Get treasure.... ")
                self.__gui.send_esc_down()
                time.sleep(2)
                self.__gui.mouse_click_bg((_displayChat+655, 383))
                _idlecount=0
                
            #soulmax
            if self.__gui.find_game_img(config[svselect]['IMAGE_SOULMAX']) != False:
                logging.info("Soul Max")
                self.__gui.mouse_click_bg((_displayChat+CLICK_SOULMAX[0], CLICK_SOULMAX[1]))
                time.sleep(1)
                continue

            else:
                _idlecount+=1
    
    def gameModeRealmRaid(self):
        global _cAttackRealm, _displayChat, _is3Realm, _setround, _firstcheck, _idlecount, _isFail
        while True:
            logging.debug("Working in [gameModeRealmRaid]")
            detectAssistance = threading.Thread(target=self.detectAssistance())
            detectAssistance.setDaemon(True)
            detectAssistance.start
            #If Found Daruma
            position=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_FN3R_PATH'])
            position2=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE'])
            if position and position2:
                logging.info('3 Realm Raid Reward')
                time.sleep(2)
                self.__gui.mouse_click_bg((_displayChat+CLICK_FINISH2[0], CLICK_FINISH2[1]))
                time.sleep(2)
                _is3Realm = True
                _idlecount=0
            
            if self.__gui.find_game_img(config[svselect]['IMAGE_REALM_CANCEL_BATTLE'], thread=0.70):
                logging.info("Exit Battle..")
                time.sleep(0.4)
                self.__gui.mouse_click_bg((_displayChat+655, 383))
                _exit = True

            #not enough ticket
            # if self.__gameMode == 6:
            position = (self.__gui.find_game_img(config['GB']['IMAGE_REALM_EMPTY_TICKET'], part=1, pos1=(1005, 10), pos2=(1105, 45), thread=0.88) or self.__gui.find_game_img(config['GB']['IMAGE_REALM_EMPTY_TICKET'], part=1, pos1=(1530, 10), pos2=(1630, 45), thread=0.97))
            positionCN = (self.__gui.find_game_img(config['CN']['IMAGE_REALM_EMPTY_TICKET'], part=1, pos1=(1005, 10), pos2=(1105, 45), thread=0.88) or self.__gui.find_game_img(config['CN']['IMAGE_REALM_EMPTY_TICKET'], part=1, pos1=(1530, 10), pos2=(1630, 45), thread=0.91))
            if  position or positionCN:
                time.sleep(1)
                logging.info("Game Mode Story")
                self.__gui.mouse_click_bg((_displayChat+1063, 116))
                time.sleep(2)
                if _firstcheck == False:
                    _setround+=1
                    self.create_file(data=str(_setround))
                    _firstcheck = True
                    _idlecount=0
                self.gameModeExplore_3Realm()

            #Click icon realm
            position=self.__gui.find_game_img(config[svselect]['IMAGE_REALM_RAID_PATH'])
            if position != False:
                logging.info("Click icon realm raid...")
                self.__gui.mouse_click_bg(position)
                _idlecount=0
                time.sleep(3)
                continue
            
            #lock line up
            position=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_LOCK_PATH'])
            if position != False:
                logging.info("Successfully lock lineup...")
                self.__gui.mouse_click_bg(position)
                continue
            
            if _is3Realm == False:
                position=(self.__gui.find_game_img(config['REALM']['IMAGE_REALM_3RAID_PATH']) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_3RAID2_PATH']) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_3RAIDFROG_PATH']))
                if position == False:
                    # logging.info('Not Found 3Realm raid icon')
                    # _is3Realm = False
                    pass
                else:
                    logging.debug('set 3Realm raid state = True')
                    _is3Realm = True

            #Click Realm
            position=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_SECTIONFROG_PATH'], thread=0.91)
            position2=(self.__gui.find_game_img(config['REALM']['IMAGE_REALM_SECTION_PATH']) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_SECTION2_PATH']))
            positionatk=(position or position2)
            position3=self.__gui.find_game_img(config[svselect]['IMAGE_REALM_ATK_PATH'])
            position4=self.__gui.find_game_img(config[svselect]['IMAGE_REALM_REFRESH_PATH'], thread=0.96)
            position5=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE'])
            #This to Refresh#=========================================================================================================
            if _is3Realm != False and _isFail >= 3 and position4 != False:
                logging.debug('This should refresh')
                self.__gui.mouse_click_bg(position4)
                time.sleep(1)
                #This to Click OK button
                if self.__gui.find_game_img(config[svselect]['IMAGE_REALM_CANCEL']) != False:
                    self.__gui.mouse_click_bg((position4[0]-253,position4[1]-145))
                    logging.debug('set 3Realm raid state = False')
                    _is3Realm = False
                    _isFail = 0
                    _idlecount=0
                    time.sleep(1)
            
            if _is3Realm != False and (_isFail < 3) and position5 != False:
                time.sleep(1)
                if positionatk != False and _is3Realm != False:
                        self.__gui.mouse_click_bg(positionatk)
                        logging.info("Click Enemy Section..")
                        _cAttackRealm+=1
                        _idlecount=0
                        _exit = False
                        time.sleep(1)
                        position3=self.__gui.find_game_img(config[svselect]['IMAGE_REALM_ATK_PATH'])
                        if position3:
                            logging.debug('Click Attack Button')
                            self.__gui.mouse_click_bg(position3)
                        else:
                            self.__gui.mouse_click_bg((positionatk[0]-77,positionatk[1]+167))
                        time.sleep(2)
                        _idlecount=0
                        while True:
                            _idlecount+=1
                            if self.__gui.find_game_img(config[svselect]['IMAGE_COOP2_SEAL']) or (_displayChat == 0 and self.__gui.find_game_img(config[svselect]['IMAGE_CHATDETECT'])) or self.__gui.find_game_img(config[svselect]['IMAGE_CHATSTICKER']):
                                detectAssistance = threading.Thread(target=self.detectAssistance())
                                detectAssistance.setDaemon(True)
                                detectAssistance.start

                            if (self.__gui.find_game_img(config['DEFAULT']['IMAGE_BACK'], gray=1) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_BACK2'], gray=1, thread=0.78)) != False:
                                self.__gui.send_esc_down()
                                time.sleep(0.4)
                                self.__gui.mouse_click_bg((_displayChat+655, 383))
                                self.__gui.mouse_click_bg((_displayChat+655, 383))
                                _exit = True
                                break

                            if _idlecount>=80:
                                logging.debug('Test')
                                self.__gui.mouse_click_bg((_displayChat+1071, 117))
                                break
            
            #This Click Enemy#=========================================================================================================
            if _is3Realm == False and position5 != False:
                time.sleep(1)
                if _is3Realm == False and position5 != False:
                    if positionatk != False and _is3Realm == False:
                        logging.info("Click Enemy Section..")
                        self.__gui.mouse_click_bg(positionatk)
                        time.sleep(2)
                        _cAttackRealm+=1
                        _firstcheck = False
                        _idlecount=0
                        position3=self.__gui.find_game_img(config[svselect]['IMAGE_REALM_ATK_PATH'])
                        time.sleep(0.5)
                        if position3:
                            logging.debug('Click Attack Button')
                            self.__gui.mouse_click_bg(position3)
                        else:
                            position=self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE'])
                            time.sleep(0.5)
                            if position:
                                logging.debug('Click Close')
                                self.__gui.mouse_click_bg(position)
                            else:
                                logging.debug('Click Close with pos')
                                self.__gui.mouse_click_bg((_displayChat+1071, 117))
                            time.sleep(1)
                        self.gameModeRealmRaid()
                #else====================================================================================================
            if positionatk == False and position4 != False:
                logging.debug('This is "Enemy Cant Attalck"')
                time.sleep(1)
                self.__gui.mouse_click_bg(position4)
                time.sleep(1)
                #This to Click OK button
                if self.__gui.find_game_img(config[svselect]['IMAGE_REALM_CANCEL']) != False:
                    self.__gui.mouse_click_bg((position4[0]-253,position4[1]-145))
                    logging.debug('set 3Realm raid state = False')
                    _is3Realm = False
                    _idlecount=0
                    time.sleep(1)
            
            #=========================================get ready=================================================
            position=self.__gui.find_game_img(config[svselect]['IMAGE_READY_PATH'])
            if position != False:
                # logging.info("Starting battle.... ")
                self.__gui.mouse_click_bg(position)
                time.sleep(2)
                continue

            if self.__gui.find_game_img(config[svselect]['IMAGE_REALM_CANCEL_BATTLE'], thread=0.70):
                logging.info("Exit Battle..")
                time.sleep(0.4)
                self.__gui.mouse_click_bg((_displayChat+655, 383))
                _exit = True

            #Fail
            position=self.__gui.find_game_img(config['DEFAULT']['IMAGE_FAILED_PATH'])
            if position != False:
                logging.info("Failed..")
                _cAttackRealm=0
                _idlecount=0
                _isFail+=1
                while True:
                    if self.__gui.find_game_img(config[svselect]['IMAGE_COOP2_SEAL']) or (_displayChat == 0 and self.__gui.find_game_img(config[svselect]['IMAGE_CHATDETECT'])) or self.__gui.find_game_img(config[svselect]['IMAGE_CHATSTICKER']):
                        detectAssistance = threading.Thread(target=self.detectAssistance())
                        detectAssistance.setDaemon(True)
                        detectAssistance.start

                    if (self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE']) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_JADE_PATH'])) != False:
                        _cAttackRealm=0
                        break
                    self.__gui.mouse_click_bg((_displayChat+CLICK_FINISH2[0], CLICK_FINISH2[1]))

            #check finish
            if (self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1_PATH']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1S3_PATH']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED2_PATH'])) != False:
                logging.info("Finishing...")
                #time.sleep(5)
                while True:
                    if self.__gui.find_game_img(config[svselect]['IMAGE_COOP2_SEAL']) or (_displayChat == 0 and self.__gui.find_game_img(config[svselect]['IMAGE_CHATDETECT'])) or self.__gui.find_game_img(config[svselect]['IMAGE_CHATSTICKER']):
                        detectAssistance = threading.Thread(target=self.detectAssistance())
                        detectAssistance.setDaemon(True)
                        detectAssistance.start

                    if (self.__gui.find_game_img(config['REALM']['IMAGE_REALM_CLOSE']) or self.__gui.find_game_img(config['REALM']['IMAGE_REALM_JADE_PATH'])) != False:
                        _cAttackRealm=0
                        _idlecount=0
                        break
                    self.__gui.mouse_click_bg((_displayChat+CLICK_FINISH2[0], CLICK_FINISH2[1]))
                break

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
        self.create_file(data=str(_setroundcount))
        _localVariable.detectCount=30
        while self.__total-count>0:
            seconds=0
            while seconds:
                time.sleep(1)
                seconds-=1
            logging.info("\n\n==================Starting a new round==================")
            self.gameModeExplore_3Realm()
            count+=1
            message="completed %s, remaining %s round"%(str(count),str(self.__total-count))
            # self.create_file(data=str(count))
            logging.info(message)


if __name__ == '__main__':
    load_config()