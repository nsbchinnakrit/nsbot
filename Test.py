from Module.GameControl import *
from Module.ThreadGame import *


from Module.loadconfig import *
from Module.logsystem import MyLog
import time, subprocess
import logging

windowName = ('阴阳师-网易游戏')
# windowName = ('Onmyoji')
hwnd = win32gui.FindWindow(None, windowName)
total=999
accounts=[]

_localVariable=threading.local()
_displayChat=0
cantattk=0
_idlecount=0
svselect='GB'

class Test(threading.Thread):
    def __init__(self, windowName, total):
        global svselect
        threading.Thread.__init__(self)
        self.__hwnd=windowName
        self.__total=total
        self.__gui=GameControl(self.__hwnd,0)
#   
    def gameModeTest(self):
        while True:
            time.sleep(1)
            self.__gui.find_game_img(self.__gui.templates['IMAGE_WQ_JADE'], threshold=0.8)
            # self.__gui.find_game_img(self.__gui.templates['IMAGE_MAIL'], threshold=0.96)

            # self.__gui.find_game_img(self.__gui.templates['IMAGE_REALM_3RAIDFROG'])
            # self.__gui.find_game_img(self.__gui.templates['IMAGE_EVENT_START'])
            # self.__gui.find_game_img(self.__gui.templates['IMAGE_EVENT_START2'])
            # self.__gui.find_game_img(self.__gui.templates['IMAGE_SOUL_START'])
            # self.__gui.find_game_img(self.__gui.templates['IMAGE_SINGLE_SOUL_START'])

        

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
            self.gameModeTest()
            count+=1
            message="completed %s, remaining %s round"%(str(count),str(self.__total-count))
            print(message)


def main():
    # load_config()
    MyLog.init()
    print (hwnd)
    print('Start Bot')
    accounts.append(Test(hwnd, total))
    account=threading.Thread(accounts[0].run())

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
    # handle the exception
        print("An exception occurred:", error)
        time.sleep(10)