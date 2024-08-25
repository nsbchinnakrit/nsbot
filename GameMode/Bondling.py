from Module.GameControl import *
from Module.ThreadGame import *
from Module.Util import *
from Module.loadconfig import *
import time, subprocess

_localVariable=threading.local()
_displayChat=0
cantattk=0
pactst=False
_idlecount=0
_firstclick=False
_ispact=False

class Bondling(threading.Thread):
    def __init__(self,Server, windowName, beforetotal, total, pid, bondlingmode, pactsettings, crystal_use, tomb, snowball, azure, kuro):
        global svselect
        threading.Thread.__init__(self)
        self.__server=Server
        svselect=self.__server
        self.__hwnd=windowName
        self.__beforetotal=beforetotal
        self.__total=total
        self.__pid=pid
        self.__mode=bondlingmode
        self.__pact=pactsettings
        self.__crystal=crystal_use
        self.__tomb=tomb
        self.__snowball=snowball
        self.__azure=azure
        self.__kuro=kuro
        self.__gui=GameControl(self.__hwnd,0)


    def gameModeBondling(self):
        global cantattk, pactst, _idlecount, _firstclick, count, _ispact
        CLICK_SOULMAX=(568, 387)
        START_SOUL_COORDINATE=(1075, 565)
        while True:  
            detectAssistance = threading.Thread(target=self.detectAssistance())
            detectAssistance.setDaemon(True)
            detectAssistance.start
            time.sleep(1)

            position=self.__gui.find_game_img(config['BONDLING']['IMAGE_BONDLING_BONDLING'])
            if position != False:
                logging.info("Enter Bondling Fairyland")
                self.__gui.mouse_click_bg(position)
                _idlecount=0
                time.sleep(5)
                continue

            # position = self.__gui.find_game_img(config['BONDLING']['IMAGE_BONDLING_PACT'], gray=1, thread=0.70) or self.__gui.find_game_img(config['BONDLING']['IMAGE_BONDLING_PACT2'], gray=1, thread=0.70)
            # if position != False and (self.__mode == 'Pact' or self.__mode == 'Both') and (self.__gui.find_game_img(config['BONDLING']['IMAGE_BONDLING_EXPDETECT']) != False
            #     ):
            #     logging.info('Pact-forming Found!:%s'%position)
            #     self.__gui.mouse_click_bg(position)
            #     time.sleep(1)

            
            #Tomb
            position = self.__gui.find_game_img(config['BONDLING']['IMAGE_BONDLING_PACT1'], gray=0, thread=0.93)
            if (self.__mode == 'Pact' or self.__mode == 'Both') and ((self.__crystal == '1') or (self.__tomb == 'true')) and position != False:
                logging.info("Tomb Guard!")
                self.__gui.mouse_click_bg(position)
                _idlecount=0
                logging.debug("_firstclick = False")
                _firstclick = False
                time.sleep(2)

            #SnowBall
            position = self.__gui.find_game_img(config['BONDLING']['IMAGE_BONDLING_PACT2'], gray=0, thread=0.93)
            if (self.__mode == 'Pact' or self.__mode == 'Both') and ((self.__crystal == '2') or (self.__snowball == 'true')) and position != False:
                logging.info("Snowball!")
                self.__gui.mouse_click_bg(position)
                _idlecount=0
                logging.debug("_firstclick = False")
                _firstclick = False
                time.sleep(2)

            #Azure
            position = self.__gui.find_game_img(config['BONDLING']['IMAGE_BONDLING_PACT3'], gray=0, thread=0.93)
            if (self.__mode == 'Pact' or self.__mode == 'Both') and ((self.__crystal == '3') or (self.__azure == 'true')) and position != False:
                logging.info("Azure Basan!")
                self.__gui.mouse_click_bg(position)
                _idlecount=0
                logging.debug("_firstclick = False")
                _firstclick = False
                time.sleep(2)

            #Kuro
            position = self.__gui.find_game_img(config['BONDLING']['IMAGE_BONDLING_PACT4'], gray=0, thread=0.93)
            if (self.__mode == 'Pact' or self.__mode == 'Both') and ((self.__crystal == '4') or (self.__kuro == 'true')) and position != False:
                logging.info("Kuro!")
                self.__gui.mouse_click_bg(position)
                _idlecount=0
                logging.debug("_firstclick = False")
                _firstclick = False
                time.sleep(3)

            position = self.__gui.find_game_img(config['BONDLING']['IMAGE_BONDLING_SUMMON'], gray=0, thread=0.93)
            if (position != False) and (_firstclick == False):
                self.__gui.mouse_click_bg((_displayChat+50, 500))
                _firstclick = True
            
            
            position = self.__gui.find_game_img(config['BONDLING']['IMAGE_BONDLING_SUMMON'], gray=0, thread=0.90)
            if self.__mode == 'Pact' and self.__crystal != 'false':
                if (self.__gui.find_game_img(config['BONDLING']['IMAGE_BONDLING_PACT%s'%self.__crystal], gray=0, thread=0.90) == False) and (position != False):
                    logging.info("Summon Bondling!")
                    time.sleep(1)
                    self.__gui.mouse_click_bg(position)
                    _idlecount=0
                    time.sleep(2)
                    position = self.__gui.find_game_img(config['BONDLING']['IMAGE_BONDLING_TOMBFACE'])
                    if position != False:
                        logging.info("Select Bondling!")
                        if self.__crystal == '1':
                            logging.info("Tomb Guard Select!")
                            self.__gui.mouse_click_bg((_displayChat+896, 383))
                            time.sleep(1)
                            self.__gui.mouse_click_bg((_displayChat+1036, 566))
                            time.sleep(5)

                        if self.__crystal == '2':
                            logging.info("Snowball Select!")
                            self.__gui.mouse_click_bg((_displayChat+405, 383))
                            time.sleep(1)
                            self.__gui.mouse_click_bg((_displayChat+1036, 566))
                            time.sleep(5)

                        if self.__crystal == '3':
                            logging.info("Azure Basan Select!")
                            self.__gui.mouse_click_bg((_displayChat+639, 383))
                            time.sleep(1)
                            self.__gui.mouse_click_bg((_displayChat+1036, 566))
                            time.sleep(5)
                            
                        if self.__crystal == '4':
                            logging.info("Kuro Select!")
                            self.__gui.mouse_click_bg((_displayChat+190, 383))
                            time.sleep(1)
                            self.__gui.mouse_click_bg((_displayChat+1036, 566))
                            time.sleep(5)

            
            #Pact Settings
            position = self.__gui.find_game_img(config['BONDLING']['IMAGE_BONDLING_PACTSETTINGS'])
            if (self.__mode == 'Pact' or self.__mode == 'Both') and (position != False) and pactst == False:
                logging.info('Pact Settings')
                self.__gui.mouse_click_bg(position)
                _idlecount=0
                time.sleep(1)
                position2 = self.__gui.find_game_img(config[svselect]['IMAGE_REALM_CANCEL'])
                if position2 != False:
                    logging.info('Test')
                    self.__gui.mouse_click_bg((position2[0],position2[1]-327))
                    time.sleep(1)
                    if self.__pact == '1':
                        logging.info('select Basic Disc')
                        self.__gui.mouse_click_bg((position2[0],position2[1]-245))
                        time.sleep(1)
                        self.__gui.mouse_click_bg((position2[0]+180,position2[1]))
                        if position2 != False:
                            self.__gui.mouse_click_bg((position2[0]+180,position2[1]))
                            time.sleep(1)
                    if self.__pact == '2':
                        logging.info('select Great Disc')
                        self.__gui.mouse_click_bg((position2[0]+125,position2[1]-245))
                        time.sleep(1)
                        self.__gui.mouse_click_bg((position2[0]+180,position2[1]))
                        if position2 != False:
                            self.__gui.mouse_click_bg((position2[0]+180,position2[1]))
                            time.sleep(1)
                    if self.__pact == '3':
                        logging.info('select Ultra Disc')
                        self.__gui.mouse_click_bg((position2[0]+249,position2[1]-245))
                        time.sleep(1)
                        self.__gui.mouse_click_bg((position2[0]+180,position2[1]))
                        if position2 != False:
                            self.__gui.mouse_click_bg((position2[0]+180,position2[1]))
                            time.sleep(1)
                pactst = True
            
            #lock line up
            position=self.__gui.find_game_img(config['SOUL']['IMAGE_SINGLE_SOUL_LOCK_PATH'])
            position2=self.__gui.find_game_img(config['BONDLING']['IMAGE_BONDLING_SUMMON'])
            position3=self.__gui.find_game_img(config['BONDLING']['IMAGE_BONDLING_PACTSETTINGS'])
            if position != False and (position2 or position3):
                logging.info("Successfully lock lineup...")
                self.__gui.mouse_click_bg(position)
                _idlecount=0
                continue
            
            if (self.__mode == 'Pact' or self.__mode == 'Both') and (self.__gui.find_game_img(config['BONDLING']['IMAGE_BONDLING_INFO']) != False
                ) and (self.__gui.find_game_img(config['BONDLING']['IMAGE_BONDLING_PACTSETTINGS']) != False):
                logging.info('Pact-forming Start')
                cantattk+=1
                _idlecount=0
                _ispact=True
                self.__gui.mouse_click_bg((_displayChat + 1045, 545))
                time.sleep(1)

            if (self.__mode == 'Explore' or self.__mode == 'Both') and (self.__gui.find_game_img(config['BONDLING']['IMAGE_BONDLING_EXPDETECT']) != False
                ) and (self.__gui.find_game_img(config['BONDLING']['IMAGE_BONDLING_SUMMON']) != False):
                logging.info('Explore Start')
                cantattk+=1
                _idlecount=0
                self.__gui.mouse_click_bg((_displayChat + 1045, 545))
                time.sleep(3)

            if cantattk >= 5 or (self.__gui.find_game_img(config['DEFAULT']['IMAGE_EMPTY_SUSHI']) != False and self.__gui.find_game_img(config['DEFAULT']['IMAGE_EMPTY_SUSHI_CLOSE']) == False) or (self.__gui.find_game_img(config[svselect]['IMAGE_REALM_CANCEL']) != False) and (self.__gui.find_game_img(config['SOUL']['IMAGE_SOUL_INVITE_CHECKBOX_PATH'], thread=0.98) == False):
                logging.info("Unable to process, Exit!")
                total = str(self.__total)
                self.create_file(data=total)
                args = ['taskkill', '/F', '/PID', str(self.__pid)]
                subprocess.Popen(args)
                sys.exit()

            gameready=self.__gui.find_game_img(config[svselect]['IMAGE_READY_PATH'])
            if gameready != False:
                self.__gui.mouse_click_bg(gameready)
                _idlecount=0
                time.sleep(1)
                continue

            #Pact sucess
            position=self.__gui.find_game_img(config['BONDLING']['IMAGE_BONDLING_BRUSH'],thread=0.70, gray=1)
            position2=self.__gui.find_game_img(config['SOUL']['IMAGE_SINGLE_SOUL_STAT_PATH'])
            if position != False and position2 == False:
                logging.info("#Pact sucess")
                while True:
                    if (self.__gui.find_game_img(config['BONDLING']['IMAGE_BONDLING_SUMMON']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_EMPTY_SUSHI']) or self.__gui.find_game_img(config['BONDLING']['IMAGE_BONDLING_PACTSETTINGS'])) != False:
                        logging.info("Pact Round End...")
                        # count+=1
                        _idlecount=0
                        break
                    self.__gui.mouse_click_bg((position[0], position[1]+120))
                break

            #Fail
            position=self.__gui.find_game_img(config['DEFAULT']['IMAGE_FAILED_PATH'])
            if position != False:
                cantattk=0
                _idlecount=0
                logging.info("Failed..")
                self.__gui.mouse_click_bg(position)
                while True:
                    if self.__gui.find_game_img(config[svselect]['IMAGE_COOP2_SEAL']) or (_displayChat == 0 and self.__gui.find_game_img(config[svselect]['IMAGE_CHATDETECT'])) or self.__gui.find_game_img(config[svselect]['IMAGE_CHATSTICKER']):
                        detectAssistance = threading.Thread(target=self.detectAssistance())
                        detectAssistance.setDaemon(True)
                        detectAssistance.start
                        
                    if self.__gui.find_game_img(config['DEFAULT']['IMAGE_FAILED_PATH']) == False:
                        break
                    self.__gui.mouse_click_bg((_displayChat+CLICK_SOULMAX[0], CLICK_SOULMAX[1]))

             #check finish
            if (self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED0_PATH']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1_PATH']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED2_PATH'])) != False:
                logging.info("Finishing...")
                cantattk=0
                _idlecount=0
                while True:
                    if self.__gui.find_game_img(config[svselect]['IMAGE_COOP2_SEAL']) or (_displayChat == 0 and self.__gui.find_game_img(config[svselect]['IMAGE_CHATDETECT'])) or self.__gui.find_game_img(config[svselect]['IMAGE_CHATSTICKER']):
                        detectAssistance = threading.Thread(target=self.detectAssistance())
                        detectAssistance.setDaemon(True)
                        detectAssistance.start

                    if (self.__gui.find_game_img(config['BONDLING']['IMAGE_BONDLING_SUMMON']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_EMPTY_SUSHI']) or self.__gui.find_game_img(config['BONDLING']['IMAGE_BONDLING_PACTSETTINGS'])) != False:
                        logging.info("Round End...")
                        if ((self.__mode == 'Both') or (self.__mode == 'Pact')):
                            count-=1
                            break
                        break

                    #soulmax
                    if (self.__gui.find_game_img(config[svselect]['IMAGE_SOULMAX'])) != False:
                        self.__gui.mouse_click_bg((_displayChat+CLICK_SOULMAX[0], CLICK_SOULMAX[1]))
                        time.sleep(1)
                        continue
                    self.__gui.mouse_click_bg((_displayChat+CLICK_SOULMAX[0], CLICK_SOULMAX[1]))
                break

            #soulmax
            if self.__gui.find_game_img(config[svselect]['IMAGE_SOULMAX']) != False:
                self.__gui.mouse_click_bg((_displayChat+CLICK_SOULMAX[0], CLICK_SOULMAX[1]))
                _idlecount=0
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
        global count
        count=self.__beforetotal
        self.create_file(data=str(count))
        while self.__total-count>0:
            seconds=0
            while seconds:
                time.sleep(1)
                seconds-=1
            logging.info("\n\n==================Starting a new round==================")
            self.gameModeBondling()
            count+=1
            message="completed %s, remaining %s round"%(str(count),str(self.__total-count))
            self.create_file(data=str(count))
            logging.info(message)


if __name__ == '__main__':
    load_config()
