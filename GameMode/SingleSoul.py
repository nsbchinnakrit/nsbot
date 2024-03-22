from Module.GameControl import *
from Module.ThreadGame import *
from Module.Util import *
from Module.loadconfig import *
import time, subprocess

_localVariable=threading.local()
_displayChat=0
cantattk=0

class SingleSoul(threading.Thread):
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


    def gameModeSingleSoul(self):
        global cantattk
        CLICK_FINISH = (_displayChat+567, 388)
        START_SOUL_COORDINATE=(_displayChat+1075, 565)
        while True:  
            detectAssistance = threading.Thread(target=self.detectAssistance())
            detectAssistance.setDaemon(True)
            detectAssistance.start

            #lock line up
            position=self.__gui.find_game_img(config['SOUL']['IMAGE_SINGLE_SOUL_LOCK_PATH'])
            if position != False:
                printWithTime("Successfully lock lineup...")
                self.__gui.mouse_click_bg(position)
                continue
            
            positions = self.__gui.find_game_img(config['SOUL']['IMAGE_SINGLE_SOUL_STAT_PATH'])
            if positions:
                printWithTime("Start... ")
                cantattk+=1
                self.__gui.mouse_click_bg(positions)
                time.sleep(1)
                continue

            if cantattk >= 12:
                printWithTime("Unable to process, please check.")
                total = str(self.__total)
                self.create_file(data=total)
                args = ['taskkill', '/F', '/PID', str(self.__pid)]
                subprocess.Popen(args)
                sys.exit()

            gameready=self.__gui.find_game_img(config[svselect]['IMAGE_READY_PATH'])
            if gameready != False:
                self.__gui.mouse_click_bg(gameready)
                time.sleep(1)
                continue

             #check finish
            if (self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED0_PATH']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1_PATH']) or self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED1S2_PATH'])) != False:
                printWithTime("Finishing...")
                cantattk=0
                while True:
                    # if self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED2_PATH']) != False or self.__gui.find_game_img(IMAGE_SOUL_ROOM_DETECT_PATH) != False:
                    if self.__gui.find_game_img(config['SOUL']['IMAGE_SINGLE_SOUL_STAT_PATH']) != False:
                        break

                    #soulmax
                    if self.__gui.find_game_img(config[svselect]['IMAGE_SOULMAX']) != False:
                        printWithTime("Clame Pet Reward.")
                        self.__gui.mouse_click_bg(CLICK_FINISH)
                        time.sleep(1)
                        continue

                    self.__gui.mouse_click_bg(START_SOUL_COORDINATE)
                break
            
            if self.__gui.find_game_img(config['DEFAULT']['IMAGE_FINISHED2_PATH']) != False:
                printWithTime("Getting reward...")
                while True:
                    if self.__gui.find_game_img(config['SOUL']['IMAGE_SINGLE_SOUL_STAT_PATH']) != False:
                        break
                    self.__gui.mouse_click_bg(CLICK_FINISH)
                break

            #Fail
            position=self.__gui.find_game_img(config['DEFAULT']['IMAGE_FAILED_PATH'])
            if position != False:
                cantattk=0
                printWithTime("Failed..")
                self.__gui.mouse_click_bg(position)
                while True:
                    if self.__gui.find_game_img(config['DEFAULT']['IMAGE_FAILED_PATH']) == False:
                        break
                    self.__gui.mouse_click_bg(CLICK_FINISH)
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
        while self.__total-count>0:
            seconds=0
            while seconds:
                time.sleep(1)
                seconds-=1
            print("\n\n==================Starting a new round==================")
            self.gameModeSingleSoul()
            count+=1
            message="GameMode:Soul (Single), completed %s, remaining %s round"%(str(count),str(self.__total-count))
            self.create_file(data=str(count))
            printWithTime(message)


if __name__ == '__main__':
    load_config()
