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
import sys

accounts=[]
Server=[]
pid = os.getpid()

getgameMode=sys.argv[1]
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

def function_will_exit():
    sys.exit()

def main():
    global Server
    Server = sys.argv[2]
    windowName = sys.argv[3]
    total = int(sys.argv[4])
    wanted = int(sys.argv[5])
    wtdelay = float(sys.argv[6])
    findimgdelay = float(sys.argv[7])
    accounts.append(gameMode(Server, windowName, total, wanted, wtdelay, findimgdelay, pid))
    account=threading.Thread(accounts[0].run())

if __name__ == '__main__':
    try:
        main()
    except:
        time.sleep(200)
    
