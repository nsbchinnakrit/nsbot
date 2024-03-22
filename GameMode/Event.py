from Module.GameControl import *
from Module.ThreadGame import *
from Module.Util import *
from Module.loadconfig import *
import time, subprocess

_localVariable=threading.local()
_displayChat=0
cantattk=0

class Event(threading.Thread):
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
#   
    def gameModeEvent(self):
        global _displayChat, cantattk
        while True:
            detectAssistance = threading.Thread(target=self.detectAssistance())
            detectAssistance.setDaemon(True)
            detectAssistance.start
            
            position = (self.__gui.find_game_img(
                config['EVENT']['IMAGE_EVENT_TARGET'], thread=0.87) or self.__gui.find_game_img(config['EVENT']['IMAGE_EVENT_TARGET'], thread=0.80))
            position2 = self.__gui.find_game_img(config['EVENT']['IMAGE_EVENT_ATT'])
            if position != False and position2 == False:
                self.__gui.mouse_click_bg(position)
                time.sleep(10)
                
            position2 = self.__gui.find_game_img(config['EVENT']['IMAGE_EVENT_ATT'])
            if position2 != False:
                self.__gui.mouse_click_bg(position2)

            position = self.__gui.find_game_img(config['EVENT']['IMAGE_EVENT_LOCK'])
            if position != False:
                self.__gui.mouse_click_bg(position)
                time.sleep(1)
                continue
            position = (self.__gui.find_game_img(config['EVENT']['IMAGE_EVENT_START'], thread= 0.95) or self.__gui.find_game_img(config['EVENT']['IMAGE_EVENT_START2'], thread= 0.95))
            if position != False:
                time.sleep(0.5)
                printWithTime('Start')
                cantattk+=1
                self.__gui.mouse_click_bg(position)
                time.sleep(1)
                continue

            if cantattk >= 12:
                printWithTime("Unable to process, please check.")
                total = str(self.__total)
                self.create_file(data=total)
                args = ['taskkill', '/F', '/PID', str(self.__pid)]
                subprocess.Popen(args)
                sys.exit()

            #=========================================get ready=================================================
            position=self.__gui.find_game_img(config[svselect]['IMAGE_READY_PATH'],thread=0.8)
            if position != False:
                self.__gui.mouse_click_bg(position)
                time.sleep(2)
                continue
            
            position=self.__gui.find_game_img(config['DEFAULT']['IMAGE_FAILED_PATH'])
            if position != False:
                cantattk=0
                printWithTime("Failed..")
                self.__gui.mouse_click_bg(position)
                continue
                
            #check finish
            if self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1_PATH']) != False or self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED2_PATH']) != False:
                printWithTime("Finishing...")
                cantattk=0
                while True:
                    if (self.__gui.find_game_img(config['EVENT']['IMAGE_EVENT_END']) or self.__gui.find_game_img(config['EVENT']['IMAGE_EVENT_END2'])) != False:
                        break
                    self.__gui.mouse_click_bg((_displayChat+694, 113))
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

    # def test_1(self):
    #     time.sleep(1)
    #     if self.__gui.find_game_img(config['DEFAULT']['IMAGE_BACK'], gray=1) != False:
    #         print("1")
    #         self.__gui.send_esc_down()
    #         time.sleep(0.8)
    #         self.__gui.mouse_click_bg((_displayChat+655, 383))
    #     if self.__gui.find_game_img(config['DEFAULT']['IMAGE_BACK2'], gray=1, thread=0.87) != False:
    #         print("2")
    #         self.__gui.send_esc_down()
    #         time.sleep(0.8)
    #         self.__gui.mouse_click_bg((_displayChat+655, 383))

    def run(self):
        count=0
        _localVariable.detectCount=10
        while self.__total-count>0:
            seconds=0
            while seconds:
                time.sleep(1)
                seconds-=1
            print("\n\n==================Starting a new round==================")
            # self.test_1()
            self.gameModeEvent()
            count+=1
            message="GameMode:Event, completed %s, remaining %s round"%(str(count),str(self.__total-count))
            self.create_file(data=str(count))
            printWithTime(message)


if __name__ == '__main__':
    load_config()
