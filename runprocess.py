from GameMode.Soul import *
from GameMode.SingleSoul import *
from GameMode.Explore import *
from GameMode.SingleExplore import *
from GameMode.RealmRaid import *
from GameMode.RealmRaidW3F3 import *
from GameMode.GuildRealmRaid import *
from GameMode.Explor3Realm import *
from GameMode.Explor3RealmW3F3 import *
from GameMode.Event import *
from GameMode.Bondling import *
import logging
from Module.logsystem import MyLog
import sys

accounts=[]
Server=[]
pid = os.getpid()

getgameMode=sys.argv[1]
Server = sys.argv[2]
windowName = sys.argv[3]
beforetotal = int(sys.argv[4])
total = int(sys.argv[5])
bondlingmode = sys.argv[6]
pactsettings = sys.argv[7]
crystal_use = sys.argv[8]
tomb = sys.argv[9]
snowball = sys.argv[10]
azure = sys.argv[11]
kuro = sys.argv[12]

if getgameMode == 'SingleSoul':
    gameMode = SingleSoul
if getgameMode == 'Soul':
    gameMode = Soul
if getgameMode == 'Explore':
    gameMode = Explore
if getgameMode == 'SingleExplore':
    gameMode = SingleExplore
if getgameMode == 'RealmRaid':
    gameMode = RealmRaid
if getgameMode == 'RealmRaidW3F3':
    gameMode = RealmRaidW3F3
if getgameMode == 'GuildRealmRaid':
    gameMode = GuildRealmRaid
if getgameMode == 'Explor3Realm':
    gameMode = Explor3Realm
if getgameMode == 'Explor3RealmW3F3':
    gameMode = Explor3RealmW3F3
if getgameMode == 'Event':
    gameMode = Event
if getgameMode == 'Bondling':
    gameMode = Bondling

def function_will_exit():
    sys.exit()

def create_file(data='0'):
    try:
        temp_path = f"runprocess/temp{pid}.txt"
        with open(temp_path, "w") as file:
            file.write(data)
            file.close
    except Exception as error:
        logging.error(error)

def main():
    MyLog.init(loglv='DEBUG') #(Use: INFO, DEBUG, OFF)
    logging.debug('GameMode:[%s], Server:[%s], Total Round:[%s]',getgameMode, Server, total)
    accounts.append(gameMode(Server, windowName, beforetotal, total, pid, bondlingmode, pactsettings, crystal_use, tomb, snowball, azure, kuro))
    account=threading.Thread(accounts[0].run())

if __name__ == '__main__':
    try:
        main()
        
    except Exception as error:
        logging.error(error)
        create_file(data=str(total))
        time.sleep(10)
    
